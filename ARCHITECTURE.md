# Architecture Documentation

## System Overview

TechShop is built using a microservices architecture with the following components:

### High-Level Architecture
```
                                    Internet
                                       │
                                       ▼
                            ┌──────────────────┐
                            │   Nginx:80       │
                            │  (Reverse Proxy) │
                            └─────────┬────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
                    ▼                 ▼                 ▼
            Static Files          /api/*          Health Check
                    │                 │
                    │                 ▼
                    │        ┌────────────────┐
                    │        │  Flask API     │
                    │        │  (Gunicorn)    │
                    │        └────────┬───────┘
                    │                 │
                    │                 ▼
                    │        ┌────────────────┐
                    │        │  PostgreSQL    │
                    │        │  (Database)    │
                    │        └────────────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │   Monitoring Stack   │
         │                      │
         │  Prometheus  ────▶   │
         │  Node Exporter       │
         │  Grafana             │
         └──────────────────────┘
```

## Component Details

### Frontend (Nginx)

**Purpose:** Static file serving and reverse proxy

**Configuration:**
- Port: 80 (internal), 8081 (external)
- Serves static HTML/CSS/JS from `/usr/share/nginx/html/`
- Proxies `/api/*` requests to backend
- CORS headers configured
- Gzip compression enabled

**Key Files:**
- `frontend/nginx/nginx.conf` - Nginx configuration
- `frontend/src/` - Static files

### Backend (Flask API)

**Purpose:** REST API for business logic

**Configuration:**
- Port: 5000
- WSGI Server: Gunicorn (4 workers)
- ORM: SQLAlchemy
- Database: PostgreSQL

**Endpoints:**
- Health check
- Product CRUD operations
- Category management
- Order processing

**Key Files:**
- `backend/app/routes.py` - API endpoints
- `backend/app/models.py` - Database models
- `backend/wsgi.py` - Application entry point

### Database (PostgreSQL)

**Purpose:** Data persistence

**Configuration:**
- Port: 5432
- Version: 16-alpine
- Persistent volume: `postgres-data`

**Schema:**
- `categories` - Product categories
- `products` - Product catalog
- `orders` - Customer orders
- `order_items` - Order line items

### Monitoring

#### Prometheus

**Purpose:** Metrics collection and storage

**Configuration:**
- Port: 9090
- Scrape interval: 15s
- Targets: Flask API, Node Exporter

**Metrics Collected:**
- HTTP request rate
- Request duration
- System resources (CPU, memory)

#### Grafana

**Purpose:** Metrics visualization

**Configuration:**
- Port: 3000
- Default credentials: admin/admin
- Pre-configured datasource: Prometheus
- Pre-loaded dashboard: TechShop Monitoring

#### Node Exporter

**Purpose:** System metrics

**Configuration:**
- Port: 9100
- Exports: CPU, memory, disk, network metrics

## Data Flow

### Product Listing Flow
```
User Request
    ↓
Nginx (port 80)
    ↓
Static HTML/JS served
    ↓
JavaScript fetch to /api/products
    ↓
Nginx proxies to Backend
    ↓
Flask API (port 5000)
    ↓
SQLAlchemy query to PostgreSQL
    ↓
Database returns data
    ↓
Flask formats JSON response
    ↓
Nginx returns to client
    ↓
JavaScript renders products
```

### Order Creation Flow
```
User submits order
    ↓
POST /api/orders
    ↓
Flask validates request
    ↓
Begin database transaction
    ↓
Create order record
    ↓
Create order_items records
    ↓
Commit transaction
    ↓
Return order_id
```

## Security Considerations

1. **Database Credentials:** Stored in `.env`, not in code
2. **Non-root User:** Backend runs as non-root user
3. **CORS:** Configured to allow frontend origin
4. **Input Validation:** All API inputs validated
5. **SQL Injection:** Protected by SQLAlchemy ORM
6. **Secrets Management:** Environment variables, not hardcoded

## Scalability Considerations

### Current State (Single Node)
- Single instance of each service
- Suitable for development and small production loads

### Future Enhancements
- **Load Balancing:** Multiple backend instances behind Nginx
- **Database Replication:** Read replicas for scaling reads
- **Caching:** Redis for frequently accessed data
- **CDN:** Static assets served via CDN
- **Container Orchestration:** Kubernetes for multi-node deployment

## CI/CD Pipeline
```
Code Push to GitHub
    ↓
GitHub Actions Triggered
    ↓
┌───────────────────────┐
│  Backend Linting      │
│  (flake8)             │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│  Backend Tests        │
│  (pytest + coverage)  │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│  Docker Compose       │
│  Validation           │
└───────────┬───────────┘
            ↓
┌───────────────────────┐
│  Build Docker Images  │
│  (frontend + backend) │
└───────────┬───────────┘
            ↓
        Success ✅
```

## Monitoring & Observability

### Metrics Collection
- Prometheus scrapes metrics every 15s
- Flask exports HTTP metrics via `/metrics` endpoint
- Node Exporter provides system metrics

### Visualization
- Grafana dashboards show real-time metrics
- Pre-configured dashboard: "TechShop Monitoring"

### Alerting (Future)
- Prometheus Alertmanager
- Alerts for:
  - High error rate
  - Slow response times
  - Service downtime
  - Resource exhaustion

## Deployment Strategy

### Current: Manual Deployment
```bash
./scripts/deploy.sh
```

### Future: Automated Deployment
- Git tag triggers deployment
- Blue-green deployment
- Automated rollback on health check failure