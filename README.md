# Coder Backend

## Table of Contents

1. [What is Coder?](#what-is-coder)
2. [Prerequisites](#prerequisites)
3. [Setup](#setup)
4. [Running Tests](#running-tests)
5. [Authentication](#authentication)
6. [API Reference](#api-reference)
   - [Quick Overview](#quick-overview)
   - [Auth](#auth)
   - [Profiles](#profiles)
   - [Offers](#offers)
   - [Orders](#orders)
   - [Reviews](#reviews)
   - [Base Info](#base-info)
7. [Project Structure](#project-structure)

---

## What is Coder?

Coder is a freelancer marketplace REST API built with Django and Django REST Framework. Business users create service offers with three pricing tiers (basic, standard, premium). Customers browse those offers, place orders, and leave reviews.

---

## Prerequisites

- Python 3.11+
- pip
- Git

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Rohric/Coder.git
cd Coder/backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv env

# Windows
env\Scripts\activate

# macOS / Linux
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the template and fill in your values:

```bash
cp .env.template .env
```

`.env` reference:

```env
SECRET_KEY=<your-secret-key>
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

To generate a secure `SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. (Optional) Create a superuser

Required to access the Django admin panel and to delete orders via the API.

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000/api/`.

---

## Running Tests

```bash
pytest
```

---

## Authentication

Protected endpoints require a token in the `Authorization` header:

```
Authorization: Token <your-token>
```

You receive a token after registering or logging in.

---

## API Reference

### Quick Overview

| Method | Endpoint | Auth required | Role restriction |
|--------|----------|:---:|---|
| POST | `/api/registration/` | No | — |
| POST | `/api/login/` | No | — |
| POST | `/api/logout/` | Yes | — |
| GET | `/api/profile/` | Yes | — |
| PATCH | `/api/profile/` | Yes | — |
| GET | `/api/profile/<id>/` | Yes | — |
| PATCH | `/api/profile/<id>/` | Yes | Owner only |
| GET | `/api/profiles/business/` | Yes | — |
| GET | `/api/profiles/customer/` | Yes | — |
| GET | `/api/offers/` | No | — |
| POST | `/api/offers/` | Yes | Business |
| GET | `/api/offers/<id>/` | Yes | — |
| PATCH | `/api/offers/<id>/` | Yes | Owner only |
| DELETE | `/api/offers/<id>/` | Yes | Owner only |
| GET | `/api/offerdetails/<id>/` | Yes | — |
| GET | `/api/orders/` | Yes | — |
| POST | `/api/orders/` | Yes | Customer |
| PATCH | `/api/orders/<id>/` | Yes | Business (assigned) |
| DELETE | `/api/orders/<id>/` | Yes | Admin only |
| GET | `/api/order-count/<business_user_id>/` | Yes | — |
| GET | `/api/completed-order-count/<business_user_id>/` | Yes | — |
| GET | `/api/reviews/` | Yes | — |
| POST | `/api/reviews/` | Yes | Customer |
| PATCH | `/api/reviews/<id>/` | Yes | Author only |
| DELETE | `/api/reviews/<id>/` | Yes | Author only |
| GET | `/api/base-info/` | No | — |

---

### Auth

#### `POST /api/registration/`

Register a new user. A profile is created automatically.

**No authentication required.**

Request:
```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "Secret123!",
  "repeated_password": "Secret123!",
  "type": "customer"
}
```

`type` must be `"customer"` or `"business"`.

Response `201`:
```json
{
  "token": "abc123...",
  "username": "john",
  "email": "john@example.com",
  "user_id": 1
}
```

---

#### `POST /api/login/`

**No authentication required.**

Request:
```json
{
  "username": "john",
  "password": "Secret123!"
}
```

Response `200`:
```json
{
  "token": "abc123...",
  "username": "john",
  "email": "john@example.com",
  "user_id": 1
}
```

---

#### `POST /api/logout/`

Invalidates the current token.

**Authentication required.**

Response `200`:
```json
{ "detail": "Erfolgreich abgemeldet." }
```

---

#### `GET /api/profile/`

Returns the authenticated user's account data.

**Authentication required.**

Response `200`:
```json
{
  "user_id": 1,
  "username": "john",
  "email": "john@example.com",
  "type": "customer"
}
```

---

#### `PATCH /api/profile/`

Updates the authenticated user's account fields.

**Authentication required.**

Request (all fields optional):
```json
{
  "username": "john_updated",
  "email": "new@example.com"
}
```

Response `200`: Updated user object (same structure as GET).

---

### Profiles

#### `GET /api/profile/<id>/`

Returns the profile of the user with the given ID.

**Authentication required.**

Response `200`:
```json
{
  "user": 1,
  "username": "john",
  "email": "john@example.com",
  "type": "business",
  "first_name": "John",
  "last_name": "Doe",
  "file": "profile.jpg",
  "location": "Berlin",
  "tel": "0151...",
  "description": "...",
  "working_hours": "9-17",
  "created_at": "2024-01-01T00:00:00Z"
}
```

---

#### `PATCH /api/profile/<id>/`

Updates a profile. Only the profile owner is allowed.

**Authentication required.**

Request (all fields optional):
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "location": "Berlin",
  "tel": "0151...",
  "description": "...",
  "working_hours": "9-17",
  "file": "profile.jpg"
}
```

Response `200`: Updated profile object.

---

#### `GET /api/profiles/business/`

Returns a list of all business profiles.

**Authentication required.**

Response `200`: Array of profile objects (same structure as `GET /api/profile/<id>/`).

---

#### `GET /api/profiles/customer/`

Returns a list of all customer profiles.

**Authentication required.**

Response `200`:
```json
[
  {
    "user": 1,
    "username": "jane",
    "first_name": "Jane",
    "last_name": "Doe",
    "file": "profile.jpg",
    "uploaded_at": "2024-01-01T00:00:00Z",
    "type": "customer"
  }
]
```

---

### Offers

An offer consists of a base object and exactly **3 detail packages** (`basic`, `standard`, `premium`).

#### `GET /api/offers/`

Returns a paginated list of all offers.

**No authentication required.**

Query parameters:

| Parameter | Type | Description |
|---|---|---|
| `creator_id` | int | Filter by the offer creator |
| `min_price` | decimal | Filter by minimum package price |
| `max_delivery_time` | int | Filter by maximum delivery days |
| `ordering` | string | `updated_at` or `min_price` |
| `search` | string | Search in title and description |
| `page_size` | int | Items per page (default: 6) |

Response `200`:
```json
{
  "count": 10,
  "next": "http://...",
  "previous": null,
  "results": [
    {
      "id": 1,
      "user": 2,
      "title": "Logo Design",
      "description": "...",
      "image": null,
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z",
      "details": [
        { "id": 1, "url": "http://.../api/offerdetails/1/" },
        { "id": 2, "url": "http://.../api/offerdetails/2/" },
        { "id": 3, "url": "http://.../api/offerdetails/3/" }
      ],
      "min_price": "100.00",
      "min_delivery_time": 5,
      "user_details": {
        "first_name": "Max",
        "last_name": "Mustermann",
        "username": "max"
      }
    }
  ]
}
```

---

#### `POST /api/offers/`

Creates a new offer with exactly 3 detail packages.

**Authentication required. User must be of type `business`.**

Request:
```json
{
  "title": "Logo Design",
  "description": "Professional logo design service.",
  "details": [
    {
      "title": "Basic",
      "revisions": 2,
      "delivery_time_in_days": 5,
      "price": "100.00",
      "features": ["Logo Design"],
      "offer_type": "basic"
    },
    {
      "title": "Standard",
      "revisions": 5,
      "delivery_time_in_days": 7,
      "price": "200.00",
      "features": ["Logo Design", "Business Card"],
      "offer_type": "standard"
    },
    {
      "title": "Premium",
      "revisions": 10,
      "delivery_time_in_days": 10,
      "price": "500.00",
      "features": ["Logo Design", "Business Card", "Letterhead"],
      "offer_type": "premium"
    }
  ]
}
```

Response `201`: The created offer object.

---

#### `GET /api/offers/<id>/`

Returns a single offer by ID.

**Authentication required.**

Response `200`: Single offer object (same structure as list items).

---

#### `PATCH /api/offers/<id>/`

Updates an offer. Only the owner is allowed.

**Authentication required.**

Request (all fields optional):
```json
{
  "title": "Updated Title",
  "description": "Updated description.",
  "details": [
    {
      "offer_type": "basic",
      "price": "120.00"
    }
  ]
}
```

Packages are matched by `offer_type` — their IDs remain unchanged.

Response `200`: Updated offer object.

---

#### `DELETE /api/offers/<id>/`

Deletes an offer and all its detail packages. Only the owner is allowed.

**Authentication required.**

Response `204`: No content.

---

#### `GET /api/offerdetails/<id>/`

Returns a single offer detail package by ID.

**Authentication required.**

Response `200`:
```json
{
  "id": 1,
  "title": "Basic",
  "revisions": 2,
  "delivery_time_in_days": 5,
  "price": "100.00",
  "features": ["Logo Design"],
  "offer_type": "basic"
}
```

---

### Orders

#### `GET /api/orders/`

Returns all orders where the authenticated user is either the customer or the business.

**Authentication required.**

Response `200`:
```json
[
  {
    "id": 1,
    "customer_user": 3,
    "business_user": 2,
    "title": "Basic",
    "revisions": 2,
    "delivery_time_in_days": 5,
    "price": "100.00",
    "features": ["Logo Design"],
    "offer_type": "basic",
    "status": "in_progress",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

---

#### `POST /api/orders/`

Creates a new order from an offer detail package.

**Authentication required. User must be of type `customer`.**

Order data (title, price, features, etc.) is captured from the offer detail at the time of order and stored as a snapshot — changes to the original offer do not affect existing orders.

Request:
```json
{
  "offer_detail_id": 1
}
```

Response `201`: The created order object (same structure as GET).

---

#### `PATCH /api/orders/<id>/`

Updates the status of an order. Only the business user assigned to that order is allowed.

**Authentication required.**

Request:
```json
{
  "status": "completed"
}
```

Valid values: `in_progress`, `completed`, `cancelled`.

Response `200`: Updated order object.

---

#### `DELETE /api/orders/<id>/`

Deletes an order. Admin only (`is_staff=True`).

**Authentication required.**

Response `204`: No content.

---

#### `GET /api/order-count/<business_user_id>/`

Returns the number of active (`in_progress`) orders for a business user.

**Authentication required.**

Response `200`:
```json
{ "order_count": 3 }
```

---

#### `GET /api/completed-order-count/<business_user_id>/`

Returns the number of completed orders for a business user.

**Authentication required.**

Response `200`:
```json
{ "completed_order_count": 7 }
```

---

### Reviews

A customer can write **one review per business user**.

#### `GET /api/reviews/`

Returns a list of reviews.

**Authentication required.**

Query parameters:

| Parameter | Type | Description |
|---|---|---|
| `business_user_id` | int | Filter by reviewed business user |
| `reviewer_id` | int | Filter by reviewer |
| `ordering` | string | `rating`, `-rating`, `updated_at`, `-updated_at` |

Response `200`:
```json
[
  {
    "id": 1,
    "business_user": 2,
    "reviewer": 3,
    "rating": 5,
    "description": "Excellent service!",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

---

#### `POST /api/reviews/`

Creates a review. A customer can only review each business user once.

**Authentication required. User must be of type `customer`.**

Request:
```json
{
  "business_user": 2,
  "rating": 5,
  "description": "Excellent service!"
}
```

`rating` must be between `1` and `5`.

Response `201`: The created review object.

---

#### `PATCH /api/reviews/<id>/`

Updates a review. Only the review's author is allowed.

**Authentication required.**

Request (all fields optional):
```json
{
  "rating": 4,
  "description": "Very good service."
}
```

Response `200`: Updated review object.

---

#### `DELETE /api/reviews/<id>/`

Deletes a review. Only the review's author is allowed.

**Authentication required.**

Response `204`: No content.

---

### Base Info

#### `GET /api/base-info/`

Returns aggregated platform statistics. Intended for landing page use.

**No authentication required.**

Response `200`:
```json
{
  "review_count": 42,
  "average_rating": 4.3,
  "business_profile_count": 15,
  "offer_count": 38
}
```

---

## Project Structure

```
backend/
├── core/                   # Django project settings and root URLs
├── user_auth_app/          # Registration, login, logout, custom User model
├── profile_app/            # User profiles (customer & business)
├── offers_app/             # Offers and tiered detail packages
├── orders_app/             # Orders with snapshot data
├── review_app/             # Reviews and ratings
├── base_info_app/          # Platform statistics
└── manage.py
```
