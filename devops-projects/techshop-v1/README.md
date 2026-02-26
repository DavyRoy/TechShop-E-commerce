<div align="center">

# 🛒 TechShop E-commerce Platform

### Modern Full-Stack E-commerce with DevOps Best Practices

[![CI/CD Pipeline](https://img.shields.io/github/actions/workflow/status/DavyRoy/TechShop-E-commerce/main.yml?label=CI%2FCD&logo=github)](https://github.com/DavyRoy/TechShop-E-commerce/actions)
[![Coverage](https://img.shields.io/badge/coverage-89%25-brightgreen)](https://github.com/DavyRoy/TechShop-E-commerce)
[![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [API](#-api-reference) • [Monitoring](#-monitoring)


</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Project Levels](#-project-levels)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [API Reference](#-api-reference)
- [Monitoring & Observability](#-monitoring--observability)
- [Automation Scripts](#-automation-scripts)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)

---

## 🎯 Overview

**TechShop** is a comprehensive e-commerce platform built to demonstrate **modern DevOps practices** and **full-stack development skills**. The project progresses through multiple complexity levels, from static containerized websites to fully monitored microservices architectures.

### 🎓 Learning Objectives

This project demonstrates proficiency in:
- **Containerization** with Docker & Docker Compose
- **CI/CD** automation with GitHub Actions
- **Monitoring & Observability** using Prometheus & Grafana
- **Infrastructure as Code** principles
- **RESTful API** development with Flask
- **Database management** with PostgreSQL
- **Automated testing** with pytest (89% coverage)
- **DevOps scripting** and automation

---

## 📊 Project Levels

<table>
<tr>
<th>Level</th>
<th>Status</th>
<th>Description</th>
<th>Key Technologies</th>
</tr>
<tr>
<td><strong>Level 1</strong><br/>Beginner</td>
<td>✅ Complete</td>
<td>Static website with Nginx and Docker containerization</td>
<td>HTML/CSS, Nginx, Docker</td>
</tr>
<tr>
<td><strong>Level 2</strong><br/>Junior</td>
<td>✅ Complete</td>
<td>Full-stack app with backend API, database, monitoring, and CI/CD</td>
<td>Flask, PostgreSQL, Prometheus, Grafana, GitHub Actions</td>
</tr>
<tr>
<td><strong>Level 3</strong><br/>Junior+</td>
<td>🔜 Coming Soon</td>
<td>Advanced features: Redis caching, Elasticsearch, message queues</td>
<td>Redis, Elasticsearch, RabbitMQ/Kafka</td>
</tr>
<tr>
<td><strong>Level 4</strong><br/>Middle</td>
<td>📋 Planned</td>
<td>Kubernetes orchestration, service mesh, advanced monitoring</td>
<td>Kubernetes, Istio, Helm, ArgoCD</td>
</tr>
</table>

---

## 🏗️ Architecture

### Level 2 Architecture (Current)
```
                           ┌─────────────────────────┐
                           │    Internet Users       │
                           └───────────┬─────────────┘
                                       │
                          ┌────────────▼─────────────┐
                          │   Nginx:80 (Frontend)    │
                          │  Static Files + Proxy    │
                          └────────────┬─────────────┘
                                       │
                          ┌────────────▼─────────────┐
                          │   Flask API:5000         │
                          │   (REST Backend)         │
                          └────────────┬─────────────┘
                                       │
                          ┌────────────▼─────────────┐
                          │   PostgreSQL:5432        │
                          │   (Database)             │
                          └──────────────────────────┘

Monitoring Stack:
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│  Prometheus      │─────▶│    Grafana       │      │  Node Exporter   │
│  :9090           │      │    :3000         │      │  :9100           │
└──────────────────┘      └──────────────────┘      └──────────────────┘
```

### 🔧 Components

| Component | Technology | Port | Purpose |
|-----------|-----------|------|---------|
| **Frontend** | Nginx Alpine | 8081 | Static files + Reverse proxy |
| **Backend** | Flask + Gunicorn | 5010 | REST API with business logic |
| **Database** | PostgreSQL 16 | 5432 | Data persistence |
| **Monitoring** | Prometheus | 9090 | Metrics collection |
| **Visualization** | Grafana | 3000 | Dashboards and alerting |
| **System Metrics** | Node Exporter | 9100 | Host metrics collection |

---

## 🛠️ Tech Stack

<div align="center">

### Backend
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-red)

### Frontend
![Nginx](https://img.shields.io/badge/Nginx-1.25-009639?logo=nginx&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?logo=javascript&logoColor=black)

### DevOps & Infrastructure
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=githubactions&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?logo=prometheus&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-F46800?logo=grafana&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?logo=gnubash&logoColor=white)

### Testing & Quality
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?logo=pytest&logoColor=white)
![Coverage](https://img.shields.io/badge/Coverage-89%25-brightgreen)
![Flake8](https://img.shields.io/badge/Flake8-Linting-blue)

</div>

---

## ✨ Features

### 🛍️ E-commerce Features
- ✅ Product catalog with categories
- ✅ Advanced pagination and filtering
- ✅ Shopping cart functionality
- ✅ Order management system
- ✅ RESTful API architecture

### 🚀 DevOps Features
- ✅ **Containerized architecture** - Full Docker Compose orchestration
- ✅ **Automated CI/CD** - GitHub Actions pipeline with linting and testing
- ✅ **Comprehensive monitoring** - Prometheus + Grafana dashboards
- ✅ **High test coverage** - 89% code coverage with pytest
- ✅ **Automated backups** - PostgreSQL backup scripts
- ✅ **Health monitoring** - Automated health check scripts
- ✅ **Centralized logging** - Container log aggregation
- ✅ **Production-ready** - Gunicorn WSGI server with multiple workers

---

## 🚀 Quick Start

### Prerequisites

<table>
<tr>
<td>
<img src="https://www.docker.com/wp-content/uploads/2022/03/vertical-logo-monochromatic.png" width="50"/>
</td>
<td><strong>Docker</strong><br/>Version 20.10 or higher</td>
</tr>
<tr>
<td>
<img src="https://docs.docker.com/compose/images/logo.png" width="50"/>
</td>
<td><strong>Docker Compose</strong><br/>Version 2.0 or higher</td>
</tr>
<tr>
<td>📦</td>
<td><strong>Git</strong><br/>For cloning repository</td>
</tr>
</table>

### 🎬 Installation
```bash
# 1. Clone the repository
git clone https://github.com/DavyRoy/TechShop-E-commerce.git
cd TechShop-E-commerce

# 2. Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# 3. Start all services
docker-compose up -d

# 4. Verify deployment
./scripts/health-check.sh

# 5. Access the application
# Frontend:   http://localhost:8081
# Backend:    http://localhost:5010
# Prometheus: http://localhost:9090
# Grafana:    http://localhost:3000 (admin/admin)
```

### ⚡ Alternative Quick Start Scripts
```bash
# Using deployment script (recommended)
./scripts/deploy.sh

# Manual step-by-step
docker-compose build
docker-compose up -d
docker-compose ps
```

---

## 📚 API Reference

### Base URL
```
http://localhost:5010/api
```

### Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/categories` | List all categories |
| `GET` | `/api/products` | List products (paginated) |
| `GET` | `/api/products/{id}` | Get product by ID |
| `GET` | `/api/products/category/{id}` | Products by category |
| `POST` | `/api/orders` | Create new order |

### 📖 Detailed API Documentation

<details>
<summary><b>GET /api/health</b> - Health Check</summary>

**Response:**
```json
{
  "status": "ok"
}
```
</details>

<details>
<summary><b>GET /api/categories</b> - Get Categories</summary>

**Response:**
```json
[
  {
    "id": 1,
    "name": "Electronics",
    "description": "Electronic devices",
    "created_at": "2026-02-25T10:00:00",
    "updated_at": "2026-02-25T10:00:00"
  }
]
```
</details>

<details>
<summary><b>GET /api/products?page=1&limit=10</b> - Get Products</summary>

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10)

**Response:**
```json
{
  "products": [
    {
      "id": 1,
      "name": "MacBook Pro 13\"",
      "description": "Apple M1 chip, 8GB RAM",
      "price": 1299.99,
      "stock": 10,
      "category_id": 1
    }
  ],
  "total": 21,
  "page": 1,
  "pages": 3,
  "limit": 10
}
```
</details>

<details>
<summary><b>POST /api/orders</b> - Create Order</summary>

**Request Body:**
```json
{
  "customer_name": "John Doe",
  "customer_email": "john@example.com",
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ]
}
```

**Response (201):**
```json
{
  "order_id": 123,
  "message": "Order created successfully"
}
```
</details>

> 📘 **Full API Documentation**: See [docs/API.md](docs/API.md) for complete details

---

## 📊 Monitoring & Observability

### Prometheus Metrics

Access: **http://localhost:9090**

**Key Metrics:**
- `flask_http_request_total` - Total HTTP requests by endpoint and method
- `flask_http_request_duration_seconds` - Request latency histogram
- `node_cpu_seconds_total` - CPU usage metrics
- `node_memory_MemTotal_bytes` - Memory utilization

### Grafana Dashboards

Access: **http://localhost:3000** (admin/admin)

**Pre-configured Dashboards:**
1. **TechShop Monitoring**
   - HTTP request rate (requests/second)
   - Average response time
   - HTTP status code distribution
   - Total request counter

2. **System Resources** (via Node Exporter)
   - CPU usage
   - Memory utilization
   - Disk I/O
   - Network traffic

### Example Queries
```promql
# Request rate per second
rate(flask_http_request_total[5m])

# Average response time
rate(flask_http_request_duration_seconds_sum[5m]) / 
rate(flask_http_request_duration_seconds_count[5m])

# 95th percentile latency
histogram_quantile(0.95, flask_http_request_duration_seconds_bucket)
```

---

## 🔧 Automation Scripts

All automation scripts are located in `scripts/` directory.

| Script | Purpose | Usage |
|--------|---------|-------|
| **backup.sh** | Create PostgreSQL backup | `./scripts/backup.sh` |
| **deploy.sh** | Deploy entire stack | `./scripts/deploy.sh` |
| **health-check.sh** | Check service health | `./scripts/health-check.sh` |
| **logs.sh** | View container logs | `./scripts/logs.sh [service]` |
| **cleanup.sh** | Clean Docker resources | `./scripts/cleanup.sh` |

### Examples
```bash
# Create database backup
./scripts/backup.sh
# Output: ./backups/backup_20260225_143022.sql

# Deploy application with rebuild
./scripts/deploy.sh

# Check all services
./scripts/health-check.sh
# ✅ techshop-frontend is running
# ✅ techshop-backend is running
# ✅ Backend API is responding

# View backend logs (last 50 lines, follow mode)
./scripts/logs.sh backend -n 50 -f

# Clean unused Docker resources
./scripts/cleanup.sh
```

> 📘 **Script Documentation**: See [scripts/README.md](scripts/README.md)

---

## 💻 Development

### Local Setup
```bash
# 1. Create Python virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
export POSTGRES_USER=your_username
export POSTGRES_PASSWORD=your_password
export POSTGRES_DB=techshop
export POSTGRES_HOST=localhost
export SECRET_KEY=dev-secret-key

# 4. Run development server
python wsgi.py
```

### Project Structure
```
TechShop-E-commerce/
├── 📁 backend/                 # Flask REST API
│   ├── 📁 app/
│   │   ├── __init__.py        # App factory
│   │   ├── config.py          # Configuration
│   │   ├── models.py          # SQLAlchemy models
│   │   └── routes.py          # API endpoints
│   ├── 📁 tests/
│   │   ├── conftest.py        # Pytest fixtures
│   │   ├── test_api.py        # API tests
│   │   └── test_health.py     # Health tests
│   ├── wsgi.py                # WSGI entry point
│   ├── Dockerfile             # Backend container
│   ├── requirements.txt       # Python dependencies
│   └── pytest.ini             # Test configuration
│
├── 📁 frontend/                # Nginx frontend
│   ├── 📁 nginx/
│   │   └── nginx.conf         # Nginx config
│   ├── 📁 src/                # Static files
│   └── Dockerfile             # Frontend container
│
├── 📁 database/                # Database initialization
│   ├── schema.sql             # Table definitions
│   └── init.sql               # Seed data
│
├── 📁 monitoring/              # Monitoring stack
│   ├── 📁 prometheus/
│   │   └── prometheus.yml     # Prometheus config
│   └── 📁 grafana/
│       └── provisioning/      # Auto-provisioning
│
├── 📁 scripts/                 # Automation scripts
│   ├── backup.sh
│   ├── deploy.sh
│   ├── health-check.sh
│   ├── logs.sh
│   └── cleanup.sh
│
├── 📁 .github/
│   └── workflows/
│       └── main.yml           # CI/CD pipeline
│
├── docker-compose.yaml        # Orchestration
├── .env.example               # Environment template
└── README.md                  # This file
```

---

## 🧪 Testing

### Run Tests
```bash
cd backend

# Run all tests
pytest -v

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_api.py -v

# Run with HTML coverage report
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

### Test Coverage

**Current Coverage: 89%**

| Module | Coverage |
|--------|----------|
| app/__init__.py | 100% |
| app/config.py | 100% |
| app/models.py | 88% |
| app/routes.py | 86% |

### CI/CD Pipeline

GitHub Actions automatically runs on every push:
```yaml
✓ Linting (flake8)
✓ Unit Tests (pytest)
✓ Coverage Report
✓ Docker Compose Validation
✓ Docker Image Builds
```

**Pipeline Status**: [![CI/CD](https://github.com/DavyRoy/TechShop-E-commerce/actions/workflows/main.yml/badge.svg)](https://github.com/DavyRoy/TechShop-E-commerce/actions)

---

## 🚢 Deployment

### Production Deployment
```bash
# 1. Configure production environment
cp .env.example .env
# Edit .env with production values

# 2. Deploy with automated script
./scripts/deploy.sh

# 3. Verify deployment
./scripts/health-check.sh

# 4. Create initial backup
./scripts/backup.sh
```

### Backup Strategy
```bash
# Manual backup
./scripts/backup.sh

# Automated cleanup (backups older than 7 days deleted automatically)
# Backups saved to: ./backups/backup_YYYYMMDD_HHMMSS.sql
```

### Environment Variables

Required variables in `.env`:
```env
# Database
POSTGRES_USER=production_user
POSTGRES_PASSWORD=strong_password_here
POSTGRES_DB=techshop
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Application
SECRET_KEY=production-secret-key-change-this

# Grafana
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=secure_password_here
```

---

## 🐛 Troubleshooting

### Common Issues

<details>
<summary><b>Services not starting</b></summary>
```bash
# Check container status
docker ps -a

# View logs for specific service
./scripts/logs.sh backend

# Restart services
docker-compose restart

# Complete rebuild
docker-compose down
docker-compose up --build -d
```
</details>

<details>
<summary><b>Database connection errors</b></summary>
```bash
# Check PostgreSQL status
docker exec techshop-postgres pg_isready

# View database logs
./scripts/logs.sh postgres

# Verify environment variables
docker exec techshop-backend env | grep POSTGRES
```
</details>

<details>
<summary><b>Port already in use</b></summary>
```bash
# Find process using port 8081
lsof -i :8081

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yaml
```
</details>

<details>
<summary><b>Out of disk space</b></summary>
```bash
# Clean Docker resources
./scripts/cleanup.sh

# Remove old backups
rm -rf backups/*

# Check disk usage
docker system df
```
</details>

---

## 🗺️ Roadmap

### ✅ Completed (Level 1 & 2)
- [x] Static website with Nginx
- [x] Docker containerization
- [x] PostgreSQL database integration
- [x] Flask REST API
- [x] Prometheus monitoring
- [x] Grafana dashboards
- [x] GitHub Actions CI/CD
- [x] Automated testing (89% coverage)
- [x] Automation scripts

### 🚧 In Progress (Level 3)
- [ ] Redis caching layer
- [ ] Elasticsearch for product search
- [ ] Message queue (RabbitMQ/Kafka)
- [ ] Microservices refactoring
- [ ] API rate limiting
- [ ] JWT authentication

### 📋 Planned (Level 4)
- [ ] Kubernetes deployment
- [ ] Helm charts
- [ ] Service mesh (Istio)
- [ ] ArgoCD for GitOps
- [ ] Advanced monitoring (Jaeger tracing)
- [ ] Multi-region deployment

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Code Style

- Python: Follow PEP 8, use `flake8` for linting
- Max line length: 120 characters
- All tests must pass: `pytest -v`

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**DavyRoy** - DevOps Engineer in Training

- GitHub: [@DavyRoy](https://github.com/DavyRoy)
- Project Link: [TechShop-E-commerce](https://github.com/DavyRoy/TechShop-E-commerce)

---

## 🙏 Acknowledgments

- Built as part of comprehensive DevOps learning journey
- Inspired by modern e-commerce architectures
- Thanks to the open-source community for amazing tools

---

<div align="center">

### ⭐ If you found this project helpful, please give it a star!

**Made with ❤️ and ☕ by DavyRoy**

[⬆ Back to Top](#-techshop-e-commerce-platform)

</div>