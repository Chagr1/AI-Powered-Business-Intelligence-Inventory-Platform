from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
        order_data: OrderCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)  # Any logged-in user can order
):
    # 1. Create the base order
    new_order = Order(user_id=current_user.id, total_amount=0)
    db.add(new_order)
    db.flush()  # Gets the new_order.id without committing to the database yet

    total_amount = 0.0

    # 2. Process each item in the order
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            db.rollback()  # Cancel the entire transaction
            raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found")

        if product.stock < item.quantity:
            db.rollback()  # Cancel if insufficient stock
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for '{product.name}'. Available: {product.stock}"
            )

        # Deduct stock
        product.stock -= item.quantity

        # Calculate pricing
        item_total = product.price * item.quantity
        total_amount += item_total

        # Add order item
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price
        )
        db.add(order_item)

    # 3. Finalize order and commit transaction
    new_order.total_amount = total_amount
    db.commit()
    db.refresh(new_order)

    return new_order