import scrapy
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor, defer
from twisted.internet.asyncioreactor import install
import re
import asyncio
from urllib.parse import urljoin

class ProductSpider(scrapy.Spider):
    name = 'product_spider'
    
    def __init__(self, url=None, *args, **kwargs):
        super(ProductSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url] if url else []
        self.scraped_data = {}
    
    def parse(self, response):
        # Generic product scraping logic
        product_data = {}
        
        # Try different selectors for different platforms
        if 'amazon' in response.url:
            product_data = self.parse_amazon(response)
        elif 'ebay' in response.url:
            product_data = self.parse_ebay(response)
        else:
            product_data = self.parse_generic(response)
        
        self.scraped_data = product_data
        yield product_data
    
    def parse_amazon(self, response):
        return {
            'name': response.css('#productTitle::text').get(),
            'price': self.extract_price(response.css('.a-price-whole::text').get()),
            'image_url': response.css('#landingImage::attr(src)').get(),
            'description': response.css('#feature-bullets ul::text').getall(),
            'platform': 'amazon'
        }
    
    def parse_ebay(self, response):
        return {
            'name': response.css('h1#x-title-label-lbl::text').get(),
            'price': self.extract_price(response.css('.notranslate::text').get()),
            'image_url': response.css('#icImg::attr(src)').get(),
            'description': response.css('.u-flL.condText::text').get(),
            'platform': 'ebay'
        }
    
    def parse_generic(self, response):
        # Fallback parsing for unknown sites
        return {
            'name': response.css('h1::text').get() or response.css('title::text').get(),
            'price': self.extract_price_from_page(response),
            'image_url': response.css('img::attr(src)').get(),
            'description': response.css('meta[name="description"]::attr(content)').get(),
            'platform': 'generic'
        }
    
    def extract_price(self, price_text):
        if not price_text:
            return None
        # Extract numeric price from text
        price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
        return float(price_match.group()) if price_match else None
    
    def extract_price_from_page(self, response):
        # Try to find price using common patterns
        price_selectors = [
            'span[class*="price"]::text',
            'div[class*="price"]::text',
            '*[class*="cost"]::text',
            '*[data-price]::attr(data-price)'
        ]
        
        for selector in price_selectors:
            price_text = response.css(selector).get()
            if price_text:
                price = self.extract_price(price_text)
                if price:
                    return price
        return None
