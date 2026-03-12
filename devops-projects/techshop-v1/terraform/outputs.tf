output "namespace_names" {
    description = "techshop_micro_service"
    value       = kubernetes_namespace.techshop_micro_service.metadata[0].name
}

output "cluster_endpoint" {
    description = "techshop_micro_service"
    value       = "minikube"
}