import requests
from bs4 import BeautifulSoup
import html2text
from pathlib import Path
from typing import Dict, List
import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseDocScraper:
    def __init__(self):
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = False
        self.setup_driver()

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def get_page(self, url: str) -> str:
        try:
            self.driver.get(url)
            # Wait for the content to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(2)  # Give JavaScript a moment to render
            return self.driver.page_source
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return ""
        
    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

class SegmentScraper(BaseDocScraper):
    def scrape(self) -> List[Dict]:
        base_urls = [
            "https://segment.com/docs/connections/sources/catalog/",
            "https://segment.com/docs/connections/destinations/catalog/",
            "https://segment.com/docs/guides/",
        ]
        articles = []
        
        for base_url in base_urls:
            html = self.get_page(base_url)
            if not html:
                continue
                
            soup = BeautifulSoup(html, 'html.parser')
            
            # Updated selectors for Segment's new documentation structure
            for article in soup.select('.DocSearch-content, .doc-content, main article'):
                title = article.find(['h1', 'h2'])
                title = title.text.strip() if title else "Untitled"
                content = self.converter.handle(str(article))
                
                articles.append({
                    'title': title,
                    'content': content,
                    'url': base_url
                })
        
        return articles

class MParticleScraper(BaseDocScraper):
    def scrape(self) -> List[Dict]:
        base_urls = [
            "https://docs.mparticle.com/guides/",
            "https://docs.mparticle.com/developers/sdk/",
            "https://docs.mparticle.com/integrations/"
        ]
        articles = []
        
        for base_url in base_urls:
            html = self.get_page(base_url)
            if not html:
                continue
                
            soup = BeautifulSoup(html, 'html.parser')
            
            # mParticle uses a different structure
            for article in soup.select('.content-body'):
                title = article.find(['h1', 'h2'])
                title = title.text.strip() if title else "Untitled"
                content = self.converter.handle(str(article))
                
                articles.append({
                    'title': title,
                    'content': content,
                    'url': base_url
                })
        
        return articles

class LyticsScraper(BaseDocScraper):
    def scrape(self) -> List[Dict]:
        base_urls = [
            "https://docs.lytics.com/guide/",
            "https://docs.lytics.com/integrations/",
            "https://docs.lytics.com/audiences/"
        ]
        articles = []
        
        for base_url in base_urls:
            html = self.get_page(base_url)
            if not html:
                continue
                
            soup = BeautifulSoup(html, 'html.parser')
            
            # Lytics documentation structure
            for article in soup.select('.documentation-content'):
                title = article.find(['h1', 'h2'])
                title = title.text.strip() if title else "Untitled"
                content = self.converter.handle(str(article))
                
                articles.append({
                    'title': title,
                    'content': content,
                    'url': base_url
                })
        
        return articles

class DocumentationScraper:
    def __init__(self):
        self.data_dir = Path('data/docs')
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize specialized scrapers
        self.scrapers = {
            'segment': SegmentScraper(),
            'mparticle': MParticleScraper(),
            'lytics': LyticsScraper(),
        }
        
        # Default documentation for common queries
        self.default_docs = {
            'segment': [{
                'title': 'Setting up Sources in Segment',
                'content': """
                To set up a new source in Segment:
                1. Log in to your Segment workspace
                2. Navigate to Connections > Sources
                3. Click 'Add Source'
                4. Choose your source type (Website, Mobile App, Server, etc.)
                5. Follow the setup instructions for your specific source
                6. Configure your source settings
                7. Enable the source when ready
                
                Common source types:
                - Analytics.js for websites
                - Mobile SDKs for iOS/Android apps
                - Server-side libraries
                - Cloud sources for SaaS tools
                """,
                'url': 'https://segment.com/docs/connections/sources/'
            }],
            'mparticle': [{
                'title': 'Creating User Profiles in mParticle',
                'content': """
                To create and manage user profiles in mParticle:
                1. Implement identity management
                2. Set up user attributes
                3. Configure identity priority
                4. Define user identity mapping
                5. Enable cross-platform identity resolution
                
                Key concepts:
                - Customer IDs
                - Device IDs
                - User attributes
                - Identity resolution
                """,
                'url': 'https://docs.mparticle.com/guides/idsync/'
            }],
            'lytics': [{
                'title': 'Building Audience Segments in Lytics',
                'content': """
                To build an audience segment in Lytics:
                1. Go to Audiences in your Lytics account
                2. Click 'Create New Audience'
                3. Define segment criteria using:
                   - User behaviors
                   - Profile attributes
                   - Content affinities
                4. Set audience rules and conditions
                5. Save and activate your audience
                
                Best practices:
                - Start with broad criteria
                - Use behavioral data
                - Test audience sizes
                - Monitor audience growth
                """,
                'url': 'https://docs.lytics.com/audiences/'
            }]
        }

    def scrape_documentation(self):
        """Scrape documentation from all CDP sources"""
        # First, save default documentation
        for cdp, content in self.default_docs.items():
            self._save_content(cdp, content)
            logger.info(f"Saved default documentation for {cdp}")

        # Then try to scrape live documentation
        for cdp, scraper in self.scrapers.items():
            try:
                logger.info(f"Scraping {cdp} documentation...")
                content = scraper.scrape()
                if content:
                    self._save_content(cdp, content)
                    logger.info(f"Successfully saved {len(content)} articles for {cdp}")
                time.sleep(2)  # Be nice to servers
            except Exception as e:
                logger.error(f"Error scraping {cdp}: {str(e)}")

    def _save_content(self, cdp: str, content: List[Dict]):
        """Save scraped content to JSON file"""
        if not content:
            return
            
        filepath = self.data_dir / f'{cdp}_docs.json'
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(content)} articles for {cdp}")
        except Exception as e:
            logger.error(f"Error saving content for {cdp}: {str(e)}") 