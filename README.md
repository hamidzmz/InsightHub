# 🚀 InsightHub - Enterprise Job Scheduling Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green)](https://djangoproject.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-red)](https://redis.io)
[![Celery](https://img.shields.io/badge/Celery-5.3-green)](https://celeryproject.org)

InsightHub is a production-ready Django REST API platform for scheduling and managing background tasks with cron expressions. Built with enterprise-grade architecture, it provides comprehensive job scheduling capabilities with real-time monitoring, execution history, and role-based access control.

## ✨ Key Features

- 🔐 **JWT Authentication** - Secure user registration, login, and token management
- 📋 **Task Scheduling** - Schedule predefined tasks with standard cron expressions
- ⚡ **Background Processing** - Asynchronous task execution using Celery + Redis
- 📊 **Execution Monitoring** - Real-time status tracking and detailed execution logs
- 🔍 **Advanced Filtering** - Dynamic filtering and sorting from request body (Extra Credit)
- 👥 **Role-Based Access** - Super users vs regular users with business rule enforcement
- 📖 **Interactive API Docs** - Complete Swagger/OpenAPI documentation
- 🐳 **Docker Ready** - Full containerization with Docker Compose
- 🎯 **Parameter Validation** - Schema-based input validation for task parameters
- 📈 **Performance Optimized** - Database indexing and query optimization

## 🏗️ System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend/API  │    │   Django Web    │    │   PostgreSQL    │
│    Consumer     │────│     Server      │────│    Database     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                │
                       ┌─────────────────┐    ┌─────────────────┐
                       │  Celery Worker  │────│      Redis      │
                       │   (Background   │    │   (Broker +     │
                       │     Tasks)      │    │    Results)     │
                       └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │  Celery Beat    │
                       │  (Scheduler)    │
                       └─────────────────┘
```

## 📋 Available Predefined Tasks

1. **Send Email** - Send emails with optional delay
2. **Data Processing** - Process datasets with different algorithms
3. **Report Generation** - Generate reports with optional charts
4. **File Backup** - Backup files with compression options
5. **Database Cleanup** - Clean up old database records

## 🚀 Quick Start

## 🚀 Getting Started

### Prerequisites

- **Docker & Docker Compose** (Recommended)
- **Python 3.11+** (For local development)
- **PostgreSQL 15+** (If running locally)
- **Redis** (For Celery broker)
- **Git** (For version control)

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/InsightHub.git
cd InsightHub
```

### 2. Set Up Git Workflow (Optional but Recommended)

```bash
chmod +x git-setup.sh
./git-setup.sh
```

This configures:
- Git aliases for efficient workflow
- Commit message templates
- Branch protection reminders
- Conventional commit standards

📖 **Read our [Git Flow Guide](./GIT_FLOW.md)** for professional development practices.

### 3. Environment Setup

**Option A: Automatic Setup (Recommended)**

```bash
chmod +x setup.sh
./setup.sh
```

If you prefer manual setup, create a `.env` file:

```bash
cp .env.example .env
```

The `.env` file should contain:

```env
DEBUG=1
SECRET_KEY=django-insecure-dev-key-change-in-production
DATABASE_URL=postgresql://postgres:postgres@db:5432/insighthub
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,web
```

> **📝 Note**: The `.env` file is gitignored for security. You'll need to create it after cloning.

### 4. Start the Application

#### Option A: Using the Start Script (Recommended)

```bash
chmod +x start.sh
./start.sh
```

This script will:
- Build Docker containers
- Start database and Redis
- Run migrations
- Seed task definitions
- Create a superuser (optional)
- Start all services

#### Option B: Manual Setup

```bash
# Build and start services
docker-compose up --build -d

# Run migrations
docker-compose exec web python manage.py migrate

# Seed task definitions
docker-compose exec web python manage.py seed_tasks

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f
```

### 4. Access the Application

- **🌐 API Base URL**: http://localhost:8000/
- **📚 Swagger Documentation**: http://localhost:8000/api/docs/
- **⚡ Django Admin**: http://localhost:8000/admin/
- **📋 ReDoc Documentation**: http://localhost:8000/api/redoc/

## 🧪 Testing the Features

### 1. User Registration

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

### 2. User Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User"
  }
}
```

### 3. List Available Tasks

```bash
curl -X GET http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Schedule a Task

```bash
curl -X POST http://localhost:8000/api/schedules/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "task_definition": 1,
    "cron_expression": "0 9 * * *",
    "parameters": {
      "email": "recipient@example.com",
      "delay": 5
    },
    "is_active": true
  }'
```

