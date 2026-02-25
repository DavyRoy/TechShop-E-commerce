#!/bin/bash
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}🚀 Deployment Script${NC}"
echo "======================="

# 1. Stop containers
echo -e "\n${YELLOW}Step 1:${NC} Stopping containers..."
docker-compose down

# 2. Pull latest code (optional - uncomment if using git)
# echo -e "\n${YELLOW}Step 2:${NC} Pulling latest code..."
# git pull origin level-2-development

# 3. Build images
echo -e "\n${YELLOW}Step 2:${NC} Building Docker images..."
docker-compose build --no-cache

# 4. Start containers
echo -e "\n${YELLOW}Step 3:${NC} Starting containers..."
docker-compose up -d

# 5. Wait for services
echo -e "\n${YELLOW}Step 4:${NC} Waiting for services to start..."
sleep 15

# 6. Check health
echo -e "\n${YELLOW}Step 5:${NC} Checking service health..."

# Проверить что контейнеры запущены
CONTAINERS=("techshop-frontend" "techshop-backend" "techshop-postgres" "techshop-prometheus" "techshop-grafana")
ALL_RUNNING=true

for container in "${CONTAINERS[@]}"; do
    if docker ps --format '{{.Names}}' | grep -q "^${container}$"; then
        echo -e "   ${GREEN}✅${NC} $container is running"
    else
        echo -e "   ${RED}❌${NC} $container failed to start"
        ALL_RUNNING=false
    fi
done

if [ "$ALL_RUNNING" = true ]; then
    echo -e "\n${GREEN}✅ Deployment completed successfully!${NC}"
    echo ""
    echo "Services are available at:"
    echo "  Frontend:   http://localhost:8081"
    echo "  Backend:    http://localhost:5000"
    echo "  Prometheus: http://localhost:9090"
    echo "  Grafana:    http://localhost:3000"
else
    echo -e "\n${RED}❌ Deployment failed! Some containers didn't start.${NC}"
    echo "Run './scripts/logs.sh all' to check logs"
    exit 1
fi