# DevOps Automation Scripts

Collection of Bash scripts for automating common DevOps tasks in the TechShop project.

## Prerequisites

- Docker and Docker Compose installed
- Project running or ready to run

## Available Scripts

### 📦 backup.sh

Creates a PostgreSQL database backup with timestamp.

**Usage:**
```bash
./scripts/backup.sh
```

**What it does:**
- Creates backup in `./backups/` directory
- Names file with timestamp: `backup_YYYYMMDD_HHMMSS.sql`
- Automatically removes backups older than 7 days
- Shows backup size

**Example output:**
```
🗄️  PostgreSQL Backup Script
==================================
Creating backup of database: techshop
✅ Backup created successfully!
   File: ./backups/backup_20260225_120000.sql
   Size: 15M
```

---

### 🚀 deploy.sh

Deploys the entire application stack.

**Usage:**
```bash
./scripts/deploy.sh
```

**What it does:**
- Stops all running containers
- Rebuilds Docker images from scratch
- Starts all containers
- Waits for services to initialize
- Checks health of all services

**Use when:**
- Deploying code changes
- After updating Dockerfiles
- Setting up environment from scratch

---

### 🧹 cleanup.sh

Cleans up unused Docker resources.

**Usage:**
```bash
./scripts/cleanup.sh
```

**What it does:**
- Removes stopped containers
- Removes unused images
- Removes unused volumes
- Clears build cache
- Shows disk space freed

**Warning:** This will remove ALL unused Docker resources, not just from this project!

---

### 🏥 health-check.sh

Checks health of all services.

**Usage:**
```bash
./scripts/health-check.sh
```

**What it does:**
- Checks if all containers are running
- Tests HTTP endpoints
- Returns exit code 0 if all OK, 1 if any failures

**Use in:**
- CI/CD pipelines
- Monitoring scripts
- After deployment

**Example output:**
```
🏥 Health Check for TechShop
==============================
✅ techshop-frontend is running
✅ techshop-backend is running
✅ techshop-postgres is running

Checking endpoints...
✅ Frontend is responding
✅ Backend API is responding
✅ Prometheus is responding
```

---

### 📋 logs.sh

View logs from services.

**Usage:**
```bash
# View last 100 lines from all services
./scripts/logs.sh

# View last 50 lines from backend
./scripts/logs.sh backend -n 50

# Follow backend logs in real-time
./scripts/logs.sh backend -f

# View specific number of lines
./scripts/logs.sh frontend -n 200
```

**Available services:**
- `frontend` - Nginx frontend
- `backend` - Flask API
- `postgres` - PostgreSQL database
- `prometheus` - Prometheus monitoring
- `grafana` - Grafana dashboards
- `all` - All services (default)

**Options:**
- `-f, --follow` - Follow log output in real-time
- `-n NUM` - Number of lines to show (default: 100)

---

## Quick Start

1. Make scripts executable:
```bash
chmod +x scripts/*.sh
```

2. Deploy the application:
```bash
./scripts/deploy.sh
```

3. Check health:
```bash
./scripts/health-check.sh
```

4. View logs:
```bash
./scripts/logs.sh backend -f
```

5. Create backup:
```bash
./scripts/backup.sh
```

---

## Tips

- Run `health-check.sh` after any deployment
- Create backups before major changes
- Use `logs.sh -f` to debug issues in real-time
- Run `cleanup.sh` periodically to free disk space

---

## Troubleshooting

**Backup fails:**
- Check that postgres container is running: `docker ps`
- Check container name matches: `CONTAINER_NAME` in backup.sh

**Deploy fails:**
- Check Docker is running: `docker info`
- Check logs: `./scripts/logs.sh all`
- Try manual cleanup: `./scripts/cleanup.sh`

**Health check fails:**
- Wait longer for services to start
- Check individual logs: `./scripts/logs.sh [service]`
- Check ports are not in use: `netstat -tulpn | grep LISTEN`
```

---

### 4. .gitignore (ИСПРАВЛЕННАЯ ВЕРСИЯ)
```
# Backups
backups/
*.sql

# Scripts logs
scripts/*.log