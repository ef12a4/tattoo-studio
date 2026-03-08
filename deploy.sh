#!/bin/bash

# Tattoo Studio Production Deployment Script
echo "🎨 Tattoo Studio Production Deployment Started..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads ssl

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your production settings before continuing."
    echo "   - Update SECRET_KEY"
    echo "   - Update database credentials"
    echo "   - Update email settings"
    echo "   - Update payment gateway keys"
    echo "   - Update domain name"
    read -p "Press Enter after editing .env file..."
fi

# Generate SSL certificate (self-signed for development)
if [ ! -f ssl/cert.pem ]; then
    echo "🔐 Generating SSL certificate..."
    openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes \
        -subj "/C=TR/ST=Istanbul/L=Istanbul/O=Tattoo Studio/CN=localhost"
fi

# Build and start services
echo "🐳 Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."
docker-compose ps

# Initialize database
echo "💾 Initializing database..."
docker-compose exec tattoo-studio python init_db.py

# Show deployment information
echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Application URLs:"
echo "   HTTP:  http://localhost"
echo "   HTTPS: https://localhost"
echo ""
echo "🔧 Management Commands:"
echo "   View logs:     docker-compose logs -f"
echo "   Stop services: docker-compose down"
echo "   Restart:       docker-compose restart"
echo "   Update:        docker-compose pull && docker-compose up -d"
echo ""
echo "📊 Monitoring:"
echo "   Health check:  curl https://localhost/health"
echo "   Flower (Celery): http://localhost:5555"
echo ""
echo "🎉 Tattoo Studio is now running in production mode!"
