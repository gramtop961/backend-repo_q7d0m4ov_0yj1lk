import os
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

from database import create_document, get_documents
from schemas import Order, OrderItem

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("bitsbites")

app = FastAPI(title="Bits&Bites API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Bits&Bites API is running"}


# ---------- Products (static menu for now) ----------

class Product(BaseModel):
    name: str
    price: float

class Category(BaseModel):
    category: str
    items: List[Product]


def menu_data() -> List[Dict[str, Any]]:
    return [
        {
            "category": "Starters",
            "items": [
                {"name": "Veg Manchuria", "price": 90},
                {"name": "Gobi Manchuria", "price": 100},
                {"name": "Crispy Corn", "price": 90},
                {"name": "Baby Corn Manchuria", "price": 110},
                {"name": "Paneer Manchuria", "price": 130},
                {"name": "Chilli Paneer", "price": 130},
                {"name": "Gobi 65", "price": 130},
                {"name": "Chicken Manchuria", "price": 130},
                {"name": "Chilli Chicken", "price": 130},
                {"name": "Kaju Chicken", "price": 150},
                {"name": "Ginger Chicken", "price": 130},
                {"name": "Chicken 65", "price": 130},
                {"name": "Egg 65", "price": 110},
                {"name": "Egg Manchuria", "price": 110},
                {"name": "Egg Chilli", "price": 110},
                {"name": "Mushroom Manchuria", "price": 129},
                {"name": "Chicken Drum Sticks", "price": 180},
                {"name": "Chicken Wings", "price": 200},
                {"name": "Garlic Chicken", "price": 130},
                {"name": "Butter Garlic Chicken", "price": 140},
                {"name": "Schezwan Prawns", "price": 210},
                {"name": "Chilly Prawns", "price": 180},
                {"name": "Crispy Prawns", "price": 200},
                {"name": "Maggi Pakora", "price": 120},
            ],
        },
        {
            "category": "Rolls",
            "items": [
                {"name": "Veg Roll", "price": 90},
                {"name": "Veg Cheese Roll", "price": 120},
                {"name": "Egg Roll", "price": 100},
                {"name": "Paneer Roll", "price": 120},
                {"name": "Paneer Cheese Roll", "price": 140},
                {"name": "Chicken Roll", "price": 130},
                {"name": "Chicken Cheese Roll", "price": 150},
                {"name": "Egg Chicken Roll", "price": 150},
                {"name": "Mutton Keema Roll", "price": 160},
                {"name": "Double Chicken Cheese Roll", "price": 160},
            ],
        },
        {
            "category": "Breads & Puffs",
            "items": [
                {"name": "Garlic Bread", "price": 70},
                {"name": "Aloo Samosa (2 pieces)", "price": 30},
                {"name": "Veg Puff", "price": 35},
                {"name": "Egg Puff", "price": 50},
                {"name": "Chicken Puff", "price": 50},
                {"name": "Paneer Puff", "price": 50},
                {"name": "Potato Wedges", "price": 80},
                {"name": "French Fries", "price": 80},
            ],
        },
        {
            "category": "Dosa",
            "items": [
                {"name": "Rava Dosa", "price": 55},
                {"name": "Onion Rava Dosa", "price": 65},
                {"name": "Plain Dosa", "price": 35},
                {"name": "Masala Dosa", "price": 50},
                {"name": "Onion Dosa", "price": 50},
                {"name": "Onion Rava Masala Dosa", "price": 65},
                {"name": "Pizza Dosa", "price": 130},
                {"name": "Upma Dosa", "price": 80},
                {"name": "Jeera Dosa", "price": 75},
                {"name": "Butter Dosa", "price": 60},
                {"name": "Butter Masala Dosa", "price": 75},
                {"name": "Butter Cheese Dosa", "price": 100},
                {"name": "Butter Corn Dosa", "price": 85},
                {"name": "Butter Karam Dosa", "price": 85},
                {"name": "Double Butter Dosa", "price": 70},
                {"name": "Paneer Dosa", "price": 95},
                {"name": "Paneer Masala Dosa", "price": 110},
                {"name": "Chilli Paneer Dosa", "price": 100},
                {"name": "Paneer Schezwan Dosa", "price": 110},
                {"name": "Paneer Corn Dosa", "price": 110},
                {"name": "Masala Uttapam", "price": 110},
                {"name": "Onion Uttapam", "price": 80},
                {"name": "Kaju Dosa", "price": 135},
                {"name": "Butter Babycorn Dosa", "price": 90},
                {"name": "Spicy Babycorn Dosa", "price": 90},
                {"name": "Paneer Babycorn Dosa", "price": 110},
                {"name": "Cheese Babycorn Dosa", "price": 100},
                {"name": "Cheese Dosa", "price": 100},
                {"name": "Cheese Masala Dosa", "price": 100},
                {"name": "Double Cheese Dosa", "price": 120},
                {"name": "Cheese Schezwan Dosa", "price": 130},
                {"name": "Chilli Cheese Dosa", "price": 90},
                {"name": "Cheese Corn Dosa", "price": 105},
                {"name": "Spl Ghee Masala Dosa", "price": 80},
                {"name": "Ghee Karam Dosa", "price": 75},
                {"name": "Plain Ghee Dosa", "price": 65},
                {"name": "Plain Uttapam", "price": 65},
                {"name": "Butter Uttapam", "price": 85},
                {"name": "Cheese Uttapam", "price": 110},
                {"name": "Kaju Cheese Uttapam", "price": 140},
                {"name": "Panner Uttapam", "price": 110},
                {"name": "Paneer Cheese Uttapam", "price": 130},
            ],
        },
        {
            "category": "Idli",
            "items": [
                {"name": "Plain Idli (4 pieces)", "price": 40},
                {"name": "Butter Idli", "price": 50},
                {"name": "Plain Ghee Idli", "price": 55},
                {"name": "Karam Podi Idli", "price": 55},
                {"name": "Guntur Ghee Idli", "price": 65},
                {"name": "Sambhar Idli", "price": 60},
                {"name": "Paneer Schezwan Idli", "price": 85},
                {"name": "Cheese Schezwan Idli", "price": 100},
                {"name": "Idli 65", "price": 80},
            ],
        },
        {
            "category": "Fried Rice",
            "items": [
                {"name": "Veg Fried Rice", "price": 90},
                {"name": "Veg Manchurian Fried Rice", "price": 110},
                {"name": "Gobi Fried Rice", "price": 110},
                {"name": "Egg Fried Rice", "price": 110},
                {"name": "Double Egg Fried Rice", "price": 120},
                {"name": "Double Egg Dble Chicken Fried Rice", "price": 150},
                {"name": "Paneer Fried Rice", "price": 120},
                {"name": "Mixed Non Veg Fried Rice", "price": 180},
                {"name": "Babycorn Fried Rice", "price": 120},
                {"name": "Mushroom Fried Rice", "price": 120},
                {"name": "Chicken Fried Rice", "price": 130},
                {"name": "Double chicken fried rice", "price": 140},
                {"name": "Chicken Schezwan Fried Rice", "price": 140},
            ],
        },
        {
            "category": "Noodles",
            "items": [
                {"name": "Veg Noodles", "price": 90},
                {"name": "Veg Manchurian Noodles", "price": 100},
                {"name": "Gobi Noodles", "price": 110},
                {"name": "Egg Noodles", "price": 110},
                {"name": "Double Egg Noodles", "price": 120},
                {"name": "Chicken Noodles", "price": 120},
                {"name": "Double Chicken Noodles", "price": 140},
                {"name": "Paneer Noodles", "price": 120},
                {"name": "Mushroom Noodles", "price": 120},
                {"name": "Babycorn Noodles", "price": 110},
                {"name": "Double Egg Dble Chicken Noodles", "price": 150},
                {"name": "Veg Schezwan Noodles", "price": 110},
                {"name": "Chicken Schezwan Noodles", "price": 130},
            ],
        },
        {
            "category": "Tea & Coffee",
            "items": [
                {"name": "Tea", "price": 20},
                {"name": "Filter Coffee", "price": 25},
                {"name": "Milk", "price": 20},
                {"name": "Black Coffee", "price": 25},
            ],
        },
    ]


