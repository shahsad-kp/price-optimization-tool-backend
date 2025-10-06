# 🏷️ Price Optimization Tool – Backend

This is the **backend service** for the *Price Optimization Tool*, a web application that helps businesses analyze demand forecasts and determine optimized product pricing strategies.

The backend exposes a secure and scalable REST API built with **Django**, **Django REST Framework**, and **django-filters**, supporting product management, demand forecasting, and price optimization.

For the frontend part of this project, see the [Price Optimization Tool Frontend](https://github.com/shahsad-kp/price-optimization-tool-frontend/README.md).

---

## 🚀 Features

- **User Authentication & Authorization**
  - Role-based access (Admin, Buyer, Supplier, etc.)
  - Secure JWT-based authentication with email verification.

- **Product Management**
  - CRUD APIs for products.
  - Product fields include: name, category, cost price, selling price, description, stock, and units sold.
  - Advanced filtering and search with `django-filters`.

- **Demand Forecast Integration**
  - Provides endpoints to fetch demand data and forecast visualizations.

- **Price Optimization**
  - Returns optimized pricing recommendations based on business rules or ML model integration.

- **Robust API Design**
  - RESTful endpoints with pagination and validation.
  - JSON responses suitable for React frontend.

---

## 🧰 Tech Stack

- **Backend Framework:** Django 5+, Django REST Framework  
- **Filtering & Querying:** django-filters  
- **Database:** PostgreSQL  
- **Auth:** JWT (via `djangorestframework-simplejwt`)  
- **Environment Management:** django-environ  

---

## ⚙️ How to Run

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/price-optimization-tool.git
cd price-optimization-tool/backend
```
### 2️⃣ Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 3️⃣ Configure Environment
```.dotenv
DEBUG=True
POSTGRES_DATABASE=abcd
POSTGRES_USER=price-optimization
POSTGRES_PASSWORD=admin
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
SECRET_KEY='django-insecure-31!&9xa8u0&!@=bs7@(p!8qxi=q$7k_9n#_n91)gag+&tv=ltc'
CORS_ALLOWED_ORIGINS=http://localhost:5173
```
### 4️⃣ Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### 5️⃣ Run Server
```bash
python manage.py runserver
```

The backend will start at http://127.0.0.1:8000/
To connect with frontend, ensure CORS and API URL are configured properly.