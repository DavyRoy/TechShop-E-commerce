#!/bin/bash

# Переменные
IMAGE_NAME="techshop"
TAG="v1"
CONTAINER_NAME="techshop-container"
HOST_PORT=8081
CONTAINER_PORT=80

# Проверить, существует ли контейнер
if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
    echo "🛑 Stopping existing container..."
    docker rm -f ${CONTAINER_NAME}
fi

# Запустить новый контейнер
echo "🚀 Starting new container..."
docker run -d \
    -p ${HOST_PORT}:${CONTAINER_PORT} \
    --name ${CONTAINER_NAME} \
    ${IMAGE_NAME}:${TAG}

# Проверка успеха
if [ $? -eq 0 ]; then
    echo "✅ Container started successfully!"
    echo "🌐 Access the site at: http://localhost:${HOST_PORT}"
else
    echo "❌ Failed to start container!"
    exit 1
fi