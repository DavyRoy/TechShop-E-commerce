
# --------------------
# ZooKeeper StatefulSet
# --------------------
resource "kubernetes_stateful_set" "zookeeper" {
  metadata {
    name      = var.zookeeper_name
    namespace = var.namespace
  }

  spec {
    service_name = var.zookeeper_name
    replicas     = 1

    selector {
      match_labels = {
        app = var.zookeeper_name
      }
    }

    template {
      metadata {
        labels = {
          app = var.zookeeper_name
        }
      }

      spec {
        init_container {
          name  = "init-myid"
          image = "busybox"
          command = [
            "sh",
            "-c",
            "mkdir -p /var/lib/zookeeper/data && echo 1 > /var/lib/zookeeper/data/myid"
          ]
          resources {
            requests = {
              cpu    = "200m"
              memory = "256Mi"
            }
            limits = {
              cpu    = "500m"
              memory = "512Mi"
            }
          }
          volume_mount {
            name       = "data"
            mount_path = "/var/lib/zookeeper/data"
          }
        }
        container {
          name  = "zookeeper"
          image = var.zookeeper_image
          resources {
            requests = {
              cpu    = "200m"
              memory = "256Mi"
            }
            limits = {
              cpu    = "500m"
              memory = "512Mi"
            }
          }

          port {
            container_port = 2181
          }
          port {
            container_port = 2888
          }
          port {
            container_port = 3888
          }

          env {
            name  = "ZOOKEEPER_CLIENT_PORT"
            value = "2181"
          }
          env {
            name  = "ZOOKEEPER_TICK_TIME"
            value = "2000"
          }

          volume_mount {
            name       = "data"
            mount_path = "/var/lib/zookeeper/data"
          }
        }

        volume {
          name = "data"
          empty_dir {}
        }
      }
    }
  }
}

############################
# Persistent Volume Claim
############################
resource "kubernetes_persistent_volume_claim" "kafka" {

  metadata {
    name      = "kafka-broker-pvc"
    namespace = var.namespace
  }

  spec {
    access_modes       = ["ReadWriteOnce"]
    storage_class_name = "standard"

    resources {
      requests = {
        storage = var.kafka_storage_size
      }
    }
  }
}

############################
# Kafka StatefulSet
############################
resource "kubernetes_stateful_set" "kafka" {

  depends_on = [
    kubernetes_stateful_set.zookeeper
  ]

  metadata {
    name      = "kafka-broker"
    namespace = var.namespace

    labels = {
      app = "kafka-broker"
    }
  }

  spec {

    service_name = "kafka-broker"
    replicas     = 1

    selector {
      match_labels = {
        app = "kafka-broker"
      }
    }

    template {

      metadata {
        labels = {
          app = "kafka-broker"
        }
      }

      spec {

        container {
          name  = "kafka-broker"
          image = "confluentinc/cp-kafka:7.5.0"

          port {
            container_port = 9092
          }

          ############################
          # ENV VARIABLES
          ############################

          env {
            name  = "KAFKA_BROKER_ID"
            value = "1"
          }

          env {
            name  = "KAFKA_ZOOKEEPER_CONNECT"
            value = "zookeeper:2181"
          }

          env {
            name  = "KAFKA_LISTENERS"
            value = "PLAINTEXT://0.0.0.0:9092"
          }

          env {
            name  = "KAFKA_ADVERTISED_LISTENERS"
            value = "PLAINTEXT://kafka-broker:9092"
          }

          env {
            name  = "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP"
            value = "PLAINTEXT:PLAINTEXT"
          }

          env {
            name  = "KAFKA_INTER_BROKER_LISTENER_NAME"
            value = "PLAINTEXT"
          }

          env {
            name  = "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR"
            value = "1"
          }

          env {
            name  = "KAFKA_TRANSACTION_STATE_LOG_MIN_ISR"
            value = "1"
          }

          env {
            name  = "KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR"
            value = "1"
          }

          env {
            name  = "KAFKA_HEAP_OPTS"
            value = "-Xmx512M -Xms256M"
          }

          env {
            name  = "KAFKA_LOG4J_LOGGERS"
            value = "kafka=WARN,kafka.controller=WARN,kafka.log.LogCleaner=WARN,state.change.logger=WARN,kafka.producer.async.DefaultEventHandler=WARN"
          }

          ############################
          # RESOURCES
          ############################

          resources {

            requests = {
              cpu    = "200m"
              memory = "512Mi"
            }

            limits = {
              cpu    = "500m"
              memory = "1Gi"
            }
          }

          ############################
          # STORAGE
          ############################

          volume_mount {
            name       = "kafka-storage"
            mount_path = "/var/lib/kafka/data"
          }
        }

        volume {
          name = "kafka-storage"

          persistent_volume_claim {
            claim_name = kubernetes_persistent_volume_claim.kafka.metadata[0].name
          }
        }
      }
    }
  }
}

# --------------------
# Services
# --------------------
resource "kubernetes_service" "zookeeper" {
  metadata {
    name      = var.zookeeper_name
    namespace = var.namespace
  }

  spec {
    cluster_ip = "None" # headless
    selector = {
      app = var.zookeeper_name
    }

    port {
      port = 2181
      name = "client"
    }
    port {
      port = 2888
      name = "quorum"
    }
    port {
      port = 3888
      name = "leader-election"
    }
  }
}

resource "kubernetes_service" "kafka" {
  metadata {
    name      = "kafka-broker"
    namespace = var.namespace
  }

  spec {
    selector = {
      app = var.kafka_name
    }

    port {
      port        = 9092
      target_port = 9092
    }
  }
}