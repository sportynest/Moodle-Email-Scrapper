from bs4 import BeautifulSoup
import requests
import logging
import time
import random
import json
from urllib.parse import unquote
from typing import List, Dict

# Configure logging
logging.basicConfig(
    filename="eclass_scrape.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class MoodleScraper:
    def __init__(self, base_url: str, cookies: Dict[str, str]):
        self.base_url = base_url
        self.cookies = cookies
        self.email_file = 'user_emails.json'

    def extract_emails(self, html_content: str) -> List[str]:
        """
        Extracts email addresses from HTML content by finding mailto: links.
        
        Args:
            html_content (str): HTML content to parse
            
        Returns:
            List[str]: List of decoded email addresses
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        email_links = soup.find_all('a', href=lambda href: href and 'mailto:' in href)
        emails = [link['href'].replace('mailto:', '') for link in email_links]
        
        decoded_emails = []
        for email in emails:
            try:
                decoded_email = unquote(email)
                decoded_emails.append(decoded_email)
            except Exception as e:
                logging.error(f"Error decoding email {email}: {e}")
                decoded_emails.append(email)
                
        return decoded_emails

    def scrape_course_emails(self, course_id: str) -> List[str]:
        """
        Scrapes emails from Moodle user profiles using browser cookies.
        
        Args:
            course_id (str): The course ID to scrape
            
        Returns:
            List[str]: List of unique email addresses
        """
        email_data = self._load_email_data()
        all_contacts = self._get_all_student_contacts(course_id)
        all_emails = self._process_contacts(all_contacts)
        self._save_emails(all_emails, email_data)
        
        return all_emails

    def _load_email_data(self) -> Dict:
        """Loads existing email data from JSON file."""
        try:
            with open(self.email_file, 'r') as f:
                email_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            email_data = {}

        if 'moodle' not in email_data:
            email_data['moodle'] = []
            
        return email_data

    def _get_all_student_contacts(self, course_id: str) -> List[str]:
        """Collects all student contact URLs from the course."""
        all_contacts = []
        page = 0
        
        while True:
            participants_url = f"{self.base_url}/user/index.php?id={course_id}&page={page}"
            
            try:
                response = requests.get(participants_url, cookies=self.cookies)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                page_contacts = self._extract_student_contacts(soup)
                
                if not page_contacts:
                    break
                    
                all_contacts.extend(page_contacts)
                logging.info(f"Found {len(page_contacts)} contacts on page {page + 1}")
                
                if not self._has_next_page(soup, page):
                    break
                    
                page += 1
                time.sleep(random.uniform(1, 2))
                
            except Exception as e:
                logging.error(f"Error processing page {page}: {e}")
                break

        return list(dict.fromkeys(all_contacts))

    def _extract_student_contacts(self, soup: BeautifulSoup) -> List[str]:
        """Extracts student contact URLs from a page."""
        contacts = []
        checkboxes = soup.find_all('input', attrs={
            'data-toggle': 'slave',
            'data-togglegroup': 'participants-table'
        })
        
        for checkbox in checkboxes:
            row = checkbox.find_parent('tr')
            if row:
                role_cell = row.find('td', {'class': 'cell c2'})
                if role_cell and role_cell.text.strip() == 'Student':
                    link = row.find('a', href=True)
                    if link and 'demostudent' not in link.text.strip().lower():
                        contacts.append(link['href'])
        
        return contacts

    def _has_next_page(self, soup: BeautifulSoup, current_page: int) -> bool:
        """Checks if there is a next page of results."""
        return bool(soup.find('li', {
            'class': 'page-item',
            'data-page-number': str(current_page + 2)
        }))

    def _process_contacts(self, contacts: List[str]) -> List[str]:
        """Processes contact URLs to extract emails."""
        all_emails = []
        
        for contact_url in contacts:
            try:
                response = requests.get(contact_url, cookies=self.cookies)
                response.raise_for_status()
                emails = self.extract_emails(response.text)
                all_emails.extend(emails)
                time.sleep(random.uniform(0.5, 1))
                
            except Exception as e:
                logging.error(f"Error processing contact {contact_url}: {e}")
                continue
                
        return list(dict.fromkeys(all_emails))

    def _save_emails(self, new_emails: List[str], email_data: Dict):
        """Saves unique emails to JSON file."""
        email_data['moodle'] = list(set(email_data['moodle'] + new_emails))
        
        with open(self.email_file, 'w') as f:
            json.dump(email_data, f, indent=4)
            
        logging.info(f"Saved {len(new_emails)} emails to {self.email_file}") 