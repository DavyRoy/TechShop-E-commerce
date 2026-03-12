variable "namespace" {
    description = "techshop-micro-service"
    type        = string
    default     = "techshop-micro-service"
}

variable "kafka_name" {
    description = "kafka_broker"
    type        = string
    default     = "kafka_broker"
}

variable "zookeeper_name" {
    description = "zookeeper"
    type        = string
    default     = "zookeeper"
}

variable "kafka_image" {
    description = "confluentinc/cp-kafka:7.5.0"
    type        = string
    default     = "confluentinc/cp-kafka:7.5.0"
}

variable "zookeeper_image" {
    description = "confluentinc/cp-zookeeper:7.5.0"
    type        = string
    default     = "confluentinc/cp-zookeeper:7.5.0"
}

variable "kafka_storage_size" {
  default = "10Gi"
}