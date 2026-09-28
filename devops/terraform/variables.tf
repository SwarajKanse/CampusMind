variable "app_name" {
  description = "Application name"
  type        = string
  default     = "CampusMind"
}

variable "port" {
  description = "Backend listening port"
  type        = number
  default     = 8000
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}

variable "groq_model" {
  description = "Groq model identifier"
  type        = string
  default     = "qwen/qwen3.8-27b"
}
