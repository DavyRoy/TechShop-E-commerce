output "service_name" {
  value = var.create_service ? kubernetes_service.service[0].metadata[0].name : null
}

output "deployment_name" {
  value = kubernetes_deployment.deployment.metadata[0].name
}