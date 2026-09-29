from fastapi import FastAPI
from app.db.database import engine, Base
from app.models.user import User
from app.models.product import Product
from app.models.order import Order, OrderItem

from app.api import auth
from app.api import products
from app.api import orders
from app.api import analytics

app = FastAPI(title="AI-Powered Business Intelligence API")

# Initialize database tables
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(analytics.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Enterprise Backend System!"}