### 5. List Your Schedules

```bash
curl -X GET http://localhost:8000/api/schedules/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 6. View Execution Logs

```bash
curl -X GET http://localhost:8000/api/schedules/1/logs/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 7. Dynamic Filtering (Extra Credit Feature)

```bash
curl -X POST http://localhost:8000/api/schedules/search/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "filters": {
      "is_active": true,
      "task_definition": 1
    },
    "ordering": ["-created_at"],
    "page_size": 5
  }'
```

### 8. Toggle Schedule Status

```bash
curl -X POST http://localhost:8000/api/schedules/1/toggle_active/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🛠️ Development Commands

We provide a convenient script for common development tasks:

```bash
# Make the script executable
chmod +x dev.sh

# Available commands:
./dev.sh shell          # Open Django shell
./dev.sh logs [service] # View logs (default: web)
./dev.sh migrate        # Run database migrations
./dev.sh makemigrations # Create new migrations
./dev.sh seed           # Seed task definitions
./dev.sh superuser      # Create superuser
./dev.sh test           # Run tests
./dev.sh collectstatic  # Collect static files
./dev.sh restart [svc]  # Restart service (default: web)
./dev.sh down           # Stop all services
./dev.sh clean          # Clean Docker resources
```

## 📊 Business Rules & Limitations

- **Regular Users**: Maximum 5 active scheduled jobs
- **Super Users**: Unlimited scheduled jobs + access to all user schedules
- **Token Expiry**: Access tokens expire in 15 minutes, refresh tokens in 1 day
- **Cron Validation**: All cron expressions are validated using the `croniter` library
- **Parameter Validation**: Task parameters are validated against predefined schemas

## 🏢 API Documentation

### Base URLs
- **Development**: http://localhost:8000/api/
- **Authentication**: `/auth/`
- **Tasks**: `/tasks/`
- **Schedules**: `/schedules/`

### Authentication Endpoints
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/refresh/` - Refresh access token
- `GET /api/auth/profile/` - Get user profile

### Task Endpoints
- `GET /api/tasks/` - List all task definitions
- `GET /api/tasks/available/` - List active task definitions

### Schedule Endpoints
- `GET /api/schedules/` - List user schedules (with pagination & filtering)
- `POST /api/schedules/` - Create new schedule
- `GET /api/schedules/{id}/` - Get schedule details
- `PUT /api/schedules/{id}/` - Update schedule
- `DELETE /api/schedules/{id}/` - Delete schedule
- `POST /api/schedules/{id}/toggle_active/` - Enable/disable schedule
- `GET /api/schedules/{id}/logs/` - Get execution history
- `POST /api/schedules/search/` - Dynamic filtering (Extra Credit)

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DEBUG` | Enable debug mode | `False` | No |
| `SECRET_KEY` | Django secret key | - | Yes |
| `DATABASE_URL` | PostgreSQL connection string | `sqlite:///db.sqlite3` | No |
| `CELERY_BROKER_URL` | Redis broker URL | `redis://localhost:6379/0` | No |
| `CELERY_RESULT_BACKEND` | Redis result backend | `redis://localhost:6379/0` | No |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` | No |

### Docker Services

| Service | Description | Port | Health Check |
|---------|-------------|------|--------------|
| `web` | Django application | 8000 | - |
| `db` | PostgreSQL database | 5432 | pg_isready |
| `redis` | Redis broker | 6379 | redis-cli ping |
| `celery` | Background worker | - | - |
| `celery-beat` | Task scheduler | - | - |

## 🧪 Running Tests

```bash
# Run all tests
./dev.sh test

# Run tests with coverage
docker-compose exec web python manage.py test --keepdb --parallel

# Run specific test file
docker-compose exec web python manage.py test schedules.tests

# Run tests in debug mode
docker-compose exec web python manage.py test --debug-mode
```

## 📁 Project Structure

```
InsightHub/
├── 📁 api/                 # API utilities (filters, pagination, permissions)
├── 📁 core/                # Shared utilities and base classes
├── 📁 executions/          # Execution logs and monitoring
├── 📁 insighthub/          # Main Django project settings
├── 📁 schedules/           # Job scheduling logic
├── 📁 staticfiles/         # Static files (CSS, JS, images)
├── 📁 tasks/               # Task definitions and Celery tasks
├── 📁 users/               # User management and authentication
├── 📄 .env                 # Environment variables
├── 📄 docker-compose.yml   # Docker services configuration
├── 📄 Dockerfile           # Docker image definition
├── 📄 requirements.txt     # Python dependencies
├── 📄 manage.py            # Django management script
├── 📄 dev.sh               # Development helper script
└── 📄 start.sh             # Quick start script
```

## 🚨 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   lsof -i :8000
   
   # Stop the service or change port in docker-compose.yml
   ```

