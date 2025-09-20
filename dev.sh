#!/bin/bash

echo "🔧 InsightHub Development Commands"
echo "=================================="

case $1 in
    "shell")
        echo "🐍 Opening Django shell..."
        docker-compose exec web python manage.py shell
        ;;
    "logs")
        service=${2:-web}
        echo "📋 Showing logs for $service..."
        docker-compose logs -f $service
        ;;
    "migrate")
        echo "🗄️ Running migrations..."
        docker-compose exec web python manage.py migrate
        ;;
    "makemigrations")
        echo "📝 Creating migrations..."
        docker-compose exec web python manage.py makemigrations
        ;;
    "seed")
        echo "🌱 Seeding task definitions..."
        docker-compose exec web python manage.py seed_tasks
        ;;
    "superuser")
        echo "👤 Creating superuser..."
        docker-compose exec web python manage.py createsuperuser
        ;;
    "test")
        echo "🧪 Running tests..."
        docker-compose exec web python manage.py test
        ;;
    "collectstatic")
        echo "📦 Collecting static files..."
        docker-compose exec web python manage.py collectstatic --noinput
        ;;
    "restart")
        service=${2:-web}
        echo "🔄 Restarting $service..."
        docker-compose restart $service
        ;;
    "down")
        echo "🛑 Stopping all services..."
        docker-compose down
        ;;
    "clean")
        echo "🧹 Cleaning up Docker resources..."
        docker-compose down -v
        docker system prune -f
        ;;
    *)
        echo "Usage: ./dev.sh [command]"
        echo ""
        echo "Available commands:"
        echo "  shell         - Open Django shell"
        echo "  logs [svc]    - Show logs (default: web)"
        echo "  migrate       - Run database migrations"
        echo "  makemigrations- Create new migrations"
        echo "  seed          - Seed task definitions"
        echo "  superuser     - Create superuser"
        echo "  test          - Run tests"
        echo "  collectstatic - Collect static files"
        echo "  restart [svc] - Restart service (default: web)"
        echo "  down          - Stop all services"
        echo "  clean         - Stop and clean all Docker resources"
        ;;
esac