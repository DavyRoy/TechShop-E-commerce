output "service_name" {
  value = kubernetes_service.postgresql.metadata[0].name
}

output "connection_string" {
  value = "postgres://${var.name}.${var.namespace}.svc.cluster.local:5432/${var.db_name}"
}