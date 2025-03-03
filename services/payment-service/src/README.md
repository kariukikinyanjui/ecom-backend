# Payment Service

The Payment Service handles payment processing for the e-commerce platform, integrating with Stripe for secure transactions. It manages payment creating, refunds, and real-time status updates via webhooks while maintaining sychronization with the order-service.

---

## Features
- **Stripe Integration**: Process payments and refunds through Stripe
- **JWT Authentication**: Secure API endpoints with auth-service validation
- **Webhook Support**: Handle Stripe events for payment status updates
- **Idempotent Operation**: Prevent duplicate payments using unique keys
- **Swagger Documentation**: Interactive API testing and documentation
- **Prometheus Metrics**: Monitor payment success rates and performance

---

## Prerequisites
- Docker & Docker Compose
- Python 3.11+
- PostgreSQL 15+
- Stripe Developer Account([Sign Up](https://dashboard.stripe.com/register))
- Access to order-service and auth-service

---

## Installation

### Docker Setup
```
git clone https://github.com/your-username/ecom-backend.git
cd ecom-backend/services/payment-service
```

# Start services
`docker compose up -d --build`

# Run migrations
`docker compose exec payment-service python manage.py migrate

# Create test API keys (optional)
docker compose exec payment-service python manage.py createsamplekeys

```
python -m venv env
. env/bin/activate

pip install -r src/requirements.txt
python src/manage.py runserver
```

# API Documentation
## Interactive Docs

Access Swagger UI at: `http://localhost:8003/swagger/`

## Key Endpoints

| Endpoint                     | Method       | Description                   | Auth Required    |
|------------------------------|--------------|-------------------------------|------------------|
|`/payments/`                  | POST         | Create new payment            | JWT              |
|`/payments/{order_id}/`       | GET          | Get payment details           | JWT              |
|`/payments/{order_id}/refund/`| POST         | Initiate refund               | JWT              |
|`/webhook/stripe/`            | POST         | Stripe event webhook          | Stripe Signature |

## Contributing
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request
