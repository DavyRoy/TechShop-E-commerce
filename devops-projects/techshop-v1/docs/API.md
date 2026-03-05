# TechShop API Documentation

## Overview

Все запросы проходят через **API Gateway** (`http://techshop.local/api`).  
Прямые обращения к сервисам запрещены.

### Base URL
```
http://techshop.local/api
```

### Authentication

Большинство endpoints требуют JWT токен в заголовке:

```
Authorization: Bearer <access_token>
```

Токен получается через `POST /auth/login`.

---

## Error Handling

Все сервисы возвращают ошибки в едином формате:

```json
{
  "error": {
    "code": "PRODUCT_NOT_FOUND",
    "message": "Product with id '123' not found",
    "status": 404
  }
}
```

### Коды ошибок

| HTTP Status | Когда используется |
|-------------|-------------------|
| 400 | Невалидные входные данные |
| 401 | Отсутствует или невалидный JWT |
| 403 | Нет прав доступа |
| 404 | Ресурс не найден |
| 409 | Конфликт (например, email уже существует) |
| 422 | Бизнес-логика отклонила запрос |
| 500 | Внутренняя ошибка сервера |

---

## Authentication Flow (JWT)

```
1. POST /auth/register  → создать аккаунт
2. POST /auth/login     → получить access_token + refresh_token
3. GET  /products       → использовать access_token в заголовке
4. POST /auth/refresh   → обновить access_token через refresh_token
```

### Token lifetimes

| Token | TTL |
|-------|-----|
| access_token | 15 минут |
| refresh_token | 7 дней |

---

## 1. User Service

### POST /auth/register

