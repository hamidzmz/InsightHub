#!/bin/bash

echo "🚀 Starting InsightHub setup..."

echo "📦 Building Docker containers..."
docker-compose build

echo "🗄️ Starting database and Redis..."
docker-compose up -d db redis

echo "⏳ Waiting for database to be ready..."
sleep 10

echo "🔧 Running migrations..."
docker-compose run --rm web python manage.py migrate

echo "🌱 Seeding task definitions..."
docker-compose run --rm web python manage.py seed_tasks

echo "👤 Creating superuser (skip if you already have one)..."
read -p "Do you want to create a superuser? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose run --rm web python manage.py createsuperuser
fi

echo "🎉 Starting all services..."
docker-compose up

echo "✅ InsightHub is now running!"
echo "🌐 API: http://localhost:8000/"
echo "📚 Swagger UI: http://localhost:8000/api/docs/"
echo "⚡ Admin Panel: http://localhost:8000/admin/"