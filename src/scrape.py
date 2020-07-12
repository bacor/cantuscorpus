"""
Script used to scrape the CANTUS API
"""

import requests
import time
import logging
import os
import math
import datetime
from helpers import write_gzip_json

# Disable InsecureRequestWarning, triggered by an expired SSL certificate
# of the Abbot server.
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

### Globals

ABBOT_ENDPOINT = 'https://abbot.uwaterloo.ca:8888'
MAX_PAGE_SIZE = 100
SRC_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(os.path.join(SRC_DIR, os.path.pardir))
DIST_DIR = os.path.join(ROOT_DIR, 'dist')
SCRAPE_DIR = os.path.join(ROOT_DIR, 'scrape')

### Helpers

def relpath(path, start=ROOT_DIR):
    return os.path.relpath(path, start=start)

### 

class AbbotScraper:

    def __init__(self, name='scrape', endpoint=ABBOT_ENDPOINT, scrape_dir=SCRAPE_DIR,
        request_delay=0.5, date=datetime.date.today().strftime("%Y-%m-%d")):
        """The AbbotScraper class.

        The scraper can scrape the entire Cantus database. It stores all 
        resources as gzipped JSON files, with one file per page.

        Parameters
        ----------
        name : str, optional
            A name for the scraping session, by default 'scrape'. This is used
            to name the directory where the results are stored.
        endpoint : str, optional
            The URL of the Abbot API, by default ABBOT_ENDPOINT.
        scrape_dir : [type], optional
            The directory where Cantus dumps are stored], by default SCRAPE_DIR
        request_delay : float, optional
            a delay between requests in seconds, by default 0.5
        date : string, optional
            a date string used to name the output directory. This defaults to
            today.
        """
        self.name = f'{date}-{name}'
        self.endpoint = endpoint
        self.request_delay = 0.5

        # Directories
        self.output_dir = os.path.join(scrape_dir, self.name)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.pages_dir = os.path.join(self.output_dir, 'pages')
        if not os.path.exists(self.pages_dir):
            os.makedirs(self.pages_dir)

        # Setup logging
        log_fn = os.path.join(self.output_dir, 'scraping.log')
        logging.basicConfig(
            filename=log_fn,
            filemode='w',
            format='%(levelname)s %(asctime)s %(message)s',
            datefmt='%d-%m-%y %H:%M:%S',
            level=logging.INFO)
        logging.info(f'Scraper {self.name} initialized')
        logging.info(f'Logging to {relpath(log_fn)}')
        logging.info(f'Storing pages in {relpath(self.pages_dir)}')

        # Connect to the Abbot API
        # Verify is false because the Abbot ssh certificate has expired (07-2020)
        self.request_params = dict(verify=False)
        self.request_url = None
        self.connect()

    def get(self, url=None, **kwargs):
        """Send a GET request to the Abbot server.

        Parameters
        ----------
        url : str or None, optional
            The request URL, by default the endpoint/browse/ url
        **kwargs
            Optional keyword arguments passed to requests.get

        Returns
        -------
        requests.models.Response
            The response
        """
        if url is None:
            url = self.request_url
        for key, value in self.request_params.items():
            if key not in kwargs:
                kwargs[key] = value
        response = requests.get(url, **kwargs)
        response.raise_for_status()
        time.sleep(self.request_delay)
        return response

    def connect(self):
        """Connect to the Abbot server and retrieve the request url used during
        scraping. If the connection to the server cannot be established, an 
        exception is raised."""
        response = self.get(self.endpoint)
        if 'X-Cantus-Version' not in response.headers:
            logging.error('Connection could not be established.')
            raise Warning('Endpoint does not point to CANTUS API')
        else:
            # Second request, now to browse/all
            self.request_url = response.json()['resources']['browse']['all']
            logging.info('Connection established.')
            logging.info('* Request URL: ' + self.request_url)
            logging.info('* Server: ' + response.headers['Server'])
            logging.info('* X-Cantus-Version: ' + response.headers['X-Cantus-Version'])
            
    def scrape(self, start_page=0, end_page=-1, page_size=MAX_PAGE_SIZE):
        """Scrape the Abbot API

        Parameters
        ----------
        start_page : int, optional
            The page where to start, by default 0
        end_page : int, optional
            The end page. If end_page=-1 (the default), all pages are retrieved
        page_size : int, optional
            The number of resources per page, by default 100 (the maximum)
        """
        
        # First request to get the number of pages
        response = self.get(self.request_url)
        num_results = int(response.headers['X-Cantus-Total-Results'])
        num_pages = math.ceil(num_results / page_size)
        if end_page == -1: end_page = num_pages
        logging.info(f'Scraping...')
        logging.info(f'* page size: {page_size}')
        logging.info(f'* total number of results: {num_results}')
        logging.info(f'* total number of pages: {num_pages}')
        logging.info(f'* Start page: {start_page}')
        logging.info(f'* End page: {end_page}')

        durations = []
        pages = range(start_page, end_page + 1)
        for i, page_num in enumerate(pages):
            t0 = time.time()
            page = self.get_page(page_num, page_size=page_size)
            page_fn = os.path.join(self.pages_dir, f'page-{page_num:04d}.json.gz')
            write_gzip_json(page_fn, page)
            durations.append(time.time() - t0)
            
            # Report progress: pages left and expected remaining time
            durations = durations[-50:]
            avg_duration = sum(durations) / len(durations)
            seconds = round((end_page - page_num) * avg_duration)
            remaining = str(datetime.timedelta(seconds=seconds))
            print(f'Page {page_num:04d}/{end_page} done. Time remaining: {remaining}',
                end='\r')

    def get_page(self, page, page_size):
        """Retrieve the resources on a given page

        Parameters
        ----------
        page : int
            the page number of the pageto retrieve
        page_size : int
            The page size

        Returns
        -------
        dict
            The page as a dictionary with keys `page`, `resources` and 
            `complete` (a flag indicating whether number of resources returned
            matches the page size).
        """
        assert int(page) > 0
        assert page_size <= MAX_PAGE_SIZE
        headers = {
            "X-Cantus-Include-Resources": "true",
            "X-Cantus-Per-Page": str(page_size),
            "X-Cantus-Page": str(page),
            "X-Cantus-Sort": "id;asc"
        }
        try:   
            req = self.get(self.request_url, headers=headers)
            results = req.json()
        except:
            logging.error(f'Request failed at page {page}, skipping...')
            results = {}

        # Extract entries and add ids of linked resources to the entries (only
        # the id, not the resource URIs)
        entries = {}
        for id, value in results.items():
            if id in ['resources', 'sort_order']: continue
            entries[id] = value
            if id in results['resources'].keys():
                for field, value in results['resources'][id].items():
                    if field.endswith('_id'):
                        assert field not in entries[id]
                        entries[id][field] = value
        
        logging.info(f"Scraped page {page} with {len(entries)} resources") 
        return {
            'page': page,
            'resources': entries,
            'complete': len(entries) == page_size
        }

###

if __name__ == "__main__":
    scraper = AbbotScraper('scrape-v0.1')
    scraper.scrape(start_page=1, end_page=-1)
