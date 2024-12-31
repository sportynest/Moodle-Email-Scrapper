# Moodle Email Scraper

## Overview

The Moodle Email Scraper is a Python application designed to scrape email addresses from Moodle user profiles within a classroom. As a member of the classroom, you can use your browser cookies for authentication and navigation within the Moodle platform. The application extracts email addresses from the user's profiles and stores them in a JSON file for easy access and management.

## Features

- Extracts email addresses from HTML content by identifying `mailto:` links.
- Manages pagination to retrieve all participants in a course.
- Eliminates duplicate email addresses while maintaining order.
- Stores extracted email addresses in a JSON file.
- Provides configurable logging to monitor the scraping process.

## Requirements

- Python 3.x
- `beautifulsoup4` library
- `requests` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/sportynest/MOODLE-EMAIL-SCRAPPER.git
    cd MOODLE-EMAIL-SCRAPPER
    ```

2. Install the required libraries:
    ```sh
    pip install beautifulsoup4 requests
    ```

## Usage

### Example Usage

1. Define the base URL and course ID:
    ```python
    base_url = "https://yourmoodle.domain"
    course_id = "123456"
    ```

2. Use your actual browser cookies:
    ```python
    cookies = {
        "LPSID-8169955": "ABcdEfGhIjKlMnOpQrStUvWxYz123456",
        "LPVID": "1234567890abcdef1234567890abcdef",
        "MDL_SSP_AuthToken": "abcdef1234567890abcdef1234567890abcdef12",
        "MDL_SSP_SessID": "1234567890abcdef1234567890abcdef",
        "MOODLEID1_": "%25AB%25CD%25EF%25GH%25IJ%25KL",
        "MoodleSession": "abcdef1234567890abcdef1234567890",
        "cookieyes-consent": "consentid:AbCdEfGhIjKlMnOpQrStUvWxYz,consent:yes,action:,necessary:yes,functional:yes,analytics:yes,performance:yes,advertisement:yes,other:yes",
        "mayaauth": "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
        "pyauth": "abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890"
    }
    ```

3. Execute the scraper:
    ```python
    from moodle_scraper import MoodleScraper

    scraper = MoodleScraper(base_url, cookies)
    emails = scraper.scrape_course_emails(course_id)
    print(emails)
    ```

### Functions

#### `extract_emails(html_content: str) -> List[str]`

Extracts email addresses from HTML content by identifying `mailto:` links.

- **Args:**
  - `html_content` (str): HTML content to parse.
- **Returns:**
  - `List[str]`: List of decoded email addresses.

#### `scrape_course_emails(course_id: str) -> List[str]`

Scrapes emails from Moodle user profiles using browser cookies.

- **Args:**
  - `course_id` (str): The course ID to scrape.
- **Returns:**
  - `List[str]`: List of unique email addresses.

#### `_load_email_data() -> Dict`

Loads existing email data from a JSON file.

- **Returns:**
  - `Dict`: Dictionary containing email data.

#### `_get_all_student_contacts(course_id: str) -> List[str]`

Gathers all student contact URLs from the course.

- **Args:**
  - `course_id` (str): The course ID to scrape.
- **Returns:**
  - `List[str]`: List of student contact URLs.

#### `_extract_student_contacts(soup: BeautifulSoup) -> List[str]`

Extracts student contact URLs from a page.

- **Args:**
  - `soup` (BeautifulSoup): Parsed HTML content.
- **Returns:**
  - `List[str]`: List of student contact URLs.

#### `_has_next_page(soup: BeautifulSoup, current_page: int) -> bool`

Determines if there is a subsequent page of results.

- **Args:**
  - `soup` (BeautifulSoup): Parsed HTML content.
  - `current_page` (int): Current page number.
- **Returns:**
  - `bool`: True if there is a next page, False otherwise.

#### `_process_contacts(contacts: List[str]) -> List[str]`

Processes contact URLs to extract emails.

- **Args:**
  - `contacts` (List[str]): List of contact URLs.
- **Returns:**
  - `List[str]`: List of unique email addresses.

#### `_save_emails(new_emails: List[str], email_data: Dict)`

Saves unique emails to a JSON file.

- **Args:**
  - `new_emails` (List[str]): List of new email addresses.
  - `email_data` (Dict): Dictionary containing existing email data.

## Logging

The scraper utilizes Python's built-in logging module to log details about the scraping process. Logs are stored in `eclass_scrape.log` with the format: `%(asctime)s - %(levelname)s - %(message)s`.

