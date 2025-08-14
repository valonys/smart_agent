# 🚀 Deployment Guide - Smart Expense Agent

This guide provides step-by-step instructions for deploying the Smart Expense Agent application in various environments.

## 📋 Prerequisites

Before deployment, ensure you have:

- **Python 3.8+** installed
- **PostgreSQL database** set up
- **Groq API key** obtained from [Groq Console](https://console.groq.com/)
- **Git** for version control

## 🔧 Environment Setup

### 1. Environment Variables

Create a `.env` file in the project root:

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/smart_expense_agent

# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile

# Optional: Application Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

### 2. Database Setup

#### PostgreSQL Installation

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
Download and install from [PostgreSQL Official Site](https://www.postgresql.org/download/windows/)

#### Database Creation

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE smart_expense_agent;
CREATE USER smart_agent_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE smart_expense_agent TO smart_agent_user;
\q
```

## 🏠 Local Development Deployment

### 1. Clone Repository

```bash
git clone https://github.com/valonys/smart_agent.git
cd smart_agent
```

### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## 🐳 Docker Deployment

### 1. Create Dockerfile

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2. Create docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - DATABASE_URL=postgresql://smart_agent_user:password@db:5432/smart_expense_agent
      - GROQ_API_KEY=${GROQ_API_KEY}
      - GROQ_MODEL=llama-3.3-70b-versatile
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=smart_expense_agent
      - POSTGRES_USER=smart_agent_user
      - POSTGRES_PASSWORD=your_secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

volumes:
  postgres_data:
```

### 3. Deploy with Docker Compose

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

## ☁️ Cloud Deployment

### Heroku Deployment

#### 1. Create Heroku App

```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login to Heroku
heroku login

# Create app
heroku create your-smart-expense-agent

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini
```

#### 2. Configure Environment Variables

```bash
heroku config:set GROQ_API_KEY=your_groq_api_key_here
heroku config:set GROQ_MODEL=llama-3.3-70b-versatile
```

#### 3. Deploy Application

```bash
# Add Heroku remote
heroku git:remote -a your-smart-expense-agent

# Deploy
git push heroku main

# Open application
heroku open
```

### Railway Deployment

#### 1. Connect Repository

1. Go to [Railway Dashboard](https://railway.app/)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your repository

#### 2. Configure Environment

Add environment variables in Railway dashboard:
- `DATABASE_URL` (auto-generated)
- `GROQ_API_KEY`
- `GROQ_MODEL`

#### 3. Deploy

Railway will automatically deploy your application on every push to main branch.

### DigitalOcean App Platform

#### 1. Create App

1. Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
2. Click "Create App"
3. Connect your GitHub repository

#### 2. Configure App Spec

```yaml
name: smart-expense-agent
services:
- name: web
  source_dir: /
  github:
    repo: valonys/smart_agent
    branch: main
  run_command: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: GROQ_API_KEY
    value: ${GROQ_API_KEY}
  - key: GROQ_MODEL
    value: llama-3.3-70b-versatile

databases:
- name: db
  engine: PG
  version: "15"
```

#### 3. Deploy

DigitalOcean will automatically deploy your application.

## 🔒 Production Security

### 1. Environment Variables

- **Never commit** `.env` files to version control
- Use **strong, unique passwords** for database
- **Rotate API keys** regularly
- Use **secrets management** services in production

### 2. Database Security

```sql
-- Create read-only user for backups
CREATE USER backup_user WITH PASSWORD 'backup_password';
GRANT CONNECT ON DATABASE smart_expense_agent TO backup_user;
GRANT USAGE ON SCHEMA public TO backup_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO backup_user;
```

### 3. Network Security

- Use **HTTPS** in production
- Configure **firewall rules**
- Enable **SSL/TLS** for database connections
- Use **VPN** for database access

### 4. Application Security

```python
# Add to app.py for production
import os
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
os.environ['STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION'] = 'true'
```

## 📊 Monitoring & Logging

### 1. Application Logs

```bash
# View Streamlit logs
streamlit run app.py --logger.level=info

# Docker logs
docker-compose logs -f app
```

### 2. Database Monitoring

```sql
-- Monitor active connections
SELECT * FROM pg_stat_activity WHERE datname = 'smart_expense_agent';

-- Monitor table sizes
SELECT schemaname, tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables WHERE schemaname = 'public';
```

### 3. Health Checks

```bash
# Application health
curl http://localhost:8501/_stcore/health

# Database health
pg_isready -h localhost -p 5432 -d smart_expense_agent
```

## 🔄 Backup & Recovery

### 1. Database Backup

```bash
# Create backup
pg_dump -h localhost -U smart_agent_user -d smart_expense_agent > backup.sql

# Automated backup script
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h localhost -U smart_agent_user -d smart_expense_agent > $BACKUP_DIR/backup_$DATE.sql
```

### 2. Application Backup

```bash
# Backup application files
tar -czf app_backup_$(date +%Y%m%d).tar.gz . --exclude=venv --exclude=__pycache__

# Backup environment variables
cp .env .env.backup
```

### 3. Recovery Procedures

```bash
# Restore database
psql -h localhost -U smart_agent_user -d smart_expense_agent < backup.sql

# Restore application
tar -xzf app_backup_YYYYMMDD.tar.gz
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Database Connection Errors

```bash
# Check database status
sudo systemctl status postgresql

# Test connection
psql -h localhost -U smart_agent_user -d smart_expense_agent
```

#### 2. API Key Issues

```bash
# Test Groq API
curl -H "Authorization: Bearer $GROQ_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":"Hello"}]}' \
     https://api.groq.com/openai/v1/chat/completions
```

#### 3. Port Conflicts

```bash
# Check port usage
netstat -tulpn | grep :8501

# Kill process using port
sudo kill -9 $(lsof -t -i:8501)
```

### Performance Optimization

#### 1. Database Optimization

```sql
-- Create indexes for better performance
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_conversations_session_id ON conversations(session_id);
```

#### 2. Application Optimization

```python
# Enable caching
@st.cache_data
def expensive_function():
    # Your expensive operation here
    pass

# Use connection pooling
# Already configured in utils/db.py
```

## 📞 Support

For deployment issues:

1. **Check logs** for error messages
2. **Verify environment variables** are set correctly
3. **Test database connection** manually
4. **Check API key** validity
5. **Review firewall settings**

**Contact**: team@smartexpenseagent.com

---

**Happy Deploying! 🚀**
