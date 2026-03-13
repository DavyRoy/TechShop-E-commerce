# Namespace: techshop
resource "kubernetes_namespace" "techshop_micro_service" {
    metadata {
        name            = var.namespace_prefix
        labels = {
            environment = var.environment
            managed-by  = "terraform"
        }
    }
}  

# Namespace: monitoring
resource "kubernetes_namespace" "monitoring" {
    metadata {
        name            = "monitoring-micro-service"
        labels = {
            environment = var.environment
            managed-by  = "terraform"
        }
    }
}

# Namespace: logging
resource "kubernetes_namespace" "logging" {
    metadata {
        name            = "logging"
        labels = {
            environment = var.environment
            managed-by  = "terraform"
        }
    }
}

# Resource Quota for techshop-micro-service namespace
resource "kubernetes_resource_quota" "techshop_micro_service" {
    metadata {
        name                = "techshop-micro-service"
        namespace           = kubernetes_namespace.techshop_micro_service.metadata[0].name
    }
    spec {
        hard = {
            "requests.cpu"    = "4"
            "requests.memory" = "8Gi"
            "limits.cpu"      = "8"
            "limits.memory"   = "16Gi"
            "pods"            = "50"
        }
    }
}

# Network Policy for techshop-micro-service
resource "kubernetes_network_policy" "techshop_micro_service" {
  metadata {
    name      = "techshop-network-policy"
    namespace = kubernetes_namespace.techshop_micro_service.metadata[0].name
  }

  spec {

    pod_selector {}

    ingress {
      from {
        namespace_selector {
          match_labels = {
            "kubernetes.io/metadata.name" = var.namespace_prefix
          }
        }
      }
    }

    policy_types = ["Ingress"]
  }
}

resource "kubernetes_ingress_v1" "api_gateway" {
  metadata {
    name      = "api-gateway-ingress"
    namespace = kubernetes_namespace.techshop_micro_service.metadata[0].name
    annotations = {
      "kubernetes.io/ingress.class" = "nginx"
    }
  }

  spec {
    rule {
      host = "techshop.local"
      http {
        path {
          path      = "/"
          path_type = "Prefix"
          backend {
            service {
              name = module.api_gateway.service_name
              port { number = 8020 }
            }
          }
        }
      }
    }
  }
}

module "mongodb" {
  source    = "./modules/databases/mongodb"
  namespace = kubernetes_namespace.techshop_micro_service.metadata[0].name
  name      = "mongo"
  db_name   = "techshop"
}

module "postgres_users" {
  source      = "./modules/databases/postgresql"
  namespace   = kubernetes_namespace.techshop_micro_service.metadata[0].name
  name        = "postgres-users"
  db_name     = "techshop_users"
  db_password = "postgres"
}

module "postgres_orders" {
  source      = "./modules/databases/postgresql"
  namespace   = kubernetes_namespace.techshop_micro_service.metadata[0].name
  name        = "postgres-orders"
  db_name     = "techshop_orders"
  db_password = "postgres"
}

module "kafka" {
  source    = "./modules/kafka"
  namespace = kubernetes_namespace.techshop_micro_service.metadata[0].name
}

module "product_service" {
  source = "./modules/microservices"
  name = "product-service"
  namespace   = kubernetes_namespace.techshop_micro_service.metadata[0].name
  image = "docker.io/library/services-product-service:latest"
  port = 8080
  resources = {
    requests_cpu    = "50m"
    requests_memory = "64Mi"
    limits_cpu      = "200m"
    limits_memory   = "256Mi"
  }
  env_vars = {
    MONGODB_URI = "mongodb://mongo:27017/"
    MONGODB_DB  = "techshop"
    SERVER_PORT = "8080"
  }
}

module "user_service" {
  source = "./modules/microservices"
  name = "user-service"
  namespace   = kubernetes_namespace.techshop_micro_service.metadata[0].name
  image = "docker.io/library/services-user-service:latest"
  port = 5020
  resources = {
    requests_cpu    = "100m"
    requests_memory = "128Mi"
    limits_cpu      = "500m"
    limits_memory   = "512Mi"
  }
  env_vars = {
    POSTGRES_USER = "postgres"
    POSTGRES_DB = "techshop_user"
    POSTGRES_HOST = "postgres-user"
    POSTGRES_PORT = "5432"
  }
  secret_vars = {
    POSTGRES_PASSWORD = "postgres"
    JWT_SECRET_KEY = "secret"
  }
}

module "order_service" {
  source = "./modules/microservices"
  name = "order-service"
  namespace   = kubernetes_namespace.techshop_micro_service.metadata[0].name
  image = "docker.io/library/services-order-service:latest"
  port = 5030
  resources = {
    requests_cpu    = "100m"
    requests_memory = "128Mi"
    limits_cpu      = "500m"
    limits_memory   = "512Mi"
  }
  env_vars = {
    POSTGRES_USER = "postgres"
    POSTGRES_DB = "techshop_order"
    POSTGRES_HOST = "postgres-order"
    POSTGRES_PORT = "5432"
    KAFKA_BROKER = "kafka-broker:9092"
    PRODUCT_SERVICE_URL = "http://product-service:8080"
  }
  secret_vars = {
    POSTGRES_PASSWORD = "postgres"
    JWT_SECRET_KEY = "secret"
  }
}

module "notification_service" {
  source = "./modules/microservices"
  name = "notification-service"
  namespace   = kubernetes_namespace.techshop_micro_service.metadata[0].name
  image = "services-notification-service:latest"
  port = 5050
  resources = {
    requests_cpu    = "100m"
    requests_memory = "128Mi"
    limits_cpu      = "200m"
    limits_memory   = "512Mi"
  }
  env_vars = {
    KAFKA_BROKER = "kafka-broker:9092"
  }
  create_service = false
}

module "api_gateway" {
  source = "./modules/microservices"
  name = "api-gateway"
  namespace   = kubernetes_namespace.techshop_micro_service.metadata[0].name
  image = "docker.io/techshop/api-gateway:latest"
  port = 8020
  resources = {
    requests_cpu    = "50m"
    requests_memory = "64Mi"
    limits_cpu      = "200m"
    limits_memory   = "256Mi"
  }
  env_vars = {
    PRODUCT_SERVICE_URL = "http://product-service:8080"
    USER_SERVICE_URL = "http://user-service:5020"
    ORDER_SERVICE_URL = "http://order-service:5030"
  }
    secret_vars = {
    JWT_SECRET = "secret"
  }
}