variable "region" {
  description = "AWS region"
  default     = "ap-south-1"
}

variable "project_name" {
  description = "Project name for resource naming"
  default     = "ecommerce-microservices"
}

variable "public_key_path" {
  description = "Path to your public SSH key"
  default     = "./ecommerce-microservices-key.pub"
}
