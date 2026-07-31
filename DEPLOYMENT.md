# Production Deployment & Infrastructure Guide

> **Fitness Tracker Using Machine Learning (FitAI)**  
> *Author & Lead Architect: **Ravi Ranjan Singh***

---

## 1. Executive Summary

This guide provides instructions for deploying **Fitness Tracker Using Machine Learning** to production environments. The application is containerized using Docker and organized with Docker Compose, enabling seamless deployment across standalone cloud VMs (AWS EC2, DigitalOcean droplets), container services (AWS ECS, GCP Cloud Run), or Kubernetes clusters.

---

## 2. Infrastructure Requirements

### Minimum Recommended Specs
- **CPU**: 2 vCPUs (x86_64 or ARM64)
- **RAM**: 4 GB RAM (8 GB recommended for concurrent high-volume inference loads)
- **Disk Storage**: 20 GB SSD storage
- **OS**: Ubuntu 22.04 LTS or Debian 12
- **Network**: Inbound ports `80` (HTTP), `443` (HTTPS)

---

## 3. Container Topology

```
                         [ Internet Traffic ]
                                   |
                                   v
             [ NGINX Reverse Proxy Container (Port 80/443) ]
                                   |
           +-----------------------+-----------------------+
           |                                               |
           v                                               v
[ React Frontend Container ]                [ FastAPI Backend Container ]
  (Static NGINX Host)                         (Uvicorn ASGI App Server)
                                                           |
                                           +---------------+---------------+
                                           |                               |
                                           v                               v
                               [ PostgreSQL 15 Container ]    [ Redis 7 Container ]
```

---

## 4. Production Environment Configuration (`.env.production`)

Create a `.env.production` file on your host server:

```env
# Application Settings
PROJECT_NAME="FitAI Machine Learning Engine"
ENVIRONMENT="production"
LOG_LEVEL="INFO"

# Security Secrets (Generate using `openssl rand -hex 32`)
SECRET_KEY="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database Connection (PostgreSQL 15)
POSTGRES_USER="fitai_prod_user"
POSTGRES_PASSWORD="SuperSecureProductionPassword123!"
POSTGRES_DB="fitai_production_db"
DATABASE_URL="postgresql+asyncpg://fitai_prod_user:SuperSecureProductionPassword123!@db:5432/fitai_production_db"

# Redis Cache & Rate Limiter
REDIS_URL="redis://cache:6379/0"

# CORS Whitelist (Comma-separated)
CORS_ORIGINS="https://fitai.yourdomain.com"

# ML Artifact Location
ML_MODEL_PATH="/app/src/ml/models/xgb_calorie_v1.onnx"
```

---

## 5. Docker Production Configuration

### 5.1 Docker Compose Manifest (`docker-compose.prod.yml`)

```yaml
version: '3.8'

services:
  gateway:
    image: nginx:1.25-alpine
    container_name: fitai_prod_gateway
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx.prod.conf:/etc/nginx/nginx.conf:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - backend
      - frontend

  backend:
    build:
      context: .
      dockerfile: docker/Dockerfile.backend
    container_name: fitai_prod_backend
    restart: always
    env_file:
      - .env.production
    expose:
      - "8000"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 15s
      timeout: 5s
      retries: 3
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy

  frontend:
    build:
      context: ./src/frontend
      dockerfile: ../../docker/Dockerfile.frontend
    container_name: fitai_prod_frontend
    restart: always
    expose:
      - "3000"

  db:
    image: postgres:15-alpine
    container_name: fitai_prod_db
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    container_name: fitai_prod_cache
    restart: always
    command: redis-server --save 60 1 --loglevel notice
    volumes:
      - redis_prod_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  postgres_prod_data:
  redis_prod_data:
```

---

## 6. Deployment Workflow Commands

### Step 1: Provision Host Server & Pull Code
```bash
git clone https://github.com/raviranjansingh/FITNESS-TRACKER-USING-MACHINE-LEARNNING.git /opt/fitai
cd /opt/fitai
```

### Step 2: Build & Start Production Containers
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

### Step 3: Execute Database Migrations
```bash
docker-compose -f docker-compose.prod.yml exec backend alembic upgrade head
```

### Step 4: Verify Deployment Health
```bash
curl -I https://fitai.yourdomain.com/health
```

---

## 7. CI/CD Automated Deployment Pipeline

The repository uses GitHub Actions (`.github/workflows/deploy.yml`) for automated testing, container image building, and production deployment upon pushing to the `main` branch:

```yaml
name: Production CI/CD Pipeline

on:
  push:
    branches: [ main ]

jobs:
  test-and-validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install Dependencies
        run: |
          pip install -r requirements.txt
      - name: Run Test Suite
        run: |
          pytest tests/ --cov=src
      - name: Validate ML Inference Models
        run: |
          pytest tests/ml_validation/

  deploy-production:
    needs: test-and-validate
    runs-on: ubuntu-latest
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1.0.0
        with:
          host: ${{ secrets.PROD_SERVER_IP }}
          username: ${{ secrets.PROD_SERVER_USER }}
          key: ${{ secrets.PROD_SSH_KEY }}
          script: |
            cd /opt/fitai
            git pull origin main
            docker-compose -f docker-compose.prod.yml up --build -d
            docker-compose -f docker-compose.prod.yml exec -T backend alembic upgrade head
```

---

## 8. Rollback Procedure

If an issue occurs after deploying a new release:

```bash
# Roll back code repository to previous stable tag
git checkout tags/v1.0.0

# Re-build and restart containers
docker-compose -f docker-compose.prod.yml up --build -d

# Downgrade database schema if necessary
docker-compose -f docker-compose.prod.yml exec backend alembic downgrade -1
```

---

## 9. Authorship & Maintenance

- **Author & Architect**: **Ravi Ranjan Singh**
- **Role**: Software Engineer, Software Architect, Full Stack Developer, AI SaaS Developer
- **Repository Maintainer**: **Ravi Ranjan Singh**
