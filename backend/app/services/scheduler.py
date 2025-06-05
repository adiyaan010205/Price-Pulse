from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from ..db.database import SessionLocal
from ..models.product import Product, PriceHistory
from .scraper_runner import scraper_service
from .email_alert import email_service
import logging

class PriceScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.setup_jobs()
    
    def setup_jobs(self):
        """Setup scheduled jobs"""
        # Check prices every hour
        self.scheduler.add_job(
            func=self.check_all_prices,
            trigger=IntervalTrigger(hours=1),
            id='price_check_hourly',
            name='Check all product prices',
            replace_existing=True
        )
        
        # Daily cleanup job
        self.scheduler.add_job(
            func=self.cleanup_old_data,
            trigger=CronTrigger(hour=2, minute=0),  # 2 AM daily
            id='daily_cleanup',
            name='Daily data cleanup',
            replace_existing=True
        )
    
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logging.info("Price scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logging.info("Price scheduler stopped")
    
    def check_all_prices(self):
        """Check prices for all active products"""
        db = SessionLocal()
        try:
            active_products = db.query(Product).filter(Product.is_active == True).all()
            
            for product in active_products:
                self.check_single_product_price(product, db)
                
        except Exception as e:
            logging.error(f"Error in price check job: {e}")
        finally:
            db.close()
    
    def check_single_product_price(self, product: Product, db: Session):
        """Check price for a single product"""
        try:
            # Scrape current price
            scraped_data = scraper_service.scrape_product_sync(product.url)
            
            if scraped_data and 'price' in scraped_data:
                new_price = scraped_data['price']
                old_price = product.current_price
                
                # Update product price
                product.current_price = new_price
                
                # Save price history
                price_history = PriceHistory(
                    product_id=product.id,
                    price=new_price
                )
                db.add(price_history)
                
                # Check for price drop alert
                if (old_price and new_price < old_price and 
                    product.target_price and new_price <= product.target_price):
                    
                    # Get user emails (you'd need to implement user-product relationships)
                    # For now, using a placeholder email
                    user_email = "user@example.com"  # Replace with actual user lookup
                    
                    email_service.send_price_alert(
                        recipient_email=user_email,
                        product_name=product.name,
                        old_price=old_price,
                        new_price=new_price,
                        product_url=product.url
                    )
                
                db.commit()
                logging.info(f"Updated price for {product.name}: ${new_price}")
                
        except Exception as e:
            logging.error(f"Error checking price for product {product.id}: {e}")
            db.rollback()
    
    def cleanup_old_data(self):
        """Clean up old price history data"""
        db = SessionLocal()
        try:
            # Keep only last 30 days of price history
            from datetime import datetime, timedelta
            cutoff_date = datetime.now() - timedelta(days=30)
            
            deleted_count = db.query(PriceHistory).filter(
                PriceHistory.timestamp < cutoff_date
            ).delete()
            
            db.commit()
            logging.info(f"Cleaned up {deleted_count} old price history records")
            
        except Exception as e:
            logging.error(f"Error in cleanup job: {e}")
        finally:
            db.close()

price_scheduler = PriceScheduler()
