# FastAPI E-Commerce API

## Overview
This is a **FastAPI-based E-Commerce API** that allows users to **manage customers, products, and orders**. It provides full **CRUD operations** with proper validation, filtering, and status updates.

---

## Tech Stack
- **FastAPI** - Web framework  
- **Pydantic** - Data validation  
- **SQLAlchemy** - ORM for database  
- **MySQL** (or SQLite for testing) - Database  
- **Pytest** - Unit testing  

---



## API Endpoints

### Customers API
| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/customers/` | Create a new customer |
| **GET** | `/customers/` | Get all customers |
| **GET** | `/customers/{customer_id}` | Get customer details by ID |
| **PUT** | `/customers/{customer_id}` | Update customer details |
| **DELETE** | `/customers/{customer_id}` | Delete a customer |


---

### Products API
| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/products/` | Create a new product |
| **GET** | `/products/{product_id}` | Get product details |
| **PUT** | `/products/{product_id}` | Update product details |
| **DELETE** | `/products/{product_id}` | Delete a product |


---

### Orders API
| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/orders/` | Create an order |
| **GET** | `/orders/{order_id}` | Get order details |
| **PUT** | `/orders/{order_id}` | Update order status |
| **DELETE** | `/orders/{order_id}` | Delete an order |


---


