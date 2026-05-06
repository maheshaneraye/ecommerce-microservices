#!/bin/bash

exec > /var/log/user-data.log 2>&1

echo "===== STARTING SETUP ====="

apt-get update -y

apt-get install -y docker.io curl

systemctl enable docker
systemctl start docker

usermod -aG docker ubuntu

echo "Docker installed"

# Lightweight K3s
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="--disable traefik --disable servicelb" sh -

echo "K3s installed"

# Create 2GB swap
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

echo '/swapfile none swap sw 0 0' >> /etc/fstab

echo "Swap enabled"

echo "===== SETUP COMPLETE ====="