Регистрация нового пользователя.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "John Doe"
}
```

**Response `201 Created`:**
```json
{
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-01-15T10:00:00Z"
  }
}
```

**Errors:**
- `409` — email уже зарегистрирован
- `400` — невалидный формат email или слабый пароль

---

### POST /auth/login

Вход в систему. Возвращает JWT токены.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response `200 OK`:**
```json
{
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "expires_in": 900
  }
}
```

**Errors:**
- `401` — неверный email или пароль

---

### POST /auth/refresh

Обновление access_token через refresh_token.

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response `200 OK`:**
```json
{
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "expires_in": 900
  }
}
```

**Errors:**
- `401` — refresh_token истёк или невалиден

---

### GET /auth/me

Информация о текущем пользователе. Требует JWT.

**Headers:** `Authorization: Bearer <access_token>`

**Response `200 OK`:**
```json
{
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-01-15T10:00:00Z"
  }
}
```

---

### GET /users/:id

Получение информации о пользователе по ID. Требует JWT.

**Response `200 OK`:**
```json
{
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

---

## 2. Product Service

### GET /products

Список товаров с пагинацией и фильтрами.

**Query params:**

| Param | Type | Description |
|-------|------|-------------|
| page | int | Номер страницы (default: 1) |
| limit | int | Кол-во на странице (default: 20, max: 100) |
| category | string | Фильтр по категории |
| search | string | Поиск по названию |

**Response `200 OK`:**
```json
{
  "data": [
    {
      "product_id": "prod_123",
      "name": "Laptop Pro 15",
      "category": "electronics",
      "price": 1299.99,
      "stock": 15,
      "description": "High performance laptop"
    }
  ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 150
  }
}
```

---

### GET /products/:id

Получение товара по ID.

**Response `200 OK`:**
```json
{
  "data": {
    "product_id": "prod_123",
    "name": "Laptop Pro 15",
    "category": "electronics",
    "price": 1299.99,
    "stock": 15,
    "description": "High performance laptop",
    "created_at": "2024-01-10T08:00:00Z"
  }
}
```

**Errors:**
- `404` — товар не найден

---

### POST /products

Создание нового товара. Требует JWT.

**Request:**
```json
{
  "name": "Laptop Pro 15",
  "category": "electronics",
  "price": 1299.99,
  "stock": 15,
  "description": "High performance laptop"
}
```

**Response `201 Created`:**
```json
{
  "data": {
    "product_id": "prod_123",
    "name": "Laptop Pro 15",
    "category": "electronics",
    "price": 1299.99,
    "stock": 15
  }
}
```

---

### PUT /products/:id

Обновление товара. Требует JWT.

**Request:**
```json
{
  "price": 1199.99,
  "stock": 20
}
```

**Response `200 OK`:**
```json
{
  "data": {
    "product_id": "prod_123",
    "name": "Laptop Pro 15",
    "price": 1199.99,
    "stock": 20
  }
}
```

---

### DELETE /products/:id

Удаление товара. Требует JWT.

**Response `204 No Content`**

---

### GET /products/health

Healthcheck Product Service.

**Response `200 OK`:**
```json
{
  "status": "ok",
  "service": "product-service",
  "database": "connected"
}
```

---

## 3. Order Service

### POST /orders

Создание заказа. Требует JWT.

Order Service автоматически запрашивает цену у Product Service и сохраняет её как `price_snapshot`.

**Request:**
```json
{
  "items": [
    {
      "product_id": "prod_123",
      "quantity": 2
    }
  ]
}
```

**Response `201 Created`:**
```json
{
  "data": {
    "order_id": "ord_456",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "items": [
      {
        "product_id": "prod_123",
        "quantity": 2,
        "price_snapshot": 1299.99
      }
    ],
    "total_amount": 2599.98,
    "status": "pending",
    "created_at": "2024-01-15T12:00:00Z"
  }
}
```

**Errors:**
- `422` — товар недоступен или нет на складе
- `404` — товар не найден в Product Service

---

### GET /orders/:id

Получение заказа по ID. Требует JWT.

**Response `200 OK`:**
```json
{
  "data": {
    "order_id": "ord_456",
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "items": [
      {
        "product_id": "prod_123",
        "quantity": 2,
        "price_snapshot": 1299.99
      }
    ],
    "total_amount": 2599.98,
    "status": "confirmed",
    "created_at": "2024-01-15T12:00:00Z"
  }
}
```

---

### GET /orders

Список заказов текущего пользователя. Требует JWT.

**Query params:**

| Param | Type | Description |
|-------|------|-------------|
| page | int | Номер страницы (default: 1) |
| limit | int | Кол-во на странице (default: 20) |
| status | string | Фильтр по статусу |

**Response `200 OK`:**
```json
{
  "data": [...],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 5
  }
}
```

---

### PUT /orders/:id/status

Обновление статуса заказа. Требует JWT.

**Request:**
```json
{
  "status": "confirmed"
}
```

**Допустимые статусы:** `pending` → `confirmed` → `shipped` → `delivered`  
**Отмена:** `pending` → `cancelled`

**Response `200 OK`:**
```json
{
  "data": {
    "order_id": "ord_456",
    "status": "confirmed",
    "updated_at": "2024-01-15T13:00:00Z"
  }
}
```

---

### DELETE /orders/:id

Отмена заказа. Требует JWT. Только заказы со статусом `pending`.

**Response `200 OK`:**
```json
{
  "data": {
    "order_id": "ord_456",
    "status": "cancelled",
    "cancelled_at": "2024-01-15T13:30:00Z"
  }
}
```

**Errors:**
- `422` — нельзя отменить заказ в статусе `shipped` или `delivered`

---

## 4. API Gateway

### GET /health

Общий healthcheck системы.

**Response `200 OK`:**
```json
{
  "status": "ok",
  "services": {
    "product-service": "ok",
    "order-service": "ok",
    "user-service": "ok"
  }
}
```

---

## 5. Routing Table

| Method | Path | Service | Auth |
|--------|------|---------|------|
| POST | /api/auth/register | user-service | ❌ |
| POST | /api/auth/login | user-service | ❌ |
| POST | /api/auth/refresh | user-service | ❌ |
| GET | /api/auth/me | user-service | ✅ |
| GET | /api/users/:id | user-service | ✅ |
| GET | /api/products | product-service | ❌ |
| GET | /api/products/:id | product-service | ❌ |
| POST | /api/products | product-service | ✅ |
| PUT | /api/products/:id | product-service | ✅ |
| DELETE | /api/products/:id | product-service | ✅ |
| POST | /api/orders | order-service | ✅ |
| GET | /api/orders | order-service | ✅ |
| GET | /api/orders/:id | order-service | ✅ |
| PUT | /api/orders/:id/status | order-service | ✅ |
| DELETE | /api/orders/:id | order-service | ✅ |
| GET | /health | api-gateway | ❌ |