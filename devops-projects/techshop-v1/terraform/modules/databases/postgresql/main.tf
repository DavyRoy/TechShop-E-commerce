# Secret для credentials
resource "kubernetes_secret" "postgresql" {
  metadata {
    name      = "${var.name}-secret"
    namespace = var.namespace
  }
  data = {
    POSTGRES_DB       = base64encode(var.db_name)
    POSTGRES_USER     = base64encode(var.db_user)
    POSTGRES_PASSWORD = base64encode(var.db_password)
  }
}

# PVC — хранилище
resource "kubernetes_persistent_volume_claim" "postgresql" {
  metadata {
    name      = "${var.name}-pvc"
    namespace = var.namespace
  }
  spec {
    access_modes = ["ReadWriteOnce"]
    resources {
      requests = {
        storage = var.storage_size
      }
    }
  }
}

# StatefulSet
resource "kubernetes_stateful_set" "postgresql" {
    metadata {
        name        = var.name
        namespace   = var.namespace
    }
    spec {
        service_name = var.name
        replicas     = 1
        selector {
            match_labels = {
                app = var.name
            }
        }
        template {
            metadata {
                labels = {
                    app = var.name
                }
            }
            spec {
                container {
                    name  = "postgresql"
                    image = var.image
                    resources {
                      requests = {
                        cpu = "200m"
                        memory = "256Mi"
                      }
                      limits = {
                        cpu = "500m"
                        memory = "512Mi"
                      }
                    }
                    port {
                        container_port = 5432
                    }
                    env {
                        name = "POSTGRES_DB"
                        value = var.db_name
                    } 
                    env {
                        name = "POSTGRES_USER"
                        value = var.db_user
                    }
                    env {
                        name = "POSTGRES_PASSWORD"
                        value = var.db_password
                    }
                    volume_mount {
                        name      = "data"
                        mount_path = "/var/lib/postgresql/data"
                    }
                }
                volume {
                    name = "data"
                    persistent_volume_claim {
                        claim_name = kubernetes_persistent_volume_claim.postgresql.metadata[0].name
                    }
                }
            }
        }
    }
}

# Service — точка доступа к Postgresql внутри кластера
resource "kubernetes_service" "postgresql" {
    metadata {
        name        = var.name
        namespace   = var.namespace
    }
    spec {
        type = "ClusterIP"
        selector = {
            app = var.name
        }
        port {
            port = 5432
            target_port = 5432
        }
    }
}