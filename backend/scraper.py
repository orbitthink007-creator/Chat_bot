import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urlparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_single_page(url: str) -> str:
    """
    Scrapes a single page and returns cleaned text.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()
            
        text = soup.get_text(separator=' ')
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        cleaned_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return cleaned_text
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return ""

def scrape_website(base_url: str = "https://www.orbitthinkservices.com/") -> str:
    """
    Scrapes multiple pages from the OrbitThink website.
    Returns combined cleaned text content.
    """
    # List of pages to scrape
    pages_to_scrape = [
        "",  # Homepage
        "services",
        "about",
        "contact",
        "portfolio",
        "process",
    ]
    
    all_content = []
    
    for page in pages_to_scrape:
        url = urljoin(base_url, page)
        logger.info(f"Scraping: {url}")
        
        content = scrape_single_page(url)
        if content:
            all_content.append(f"=== Content from {url} ===\n{content}\n")
    
    combined_content = "\n\n".join(all_content)
    logger.info(f"Successfully scraped {len(combined_content)} total characters from {len(all_content)} pages")
    
    return combined_content

if __name__ == "__main__":
    print(scrape_website())

