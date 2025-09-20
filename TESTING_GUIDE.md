# 🧪 InsightHub API Testing Guide

This guide provides comprehensive examples for testing all InsightHub features using curl commands and example responses.

## 🚀 Getting Started

### Prerequisites
- InsightHub running locally (see main README.md)
- curl installed
- jq (optional, for pretty JSON formatting)

### Base URL
```
http://localhost:8000/api
```

## 🔐 Authentication Flow

### 1. Register a New User

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

**Expected Response:**
```json
{
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "full_name": "Test User",
    "is_super_user": false,
    "created_at": "2025-09-20T17:30:00Z"
  },
  "message": "User created successfully"
}
```

### 2. Login User

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword123"
  }'
```

**Expected Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk1MjI4NjAwLCJpYXQiOjE2OTUyMjc3MDAsImp0aSI6IjEyMzQ1Njc4OTAiLCJ1c2VyX2lkIjoxfQ.abc123...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NTMxNDEwMCwiaWF0IjoxNjk1MjI3NzAwLCJqdGkiOiIwOTg3NjU0MzIxIiwidXNlcl9pZCI6MX0.def456...",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User",
    "full_name": "Test User",
    "is_super_user": false,
    "created_at": "2025-09-20T17:30:00Z"
  }
}
```

### 3. Refresh Access Token

```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "YOUR_REFRESH_TOKEN"
  }'
```

### 4. Get User Profile

```bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📋 Task Management

### 1. List All Available Tasks

```bash
curl -X GET http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Expected Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Send Email",
      "description": "Send an email with optional delay",
      "input_schema": {
        "email": "string",
        "delay": "integer"
      },
      "input_fields": ["email", "delay"],
      "is_active": true,
      "created_at": "2025-09-20T17:00:00Z"
    },
    {
      "id": 2,
      "name": "Data Processing",
      "description": "Process dataset with specified parameters",
      "input_schema": {
        "dataset_size": "integer",
        "processing_type": "string"
      },
      "input_fields": ["dataset_size", "processing_type"],
      "is_active": true,
      "created_at": "2025-09-20T17:00:00Z"
    }
  ]
}
```

### 2. List Only Active Tasks

```bash
curl -X GET http://localhost:8000/api/tasks/available/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📅 Schedule Management

### 1. Create a Schedule

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

**Expected Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "user_username": "testuser",
  "user_full_name": "Test User",
  "task_definition_id": 1,
  "task_definition_name": "Send Email",
  "task_definition_description": "Send an email with optional delay",
  "cron_expression": "0 9 * * *",
  "parameters": {
    "email": "recipient@example.com",
    "delay": 5
  },
  "is_active": true,
  "created_at": "2025-09-20T17:45:00Z",
  "updated_at": "2025-09-20T17:45:00Z",
  "next_run_time": "2025-09-21T09:00:00Z"
}
```

### 2. List User Schedules

```bash
curl -X GET http://localhost:8000/api/schedules/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. List Schedules with Pagination

```bash
curl -X GET "http://localhost:8000/api/schedules/?page=1&page_size=5" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Filter Schedules

```bash
# Filter by active status
curl -X GET "http://localhost:8000/api/schedules/?is_active=true" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Filter by task definition
curl -X GET "http://localhost:8000/api/schedules/?task_definition=1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# Multiple filters
curl -X GET "http://localhost:8000/api/schedules/?is_active=true&task_definition=1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Get Specific Schedule

```bash
curl -X GET http://localhost:8000/api/schedules/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 6. Update Schedule

```bash
curl -X PUT http://localhost:8000/api/schedules/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "cron_expression": "0 10 * * *",
    "parameters": {
      "email": "updated@example.com",
      "delay": 10
    },
    "is_active": true
  }'
```

### 7. Partial Update Schedule

```bash
curl -X PATCH http://localhost:8000/api/schedules/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "is_active": false
  }'
```

### 8. Toggle Schedule Status

```bash
curl -X POST http://localhost:8000/api/schedules/1/toggle_active/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Expected Response:**
```json
{
  "message": "Schedule deactivated successfully",
  "is_active": false
}
```

### 9. Delete Schedule

