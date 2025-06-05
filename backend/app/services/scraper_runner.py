from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from twisted.internet.asyncioreactor import install
import asyncio
import threading
from ..scrapy_spiders.product_spider import ProductSpider
import logging

class ScraperService:
    def __init__(self):
        self.runner = None
        self.setup_reactor()
    
    def setup_reactor(self):
        """Setup the Twisted reactor for asyncio compatibility"""
        try:
            install()
        except:
            pass  # Reactor already installed
    
    async def scrape_product(self, url: str) -> dict:
        """Scrape product data from given URL"""
        try:
            # Create a new event loop for the scraping operation
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Use CrawlerProcess for one-time scraping
            process = CrawlerProcess(get_project_settings())
            
            # Store result
            result = {}
            
            def spider_closed(spider):
                result.update(spider.scraped_data)
            
            # Connect to spider_closed signal
            from scrapy import signals
            from pydispatch import dispatcher
            dispatcher.connect(spider_closed, signal=signals.spider_closed)
            
            # Run the spider
            process.crawl(ProductSpider, url=url)
            process.start()
            
            return result
            
        except Exception as e:
            logging.error(f"Error scraping {url}: {str(e)}")
            return {}
    
    def scrape_product_sync(self, url: str) -> dict:
        """Synchronous version for background tasks"""
        settings = get_project_settings()
        process = CrawlerProcess(settings)
        
        result = {}
        
        def spider_closed(spider):
            nonlocal result
            result = spider.scraped_data
        
        from scrapy import signals
        from pydispatch import dispatcher
        dispatcher.connect(spider_closed, signal=signals.spider_closed)
        
        process.crawl(ProductSpider, url=url)
        process.start()
        
        return result

scraper_service = ScraperService()
