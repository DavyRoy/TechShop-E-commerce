#!/bin/bash
set -e  # Exit on error

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Конфигурация
BACKUP_DIR="./backups"
CONTAINER_NAME="techshop-postgres"
DB_NAME="techshop"
DB_USER="sergey"

echo -e "${YELLOW}🗄️  PostgreSQL Backup Script${NC}"
echo "=================================="

# Создать папку для бэкапов
mkdir -p "$BACKUP_DIR"

# Создать бэкап
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/backup_${TIMESTAMP}.sql"

echo "Creating backup of database: $DB_NAME"
echo "Container: $CONTAINER_NAME"

# ✅ ДОБАВЬ ЭТУ КОМАНДУ
docker exec $CONTAINER_NAME pg_dump -U $DB_USER $DB_NAME > "$BACKUP_FILE"

# Проверить что бэкап создан
if [ -f "$BACKUP_FILE" ]; then
    BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo -e "${GREEN}✅ Backup created successfully!${NC}"
    echo "   File: $BACKUP_FILE"
    echo "   Size: $BACKUP_SIZE"
else
    echo -e "${RED}❌ Backup failed!${NC}"
    exit 1
fi

# Удалить старые бэкапы (старше 7 дней)
echo "Cleaning up old backups (older than 7 days)..."
DELETED=$(find "$BACKUP_DIR" -name "backup_*.sql" -mtime +7 -delete -print | wc -l)
echo "Deleted $DELETED old backup(s)"

echo -e "${GREEN}✅ Backup complete!${NC}"