```bash
curl -X DELETE http://localhost:8000/api/schedules/1/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🔍 Advanced Filtering (Extra Credit Feature)

### Dynamic Search with Request Body

```bash
curl -X POST http://localhost:8000/api/schedules/search/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "filters": {
      "is_active": true,
      "task_definition": 1
    },
    "ordering": ["-created_at", "cron_expression"],
    "page_size": 10
  }'
```

**Expected Response:**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 3,
      "user_id": 1,
      "user_username": "testuser",
      "task_definition_name": "Send Email",
      "cron_expression": "0 9 * * *",
      "is_active": true,
      "created_at": "2025-09-20T18:00:00Z"
    }
  ]
}
```

### Complex Filtering Examples

```bash
# Filter by date range
curl -X POST http://localhost:8000/api/schedules/search/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "filters": {
      "created_at__gte": "2025-09-20T00:00:00Z",
      "created_at__lte": "2025-09-21T00:00:00Z"
    },
    "ordering": ["created_at"]
  }'

# Multiple field ordering
curl -X POST http://localhost:8000/api/schedules/search/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "ordering": ["is_active", "-created_at"],
    "page_size": 20
  }'
```

## 📊 Execution Monitoring

### 1. Get Execution Logs for a Schedule

```bash
curl -X GET http://localhost:8000/api/schedules/1/logs/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Expected Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "schedule_id": 1,
      "celery_task_id": "abc123-def456-789ghi",
      "status": "success",
      "started_at": "2025-09-20T09:00:00Z",
      "completed_at": "2025-09-20T09:00:05Z",
      "result": {
        "email_sent": true,
        "recipient": "recipient@example.com"
      },
      "error_message": null,
      "execution_time": "0:00:05"
    },
    {
      "id": 2,
      "schedule_id": 1,
      "celery_task_id": "xyz789-uvw456-rst123",
      "status": "failure",
      "started_at": "2025-09-19T09:00:00Z",
      "completed_at": "2025-09-19T09:00:03Z",
      "result": null,
      "error_message": "Invalid email address",
      "execution_time": "0:00:03"
    }
  ]
}
```

### 2. Get Logs with Pagination

```bash
curl -X GET "http://localhost:8000/api/schedules/1/logs/?page=1&page_size=10" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🧪 Complete Testing Workflow

### Test Scenario: Regular User Journey

```bash
#!/bin/bash

# Set base URL
BASE_URL="http://localhost:8000/api"

echo "🧪 Starting InsightHub API Testing..."

# 1. Register a new user
echo "1. Registering new user..."
REGISTER_RESPONSE=$(curl -s -X POST $BASE_URL/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "apitest",
    "email": "apitest@example.com",
    "first_name": "API",
    "last_name": "Test",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }')
echo "✅ User registered: $(echo $REGISTER_RESPONSE | jq -r '.user.username')"

# 2. Login user
echo "2. Logging in user..."
LOGIN_RESPONSE=$(curl -s -X POST $BASE_URL/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "apitest",
    "password": "securepassword123"
  }')
ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.access_token')
echo "✅ User logged in, token obtained"

# 3. Get available tasks
echo "3. Fetching available tasks..."
TASKS_RESPONSE=$(curl -s -X GET $BASE_URL/tasks/ \
  -H "Authorization: Bearer $ACCESS_TOKEN")
TASK_ID=$(echo $TASKS_RESPONSE | jq -r '.results[0].id')
echo "✅ Found $(echo $TASKS_RESPONSE | jq -r '.count') tasks"

# 4. Create a schedule
echo "4. Creating a schedule..."
SCHEDULE_RESPONSE=$(curl -s -X POST $BASE_URL/schedules/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d "{
    \"task_definition\": $TASK_ID,
    \"cron_expression\": \"0 9 * * *\",
    \"parameters\": {
      \"email\": \"test@example.com\",
      \"delay\": 5
    },
    \"is_active\": true
  }")
SCHEDULE_ID=$(echo $SCHEDULE_RESPONSE | jq -r '.id')
echo "✅ Schedule created with ID: $SCHEDULE_ID"

# 5. List user schedules
echo "5. Listing user schedules..."
USER_SCHEDULES=$(curl -s -X GET $BASE_URL/schedules/ \
  -H "Authorization: Bearer $ACCESS_TOKEN")
echo "✅ User has $(echo $USER_SCHEDULES | jq -r '.count') schedules"

