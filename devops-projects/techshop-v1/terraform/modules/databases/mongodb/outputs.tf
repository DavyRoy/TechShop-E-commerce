output "service_name" {
  value = kubernetes_service.mongodb.metadata[0].name
}

output "connection_string" {
  value = "mongodb://${var.name}.${var.namespace}.svc.cluster.local:27017/${var.db_name}"
}