# Сurrency_api

## Overview
This project is a Django REST Framework-based API service that allows users to:
- Retrieve exchange rates for different currencies.
- Store and track exchange transactions.
- Maintain a balance system for transactions.
- Authenticate using JWT tokens.

## Features
- **User Registration:** Users can register and receive an initial balance of 1000 coins.
- **Balance Management:** Users can check their current balance.
- **Currency Exchange:** Users can retrieve and store transactions.
- **Transaction History:** Users can filter transaction history by currency and date.
- **Authentication:** JWT-based authentication ensures secure access to endpoints.

## Installation

### 1. Clone the Repository
```bash
git clone <repo_url>
cd project_folder
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add:
```ini
EXCHANGE_RATE_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
DEBUG=True
```

### 5. Apply Database Migrations
```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

## API Endpoints

### 1. **User Registration**
**POST /register/**
- Registers a new user with an initial balance of 1000 coins.

### 2. **User Balance**
**GET /balance/**
- Retrieves the current balance of an authenticated user.

### 3. **Currency Exchange**
**POST /currency/**
- Fetches exchange rates from an external API.
- Deducts balance if the request is successful.
- Stores the exchange rate data in the database.

### 4. **Transaction History**
**GET /history/**
- Retrieves the user's past exchange transactions.
- Supports filtering by currency and date.

## Authentication
- Uses JWT for secure authentication.
- Obtain a token:
```bash
POST /api/token/
{
  "username": "your_username",
  "password": "your_password"
}
```
- Use the token for authenticated requests:
```bash
Authorization: Bearer your_token
```

## Testing
Run unit tests with:
```bash
python manage.py test
