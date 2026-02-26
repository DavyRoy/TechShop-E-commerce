# API Documentation

Base URL: `http://localhost:5000/api`

## Authentication

Currently no authentication required. Future versions will implement JWT authentication.

## Endpoints

### Health Check

#### GET /api/health

Check API health status.

**Response 200:**
```json
{
  "status": "ok"
}
```

---

### Categories

#### GET /api/categories

Get all product categories.

**Response 200:**
```json
[
  {
    "id": 1,
    "name": "Electronics",
    "description": "Electronic devices and accessories",
    "created_at": "2026-02-25T10:00:00",
    "updated_at": "2026-02-25T10:00:00"
  }
]
```

---

### Products

#### GET /api/products

Get paginated list of products.

**Query Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| page | integer | No | 1 | Page number |
| limit | integer | No | 10 | Items per page |

**Response 200:**
```json
{
  "products": [
    {
      "id": 1,
      "name": "MacBook Pro 13\"",
      "description": "Apple M1 chip, 8GB RAM, 256GB SSD",
      "price": 1299.99,
      "stock": 10,
      "category_id": 1,
      "url_image": null,
      "created_at": "2026-02-25T10:00:00",
      "updated_at": "2026-02-25T10:00:00"
    }
  ],
  "total": 21,
  "page": 1,
  "pages": 3,
  "limit": 10
}
```

---

#### GET /api/products/{id}

Get single product by ID.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| id | integer | Product ID |

**Response 200:**
```json
{
  "id": 1,
  "name": "MacBook Pro 13\"",
  "description": "Apple M1 chip, 8GB RAM, 256GB SSD",
  "price": 1299.99,
  "stock": 10,
  "category_id": 1,
  "url_image": null,
  "created_at": "2026-02-25T10:00:00",
  "updated_at": "2026-02-25T10:00:00"
}
```

**Response 404:**
```json
{
  "error": "Product not found"
}
```

---

#### GET /api/products/category/{category_id}

Get all products in a category.

**Path Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| category_id | integer | Category ID |

**Response 200:**
```json
[
  {
    "id": 1,
    "name": "MacBook Pro 13\"",
    "description": "Apple M1 chip",
    "price": 1299.99,
    "stock": 10,
    "category_id": 1
  }
]
```

---

### Orders

#### POST /api/orders

Create a new order.

**Request Body:**
```json
{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 3,
      "quantity": 1
    }
  ]
}
```

**Validation Rules:**
- `customer_name`: Required, string
- `customer_email`: Required, valid email format
- `items`: Required, array with at least 1 item
- `items[].product_id`: Required, must exist in database
- `items[].quantity`: Required, positive integer

**Response 201:**
```json
{
  "order_id": 123,
  "message": "Order created successfully"
}
```

**Response 400 - Missing fields:**
```json
{
  "error": "Missing required fields"
}
```

**Response 404 - Product not found:**
```json
{
  "error": "Product not found"
}
```

**Response 500 - Server error:**
```json
{
  "error": "Internal server error"
}
```

---

## Error Handling

All endpoints return appropriate HTTP status codes:

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error |

Error responses include JSON body:
```json
{
  "error": "Description of the error"
}
```

---

## Rate Limiting

Currently no rate limiting implemented. Future versions will implement:
- 100 requests per minute per IP
- 1000 requests per hour per IP

---

## Examples

### Get products with pagination
```bash
curl "http://localhost:5000/api/products?page=2&limit=5"
```

### Create an order
```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "Jane Smith",
    "customer_email": "jane@example.com",
    "items": [
      {"product_id": 1, "quantity": 1},
      {"product_id": 2, "quantity": 3}
    ]
  }'
```

### Get product by ID
```bash
curl http://localhost:5000/api/products/5
```