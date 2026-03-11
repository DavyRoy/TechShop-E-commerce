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