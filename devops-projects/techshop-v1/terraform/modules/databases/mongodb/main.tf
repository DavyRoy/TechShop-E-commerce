# PersistentVolumeClaim — хранилище для данных
resource "kubernetes_persistent_volume_claim" "mongodb" {
    metadata {
        name        = "${var.name}-pvc"
        namespace   = var.namespace
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

# StatefulSet — запускает MongoDB под
resource "kubernetes_stateful_set" "mongodb" {
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
                    name  = "mongodb"
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
                        container_port = 27017
                    }
                    env {
                        name = "MONGO_INITDB_DATABASE"
                        value = var.db_name
                    }
                    volume_mount {
                        name      = "data"
                        mount_path = "/data/db"
                    }
                }
                volume {
                    name = "data"
                    persistent_volume_claim {
                        claim_name = kubernetes_persistent_volume_claim.mongodb.metadata[0].name
                    }
                }
            }
        }
    }
}

# Service — точка доступа к MongoDB внутри кластера
resource "kubernetes_service" "mongodb" {
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
            port = 27017
            target_port = 27017
        }
    }
}