# 6. Test dynamic filtering
echo "6. Testing dynamic filtering..."
FILTERED_SCHEDULES=$(curl -s -X POST $BASE_URL/schedules/search/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{
    "filters": {
      "is_active": true
    },
    "ordering": ["-created_at"]
  }')
echo "✅ Found $(echo $FILTERED_SCHEDULES | jq -r '.count') active schedules"

# 7. Toggle schedule status
echo "7. Toggling schedule status..."
TOGGLE_RESPONSE=$(curl -s -X POST $BASE_URL/schedules/$SCHEDULE_ID/toggle_active/ \
  -H "Authorization: Bearer $ACCESS_TOKEN")
echo "✅ Schedule status: $(echo $TOGGLE_RESPONSE | jq -r '.message')"

# 8. Get execution logs
echo "8. Checking execution logs..."
LOGS_RESPONSE=$(curl -s -X GET $BASE_URL/schedules/$SCHEDULE_ID/logs/ \
  -H "Authorization: Bearer $ACCESS_TOKEN")
echo "✅ Found $(echo $LOGS_RESPONSE | jq -r '.count') execution logs"

echo "🎉 API testing completed successfully!"
```

## 🎯 Testing Different Task Types

### 1. Send Email Task

```bash
curl -X POST http://localhost:8000/api/schedules/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "task_definition": 1,
    "cron_expression": "*/5 * * * *",
    "parameters": {
      "email": "test@example.com",
      "delay": 2
    },
    "is_active": true
  }'
```

### 2. Data Processing Task

```bash
curl -X POST http://localhost:8000/api/schedules/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "task_definition": 2,
    "cron_expression": "0 2 * * *",
    "parameters": {
      "dataset_size": 1000,
      "processing_type": "complex"
    },
    "is_active": true
  }'
```

### 3. Report Generation Task

```bash
curl -X POST http://localhost:8000/api/schedules/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "task_definition": 3,
    "cron_expression": "0 8 * * 1",
    "parameters": {
      "report_type": "weekly",
      "include_charts": true
    },
    "is_active": true
  }'
```

### 4. File Backup Task

```bash
curl -X POST http://localhost:8000/api/schedules/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "task_definition": 4,
    "cron_expression": "0 23 * * *",
    "parameters": {
      "source_path": "/app/data",
      "destination": "/backup/daily",
      "compress": true
    },
    "is_active": true
  }'
```

### 5. Database Cleanup Task

```bash
curl -X POST http://localhost:8000/api/schedules/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "task_definition": 5,
    "cron_expression": "0 1 1 * *",
    "parameters": {
      "days_old": 30,
      "table_name": "execution_logs"
    },
    "is_active": true
  }'
```

## ❌ Error Testing

### 1. Invalid Cron Expression

```bash
curl -X POST http://localhost:8000/api/schedules/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "task_definition": 1,
    "cron_expression": "invalid cron",
    "parameters": {
      "email": "test@example.com"
    },
    "is_active": true
  }'
```

**Expected Error Response:**
```json
{
  "cron_expression": ["Invalid cron expression format"]
}
```

### 2. Invalid Task Parameters

```bash
curl -X POST http://localhost:8000/api/schedules/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "task_definition": 1,
    "cron_expression": "0 9 * * *",
    "parameters": {
      "email": 123,
      "delay": "not_a_number"
    },
    "is_active": true
  }'
```

### 3. Exceeding Job Limit (Regular Users)

```bash
# Create 6 schedules to test the 5-job limit
for i in {1..6}; do
  curl -X POST http://localhost:8000/api/schedules/ \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
    -d "{
      \"task_definition\": 1,
      \"cron_expression\": \"0 $i * * *\",
      \"parameters\": {
        \"email\": \"test$i@example.com\"
      },
      \"is_active\": true
    }"
done
```

## 🔒 Permission Testing

### Super User Access

```bash
# Login as superuser
SUPERUSER_LOGIN=$(curl -s -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }')
SUPER_TOKEN=$(echo $SUPERUSER_LOGIN | jq -r '.access_token')

# Super user can see all schedules
curl -X GET http://localhost:8000/api/schedules/ \
  -H "Authorization: Bearer $SUPER_TOKEN"
```

---

This testing guide covers all major features and edge cases. Use the Swagger UI at http://localhost:8000/api/docs/ for interactive testing!