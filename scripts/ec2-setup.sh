#!/bin/bash
# Run once on a fresh Ubuntu EC2 instance (as root or with sudo).
set -e

# --- Docker ---
apt-get update
apt-get install -y ca-certificates curl git
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
  | tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

systemctl enable docker
systemctl start docker
usermod -aG docker ubuntu

# --- App directory ---
mkdir -p /opt/coffee-restaurant
cd /opt/coffee-restaurant

# Clone repo (replace URL with your actual GitHub repo)
git clone https://github.com/Tojinazarovbekzod/Coffee_restaurant .

# Create .env from example
cp .env.example .env
echo ""
echo "========================================================"
echo "  Edit /opt/coffee-restaurant/.env with real values"
echo "  Then start the stack:"
echo "    docker compose -f docker-compose.prod.yml up -d"
echo "========================================================"