@app.get("/products", response_model=List[Category])
def get_products():
    return menu_data()


# ---------- Orders ----------

@app.post("/orders")
def create_order(order: Order):
    if order.payment_method not in ("COD", "UPI"):
        raise HTTPException(status_code=400, detail="Invalid payment method. Use COD or UPI.")

    # Recalculate on server for safety
    subtotal = sum(i.price * i.quantity for i in order.items)
    discount = order.discount if order.discount is not None else 0
    total = max(subtotal - discount, 0)

    doc = {
        "customer_name": order.customer_name,
        "contact_number": order.contact_number,
        "payment_method": order.payment_method,
        "items": [i.model_dump() for i in order.items],
        "subtotal": subtotal,
        "discount": discount,
        "total": total,
        "notes": order.notes,
        "status": order.status,
    }

    inserted_id = create_document("order", doc)

    # Log the payment method as requested (no Razorpay or other gateways involved)
    logger.info("New order saved: id=%s, payment_method=%s, total=%.2f", inserted_id, order.payment_method, total)

    return {"ok": True, "order_id": inserted_id, "total": total}


@app.get("/orders")
def list_orders(limit: int = 50):
    docs = get_documents("order", {}, limit=limit)
    # Convert ObjectId to str if present
    for d in docs:
        _id = d.get("_id")
        if _id is not None:
            d["_id"] = str(_id)
    return docs


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": [],
    }

    try:
        from database import db

        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, "name") else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except ImportError:
        response["database"] = "❌ Database module not found"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    return response


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
