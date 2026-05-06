#!/bin/bash

# Update system
apt update -y

# Install Docker
apt install -y docker.io
systemctl enable docker
systemctl start docker

# Install K3s (lightweight Kubernetes)
curl -sfL https://get.k3s.io | sh -

# Fix kubeconfig permissions
chmod 644 /etc/rancher/k3s/k3s.yaml

# Configure kubectl for ubuntu user
echo "export KUBECONFIG=/etc/rancher/k3s/k3s.yaml" >> /home/ubuntu/.bashrc

# Optional: install kubectl explicitly (safe fallback)
apt install -y kubectl
