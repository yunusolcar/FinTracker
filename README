# FinTrack - Financial Transaction Tracking Application

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Features](#features)
4. [API Endpoints](#api-endpoints)
5. [Installation](#installation)
6. [Docker Deployment](#docker-deployment)
7. [Authentication & Authorization](#authentication--authorization)
8. [Models](#models)
9. [Testing](#testing)
10. [Frontend Integration Notes](#frontend-integration-notes)

## Introduction

FinTrack is a financial transaction tracking RESTful API built with Django and Django Rest Framework. It helps users manage their finances by tracking expenses, income and budgets. The application provides robust API endpoints for creating, reading, updating, and deleting financial records.

## Project Structure

The application follows a modular structure and is organized into different apps:

```
fintrack/
├── apps/
│   ├── transactions/      # Core financial transactions functionality
│   │   ├── models.py      # Category, Transaction, Budget models
│   │   ├── serializers.py # JSON serialization
│   │   ├── views.py       # API viewsets
│   │   └── urls.py        # API routing
│   │
│   └── users/             # User management
│       ├── models.py      # Custom user model
│       ├── serializers.py # JSON serialization
│       ├── views.py       # Registration and user management views
│       └── urls.py        # API routing
│
├── fintrack/              # Project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── manage.py
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Features

1. **User Management**
   - User registration
   - Authentication with JWT tokens
   - Profile management

2. **Categories Management**
   - Create, read, update and delete categories
   - Each category is user-specific

3. **Transaction Management**
   - Track income and expenses
   - Categorize transactions
   - Filter and sort transactions
   - Support for recurring transactions

4. **Budget Planning**
   - Set budget limits for categories
   - Track budget status and spending
   - Get alerts when approaching budget limits

5. **Reporting**
   - Transaction summaries
   - Expense categorization
   - Recurring transaction analysis

## API Endpoints

### User Endpoints

```
POST /api/users/register/        # Create a new user account
POST /api/users/login/           # Obtain JWT tokens
POST /api/users/logout/          # Blacklist refresh token
GET/PUT /api/users/profile/      # Get or update user profile
POST /api/users/token/refresh/   # Refresh access token
```

### Transaction Endpoints

```
GET/POST /api/categories/                # List all categories or create a new one
GET/PUT/DELETE /api/categories/{id}/     # Retrieve, update or delete a category

GET/POST /api/transactions/              # List all transactions or create a new one
GET/PUT/DELETE /api/transactions/{id}/   # Retrieve, update or delete a transaction
GET /api/transactions/summary/           # Get transaction summary
GET /api/transactions/recurring_summary/ # Get recurring transactions summary

GET/POST /api/budgets/                   # List all budgets or create a new one
GET/PUT/DELETE /api/budgets/{id}/        # Retrieve, update or delete a budget
GET /api/budgets/{id}/status/            # Get budget status and spending
```

## Installation

### Requirements

- Python 3.11 or higher
- SQLite (default) or PostgreSQL

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd fintrack
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py migrate
```

5. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Docker Deployment

The application can be deployed using Docker:

1. Make sure Docker and Docker Compose are installed

2. Build and start the containers:
```bash
docker-compose up -d
```

3. The application will be available at http://localhost:8000

4. To stop the application:
```bash
docker-compose down
```

## Authentication & Authorization

The application uses JWT (JSON Web Tokens) for authentication:

- Access tokens expire after 30 minutes
- Refresh tokens expire after 1 day
- Refresh tokens are rotated and blacklisted after use
- Authentication uses the Bearer token scheme

Example authentication header:
```
Authorization: Bearer <access_token>
```

## Models

### User Model

The application uses a custom user model that uses email as the primary identifier:

- Email (unique)
- Username
- Password
- First Name (optional)
- Last Name (optional)

### Category Model

- Name (string)
- User (foreign key)
- Created At (timestamp)
- Updated At (timestamp)

### Transaction Model

- User (foreign key)
- Category (foreign key)
- Amount (decimal)
- Description (string)
- Transaction Type (income/expense)
- Date (date)
- Is Recurring (boolean)
- Recurring Type (none/weekly/monthly/yearly)
- Created At (timestamp)
- Updated At (timestamp)

### Budget Model

- User (foreign key)
- Category (foreign key)
- Amount (decimal)
- Start Date (date)
- End Date (date)
- Created At (timestamp)
- Updated At (timestamp)
