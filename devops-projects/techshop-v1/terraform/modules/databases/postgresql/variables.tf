variable "namespace" {
    description = "techshop-micro-service"
    type        = string
    default     = "techshop-micro-service"
}

variable "name" {
    description = "postgres"
    type        = string
    default     = "postgres"
}

variable "db_name" {
    description = "techshop"
    type        = string
    default     = "techshop"
}

variable "db_user" {
    description = "postgres"
    type        = string
    default     = "postgres"
}

variable "db_password" {
    description = "password"
    type        = string
    default     = "password"
}

variable "storage_size" {
    description = "2Gi"
    type        = string
    default     = "2Gi"
}

variable "image" {
    description = "postgres:15-alpine"
    type        = string
    default     = "postgres:15-alpine"
}
