output "instance_public_ip" {
  value = aws_instance.k8s_server.public_ip
}

output "ssh_command" {
  value = "ssh -i ecommerce-microservices-key.pem ubuntu@${aws_instance.k8s_server.public_ip}"
}
