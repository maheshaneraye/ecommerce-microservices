output "public_ip" {
  description = "Public IP of EC2 instance"
  value       = aws_instance.k8s_server.public_ip
}

output "ssh_command" {
  value = "ssh -i devops-key ubuntu@${aws_instance.k8s_server.public_ip}"
}
