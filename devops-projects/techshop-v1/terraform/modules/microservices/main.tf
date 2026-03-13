# ConfigMap для env переменных
resource "kubernetes_config_map" "env" {
  metadata {
    name      = var.name
    namespace = var.namespace
  }
  data = var.env_vars
}

# Secret для чувствительных переменных
resource "kubernetes_secret" "secret" {
  metadata {
    name      = "${var.name}-secret"
    namespace = var.namespace
  }
  data = var.secret_vars  # уже base64
}

# Deployment
resource "kubernetes_deployment" "deployment" {
  metadata {
    name      = var.name
    namespace = var.namespace
    labels    = { app = var.name }
  }

  spec {
    replicas = var.replicas

    selector {
      match_labels = { app = var.name }
    }

    template {
      metadata {
        labels = { app = var.name }
      }

      spec {
        container {
          name  = var.name
          image = var.image
          image_pull_policy = "Never"

          port {
            container_port = var.port
          }

          # Env из ConfigMap
          env_from {
            config_map_ref {
              name = kubernetes_config_map.env.metadata[0].name
            }
          }

          # Env из Secret
          env_from {
            secret_ref {
              name = kubernetes_secret.secret.metadata[0].name
            }
          }

          # Resource limits
          resources {
            requests = { cpu = var.resources.requests_cpu, memory = var.resources.requests_memory }
            limits   = { cpu = var.resources.limits_cpu,   memory = var.resources.limits_memory }
          }

          # Liveness probe — жив ли контейнер?
          liveness_probe {
            http_get {
              path = var.health_path
              port = var.port
            }
            initial_delay_seconds = 15
            period_seconds        = 20
          }

          # Readiness probe — готов ли принимать трафик?
          readiness_probe {
            http_get {
              path = var.health_path
              port = var.port
            }
            initial_delay_seconds = 5
            period_seconds        = 10
          }
        }
      }
    }
  }
}

# Service (ClusterIP) — только если create_service = true
resource "kubernetes_service" "service" {
  count = var.create_service ? 1 : 0

  metadata {
    name      = var.name
    namespace = var.namespace
  }

  spec {
    selector = { app = var.name }
    port {
      port        = var.port
      target_port = var.port
    }
    type = "ClusterIP"
  }
}