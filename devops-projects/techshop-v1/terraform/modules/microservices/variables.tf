variable "name" {
  description = "название сервиса"
  type        = string
}

variable "namespace" {
  description = "kubernetes namespace"
  type        = string
}

variable "image" {
  description = "docker image"
  type        = string
}

variable "replicas" {
  description = "количество реплик"
  type        = number
  default     = 2
}

variable "port" {
  description = "порт контейнера"
  type        = number
}

variable "env_vars" {
  description = "не секретные env переменные"
  type        = map(string)
  default     = {}
}

variable "secret_vars" {
  description = "секретные env переменные"
  type        = map(string)
  default     = {}
  sensitive   = true
}

variable "resources" {
  description = "resource requests и limits"
  type = object({
    requests_cpu    = string
    requests_memory = string
    limits_cpu      = string
    limits_memory   = string
  })
}

variable "health_path" {
  description = "путь для health check"
  type        = string
  default     = "/health"
}

variable "create_service" {
  description = "создавать ли Service"
  type        = bool
  default     = true
}