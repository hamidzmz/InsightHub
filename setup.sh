#!/bin/bash

echo "🎯 InsightHub Quick Setup for GitHub Users"
echo "=========================================="

# Check if .env exists
if [ -f ".env" ]; then
    echo "✅ .env file already exists"
else
    echo "📝 Creating .env file from template..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ .env file created from .env.example"
        echo "💡 You can customize the .env file if needed"
    else
        echo "❌ .env.example not found. Creating default .env..."
        cat > .env << 'EOF'
DEBUG=1
SECRET_KEY=django-insecure-dev-key-change-in-production
DATABASE_URL=postgresql://postgres:postgres@db:5432/insighthub
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,web
EOF
        echo "✅ Default .env file created"
    fi
fi

echo ""
echo "🚀 Now you can start the application:"
echo "   ./start.sh            # Complete setup with prompts"
echo "   or"
echo "   docker-compose up --build   # Manual setup"
echo ""
echo "📚 Don't forget to check:"
echo "   - README.md for full documentation"
echo "   - TESTING_GUIDE.md for API testing examples"
echo "   - http://localhost:8000/api/docs/ for interactive API docs"
echo ""
echo "🎉 Setup complete!"