2. **Database connection errors**
   ```bash
   # Restart database service
   docker-compose restart db
   
   # Check database logs
   docker-compose logs db
   ```

3. **Celery tasks not executing**
   ```bash
   # Check Celery worker logs
   docker-compose logs celery
   
   # Check Celery beat logs
   docker-compose logs celery-beat
   
   # Restart Celery services
   docker-compose restart celery celery-beat
   ```

4. **Migration issues**
   ```bash
   # Reset migrations (development only)
   ./dev.sh clean
   docker-compose up --build
   ```

### Logs and Debugging

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f web
docker-compose logs -f celery
docker-compose logs -f db

# Enter container shell
docker-compose exec web bash
docker-compose exec db psql -U postgres -d insighthub
```

## 🚀 Production Deployment

### Environment Setup

1. **Set production environment variables**
   ```env
   DEBUG=0
   SECRET_KEY=your-super-secure-secret-key
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

2. **Database and Redis**
   - Use managed PostgreSQL service (AWS RDS, Google Cloud SQL)
   - Use managed Redis service (AWS ElastiCache, Google Memorystore)

3. **Security considerations**
   - Use HTTPS in production
   - Set secure secret key
   - Configure proper CORS settings
   - Use environment-specific settings

### Docker Production Build

```bash
# Build production image
docker build -t insighthub:production .

# Run with production settings
docker run -p 8000:8000 --env-file .env.production insighthub:production
```

## 📝 For GitHub Users

### Getting Started from GitHub

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/InsightHub.git
   cd InsightHub
   ```

2. **Quick setup** (recommended):
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Set up Git workflow** (recommended for developers):
   ```bash
   chmod +x git-setup.sh
   ./git-setup.sh
   ```

4. **Start the application**:
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

### What's Included

- 📄 **README.md** - Complete project documentation
- 📄 **TESTING_GUIDE.md** - Comprehensive API testing examples
- 📄 **GIT_FLOW.md** - Professional Git workflow guide
- 📄 **CONTRIBUTING.md** - Contribution guidelines
- 📄 **.env.example** - Environment variables template
- 📄 **setup.sh** - Quick setup script for new users
- 📄 **git-setup.sh** - Git workflow configuration
- 📄 **start.sh** - Application startup script
- 📄 **dev.sh** - Development helper commands
- 🐳 **Docker** configuration for easy deployment
- 🔧 **GitHub templates** - Issue and PR templates

### Environment Security

The `.env` file containing sensitive configuration is **not included** in the repository for security reasons. The setup script will create it automatically from the template, or you can copy it manually:

```bash
cp .env.example .env
```

## 🤝 Contributing

We welcome contributions! This project follows professional development practices:

### Quick Start for Contributors

1. **Read the guides**:
   - 📖 [Git Flow Guide](./GIT_FLOW.md) - Branching strategy and workflow
   - 📖 [Contributing Guide](./CONTRIBUTING.md) - Detailed contribution guidelines

2. **Set up development environment**:
   ```bash
   git clone https://github.com/your-username/InsightHub.git
   cd InsightHub
   ./git-setup.sh  # Configure Git workflow
   ./setup.sh      # Set up environment
   ./start.sh      # Start development server
   ```

3. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make changes and test**:
   ```bash
   # Make your changes
   docker-compose exec web python manage.py test
   ```

5. **Submit Pull Request**:
   - Use our PR template
   - Follow conventional commit messages
   - Ensure all tests pass

### Development Standards

- ✅ **GitHub Flow**: Simple, effective branching strategy
- ✅ **Conventional Commits**: Standardized commit messages
- ✅ **Code Review**: All changes reviewed before merge
- ✅ **Test Coverage**: Comprehensive testing requirements
- ✅ **Documentation**: Keep docs updated with changes
- ✅ **Clean Code**: Self-documenting, well-structured code

### Contribution Areas

- 🐛 **Bug Fixes**: Report and fix issues
- ✨ **Features**: Enhance scheduling capabilities
- 📚 **Documentation**: Improve guides and examples
- 🧪 **Testing**: Increase test coverage
- 🚀 **Performance**: Optimize database queries
- 🔒 **Security**: Strengthen authentication and validation

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**🎉 Happy scheduling with InsightHub!**