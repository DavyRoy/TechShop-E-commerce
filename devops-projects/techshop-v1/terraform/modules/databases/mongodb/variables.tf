variable "namespace" {
    description = "techshop-micro-service"
    type        = string
    default     = "techshop-micro-service"
}

variable "name" {
    description = "mongo"
    type        = string
    default     = "mongo"
}

variable "image" {
    description = "mongo:7"
    type        = string
    default     = "mongo:7"
}

variable "db_name" {
    description = "techshop"
    type        = string
    default     = "techshop"
}

variable "storage_size" {
    description = "1Gi"
    type        = string
    default     = "1Gi"
}
