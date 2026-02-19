import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class APIDiscovery:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0'}
    
    def discover_apis(self, search_terms):
        """
        Discovers APIs based on search terms by scraping API directories.
        Args:
            search_terms (list): List of keywords to search for.
        Returns:
            list: List of discovered API endpoints and documentation links.
        """
        api_info = []
        try:
            for term in search_terms:
                self._scrape_api_catalog(term, api_info)
        except Exception as e:
            logger.error(f"API discovery failed: {str(e)}")
        return api_info
    
    def _scrape_api_catalog(self, term, api_info):
        """
        Scrapes an API catalog for the given search term.
        Args:
            term (str): Search term to look up.
            api_info (list): List to append discovered APIs.
        """
        url = f"https://api-directory.com/search/{term}"
        try:
            response = self.session.get(url, headers=self.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for api_card in soup.find_all('div', class_='api-card'):
                    name = api_card.find('h3').text
                    endpoint = api_card.find('a')['href']
                    doc_link = api_card.find('p', class_='doc-link').text
                    api_info.append({'name': name, 'endpoint': endpoint, 'documentation': doc_link})
        except Exception as e:
            logger.error(f"Scraping failed for {term}: {str(e)}")