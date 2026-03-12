output "service_name" {
  value = kubernetes_service.kafka.metadata[0].name
}

output "connection_string" {
  value = "kafka://${var.kafka_name}.${var.namespace}.svc.cluster.local:9092/"
}