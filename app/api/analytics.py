from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.db.database import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.api.dependencies import require_role

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
def get_sales_summary(
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role(["admin", "manager"]))
):
    """Returns total revenue and total order count across the platform."""

    # SQL: SELECT COUNT(id) FROM orders;
    total_orders = db.query(func.count(Order.id)).scalar() or 0

    # SQL: SELECT SUM(total_amount) FROM orders;
    total_revenue = db.query(func.sum(Order.total_amount)).scalar() or 0.0

    return {
        "total_orders": total_orders,
        "total_revenue": total_revenue
    }


@router.get("/top-products")
def get_top_products(
        limit: int = 5,
        db: Session = Depends(get_db),
        current_user: User = Depends(require_role(["admin", "manager"]))
):
    """Returns the best-selling products using SQL JOIN and GROUP BY."""

    # SQL Equivalent:
    # SELECT products.name, SUM(order_items.quantity), SUM(order_items.quantity * order_items.unit_price)
    # FROM products
    # JOIN order_items ON products.id = order_items.product_id
    # GROUP BY products.id, products.name
    # ORDER BY total_sold DESC LIMIT 5;

    results = (
        db.query(
            Product.name.label("product_name"),
            func.sum(OrderItem.quantity).label("total_sold"),
            func.sum(OrderItem.quantity * OrderItem.unit_price).label("revenue")
        )
        .join(OrderItem, Product.id == OrderItem.product_id)
        .group_by(Product.id, Product.name)
        .order_by(desc("total_sold"))
        .limit(limit)
        .all()
    )

    return [
        {
            "product_name": row.product_name,
            "total_sold": row.total_sold,
            "revenue": row.revenue
        }
        for row in results
    ]