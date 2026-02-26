#!/bin/bash
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}🚀 Test Script${NC}"
echo "======================="

if [ "$1" == "--help" ]; then
    echo "Run all tests for the TechShop application."
    echo "Usage: ./scripts/test.sh"
    exit 0
fi

# 1. cd backend
echo -e "\n${YELLOW}Step 1:${NC} cd backend..."
cd backend

# 2. Run tests
echo -e "\n${YELLOW}Step 2:${NC} Run tests..."
python -m pytest -v

# 3. Run test --cov
echo -e "\n${YELLOW}Step 3:${NC} Run test --cov..."
python -m pytest --cov=app

echo -e "\n${GREEN}✅ All tests passed successfully!${NC}"