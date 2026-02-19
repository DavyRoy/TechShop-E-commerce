#!/bin/bash

# Переменные
IMAGE_NAME="techshop"
TAG="v1.0"

# Информативное сообщение
echo "🔨 Building Docker image..."

# Сборка образа
docker build -t ${IMAGE_NAME}:${TAG} .

# Проверка успеха (опционально)
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed!"
    exit 1
fi