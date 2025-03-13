# Product Service

The Product Service is a Django-based microservice responsible for managing product catalogs, categories, and inventory in the e-commerce backend. It features advanced search capabilities, bulk operations, and seamless integration with authentication services.

---

## Features
- **Product Management**: Full CRUD operations for products
- **Hierarchial Categories**: Nested category system with parent-child relationships
- **Full-Text Search**: PostgreSQL-powered search across product names/descriptions
- **Bulk Operations**: Create/update multiple products in single API calls
- **JWT Integration**: Secure endpoints with auth-service validation
- **Advanced Filtering**: Price ranges, stock levels, category filters
- **Monitoring**: Prometheus metrics endpoint at `/metrics`
- **Swagger Docs**: Interactive API documentation

---

## Prerequisites
- Docker & Docker Compose
- Python 3.9+
- PostgreSQL 15+
- HTTP client (curl/httpie/Postman)
- Access to auth-service for JWT validation

---

## Installation

### Docker Setup
```
git clone https://github.com/your-username/ecom-backend.git
cd ecom-backend/services/product-service
```

# Start services
`docker compose up -d --build`

# Run migrations
`docker compose exec product-service python manage.py migrate`

# Create test data (optional)
`docker compose exec product-service python manage.py createsampleproducts`

## Local Development
```
python -m venv venv
. env/bin/activate

pip install -r src/requirements.txt
python src/manage.py runserver
```

# API Documentation
Interactive Docs
Access Swagger UI at: `http://localhost:8001/swagger/`

## Key Endpoints

| Endpoint                      | Method    | Description                  | Auth Required|
|-------------------------------|-----------|------------------------------|--------------|
| `/products/`                  | GET       | List products with filtering | No           |
| `/products/`                  | POST      | Create new product           | Admin        |
| `/products/{id}/`             | PATCH     | Update product               | Admin        |
| `/products/search/?q={query}` | GET       | Full-text search             | No           |
| `/product/bulk/`              | POST      | Bulk create products         | Admin        |
| `/categories/`                | GET       | List categories              | No           |

## Testing
### Run Test Suite

```
docker compose exec product-service python manage.py test products --verbosity=2

docker compose exec product-service pytest products/ -v

docker compose exec product-service coverage run manage.py test products

docker compose exec product-service coverage report
```

# Monitoring
## Prometheus Metrics

Endpoint `http://localhost:8001/metrics`

Track key metrics:

- API request rates
- Database query performance
- Error rates
- Product inventory levels

# Service Integration
## Authentication Flow
1. Frontend obtain JWT from auth-service
2. Product-service validates token on protected endpoints

# Deployment
## Kubernetes

`kubectl apply -f infrastructure/kubernetes/

`docker compose -f docker-compose-prod.yml up --build -d

## Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request
