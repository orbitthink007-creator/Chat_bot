import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_website(url: str = "https://www.orbitthinkservices.com/") -> str:
    """
    Scrapes the content from the OrbitThink website.
    Returns the cleaned text content.
    """
    try:
        logger.info(f"Starting scrape for {url}")
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
        
        logger.info(f"Successfully scraped {len(cleaned_text)} characters")
        return cleaned_text
    except Exception as e:
        logger.error(f"Error scraping website: {e}")
        return ""

if __name__ == "__main__":
    print(scrape_website())
