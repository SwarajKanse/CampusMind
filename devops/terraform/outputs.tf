output "app_name" {
  description = "Configured application name"
  value       = var.app_name
}

output "backend_port" {
  description = "Target backend port"
  value       = var.port
}

output "deployment_status" {
  description = "Provisioning status"
  value       = "Terraform configuration initialized"
}
