from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..db.database import get_db
from ..models.product import Product, PriceHistory, User
from ..schemas.product import (
    ProductCreate, ProductUpdate, Product as ProductSchema,
    PriceHistory as PriceHistorySchema, UserCreate, User as UserSchema
)
from ..services.scraper_runner import scraper_service
from ..services.scheduler import price_scheduler

router = APIRouter(prefix="/api/v1", tags=["tracker"])

# Product endpoints
@router.post("/products/", response_model=ProductSchema)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product to track"""
    # Check if product already exists
    existing_product = db.query(Product).filter(Product.url == str(product.url)).first()
    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="Product with this URL already exists"
        )
    
    # Scrape initial product data
    scraped_data = await scraper_service.scrape_product(str(product.url))
    
    # Create product with scraped data
    db_product = Product(
        name=scraped_data.get('name', product.name),
        url=str(product.url),
        current_price=scraped_data.get('price'),
        target_price=product.target_price,
        image_url=scraped_data.get('image_url'),
        description=scraped_data.get('description'),
        platform=scraped_data.get('platform', product.platform)
    )
    
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Add initial price history
    if db_product.current_price:
        price_history = PriceHistory(
            product_id=db_product.id,
            price=db_product.current_price
        )
        db.add(price_history)
        db.commit()
    
    return db_product

@router.get("/products/", response_model=List[ProductSchema])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all tracked products"""
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.get("/products/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    """Update a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.get("/products/{product_id}/price-history", response_model=List[PriceHistorySchema])
def get_price_history(product_id: int, db: Session = Depends(get_db)):
    """Get price history for a product"""
    price_history = db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id
    ).order_by(PriceHistory.timestamp.desc()).all()
    return price_history

@router.post("/products/{product_id}/check-price")
async def check_price_now(product_id: int, db: Session = Depends(get_db)):
    """Manually trigger price check for a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check price using scheduler service
    price_scheduler.check_single_product_price(product, db)
    
    db.refresh(product)
    return {"message": "Price check completed", "current_price": product.current_price}

# User endpoints
@router.post("/users/", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    db_user = User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/", response_model=List[UserSchema])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all users"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users
