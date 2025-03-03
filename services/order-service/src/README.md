# Order Service Architecture

## Data Flow
1. User submits order via API
2. Service validate JWT with auth-service
3. For each product:
    - Verify existence via product-service
    - Check current price
    - Validate stock availability
4. Calculate total
5. Persist order with historical prices

### Failure Modes
- **Product Service Unavailable**: Retry 3 times with exponential backoff
- **Insufficient Stock**: Return 400 with detailed error
- **Price Mismatch**: Log discrepancy and use latest price

### Monitoring
- Track `order_created_total` metric
- Alert on `order_failure_rate > 5%`
