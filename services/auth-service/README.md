# Auth Service

The Auth Service is a Django-based microservice responsible for user authentication and management in the e-commerce backend. It handles user registration, login, JWT token generation/refresh, and integrates with PostgreSQL for data persistence.

---

## Features
- **User Registration**: Create new user accounts with email/password.
- **JWT Authentication**: Secure stateless authentication with access/refresh tokens.
- **Token Refresh**: Renew expired access tokens using refresh tokens.
- **Swagger Documentation**: Interactive API documentation.
- **PostgreSQL Integration**: Isolated database for user data.
- **Docker Support**: Containerized development/production environments.
- **Test Coverage**: Unit and integration tests for core functionality.

---

## Prerequisites
- Docker & Docker Compose
- Python 3.9+
- PostgreSQL client (for direct DB access)
- HTTP client (Postman/cURL) for API testing

---

## Installation

### 1. Clone Repository
```
git clone https://github.com/your-username/ecom-backend.git
cd ecom-backend/services/auth-service
```

### 2. Configure Environment
Create `.env` file:

### 3. Start Services
`docker compose up -d --build`

### 4. Run Migrations
`docker compose exec auth-service python manage.py migrate`

### 5. Create Superuser (Optional)
`docker compose exec auth-service python manage.py createsuperuser`

# API Endpoints

|Endpoint      | Method   | Path            | Description             |
---------------|----------|-----------------|-------------------------|
|Register User | POST     | `/api/register/`| Create new user account |
|Login         | POST     | `/api/login/`   | Generate JWT tokens     |
|Refresh Token | POST     | `/api/refresh/` | Get new access token    |

# Documentation

Interactive API documentation available at:
`http://localhost:8000/swagger/

# Testing

Run tests with coverage report:
```
docker compose exec auth-service python manage.py test users --verbosity=2
docker compose exec auth-service python manage.py coverage report
```

# Development

## Local Setup

## 1. **Create virtual environment**:
`python -m venv venv && . venv/bin/activate`

## 2. **Install dependencies**:
`pip install -r src/requirements.txt`

## 3. **Run server**:
`python src/manage.py runserver`

# Deployment

## Production
`docker compose -f docker-compose.prod.yml up --build -d`

## Kubernetes
See `infrastructure/kubernetes/` for deployment manifests.

## Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -m 'Add some feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open Pull Request
