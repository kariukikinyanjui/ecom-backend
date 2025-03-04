# Review Service
The Review Service manages product reviews and ratings, enabling users to leave feedback and view products analytics. It integrates with auth-service for authentication and product-service for product validation.

---

## Features
- **Review Management**: CRUD operations for product reviews
- **Nested Comments**: Hierarchical comment system
- **Rating Validation**: 1-5 start rating system with constraints
- **Analytics**: Product rating statistics and distributions
- **JWT Authentication**: Secure endpoints via auth-service
- **Swagger Documenation**: Interactive API exploration
- **Prometheus Metrics**: Monitor request rates and performace

---

## Prerequisites
- Docker & Docker Compose
- Python 3.11+
- PostgreSQL 15+
- Running instances of:
    - Auth-Service (JWT provider)
    - Product-Service (product validation)

---

## Installation

### Docker Setup
```
git clone https://github.com/your-username/ecom-backend.git
cd ecom-backend/services/review-service
```

# Start services
`docker compose up -d --build`

# Run migrations
`docker compose exec review-service python manage.py migrate`

## Local Development
`python -m venv evn`
`. env/bin/activate`

`pip install - r src/requirements.txt`
`python src/manage.py runserver`

# API Documentation

## Interactive Docs

**Access Swagger UI at**: `http://localhost:8004/swagger/`

## Key Endpoints

| Endpoint                                       | Method     | Description       | Auth Required|
|------------------------------------------------|------------|-------------------|--------------|
|`/products/{id}/reviews/`                       | POST       | Create review     | Yes          |
|`/products/{id}/reviews/`                       | GET        | Listing reviews   | No           |
|`/products/{id}/analytics/`                     | GET        | Get rating stats  | No           |
|`/products/{id}/reviews/{review_id}/comments/`  | POST       | Add comment       | Yes          |

## Contributing

1. Fork the repository
2. Creature feature branch (`git checkout -b feature/awesome-feature`)
3. Commit changes (`git commit -m 'Add awesome feature'`)
4. Push to branch(`git push origin feature/awesome-feature`)
5. Open Pull Request
