#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}🚀 Health-Check Script${NC}"
echo "======================="

if [ "$1" == "--help" ]; then
    echo "Check health of a specific service or all services if no argument is provided."
    echo "Run './scripts/health-check.sh' to check a specific service."
    exit 0
fi

if curl -s -o /dev/null -w "%{http_code}" http://localhost:8081/ | grep -q "200"; then
    echo -e "   ${GREEN}✅${NC} Frontend is healthy"
else
    echo -e "   ${RED}❌${NC} Frontend is not responding"
fi

if curl -s -o /dev/null -w "%{http_code}" http://localhost:5010/api/health | grep -q "200"; then
    echo -e "   ${GREEN}✅${NC} Backend is healthy"
else
    echo -e "   ${RED}❌${NC} Backend is not responding"
fi

if curl -s -o /dev/null -w "%{http_code}" http://localhost:9090 | grep -q "200"; then
    echo -e "   ${GREEN}✅${NC} Prometheus is healthy"
else
    echo -e "   ${RED}❌${NC} Prometheus is not responding"
fi

if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; then
    echo -e "   ${GREEN}✅${NC} Grafana is healthy"
else
    echo -e "   ${RED}❌${NC} Grafana is not responding"
fi