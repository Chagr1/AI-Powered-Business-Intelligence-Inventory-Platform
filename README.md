# 🚀 AI-Powered Business Intelligence & Inventory Platform

A robust, real-time backend enterprise system built with FastAPI. This platform integrates secure inventory management, transaction-safe order processing, and an embedded LLM-powered Business Assistant (via Groq API) to provide actionable business intelligence insights.

## ✨ Key Features

* **🔐 Secure Authentication & RBAC:** JWT-based user authentication with Role-Based Access Control (Admin & Manager roles).
* **📦 Advanced Inventory Management:** Full CRUD operations for product catalogs and dynamic stock tracking.
* **🛒 Transactional Order Processing:** Secure and atomic SQL transactions to handle sales and prevent data inconsistency during checkout.
* **📊 Real-Time Analytics:** Live endpoints for calculating total revenue, order volume, and top-performing products.
* **🤖 AI Business Assistant:** An integrated LLM endpoint (powered by Groq `openai/gpt-oss-20b`) that reads live PostgreSQL data and generates strategic business reports and recommendations instantly.

## 🛠️ Tech Stack

* **Framework:** Python, FastAPI
* **Database:** PostgreSQL (Neon Tech), SQLAlchemy (ORM)
* **Data Validation:** Pydantic
* **AI Integration:** Groq API 
* **Security:** Passlib (Bcrypt), Python-JOSE (JWT)

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Chagr1/AI-Powered-Business-Intelligence-Inventory-Platform.git](https://github.com/Chagr1/AI-Powered-Business-Intelligence-Inventory-Platform.git)
   cd AI-Powered-Business-Intelligence-Inventory-Platform
