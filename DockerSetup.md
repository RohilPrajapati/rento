# Rento — Docker Setup Guide

This guide covers Docker setup for both development and production environments for the Rento electricity billing app.

## Prerequisites

- Docker installed on your system
- Docker Compose installed
- Git (to clone the repository)

## Setup Instructions

### Development Environment

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd rento
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env.dev
   # Edit .env.dev with your development settings
   ```

3. **Build and run the development container**
   ```bash
   docker-compose -f docker-compose.yml up --build
   ```

4. **Access the application**
   - Open your browser and go to `http://localhost:8000`

5. **Create superuser (in a new terminal)**
   ```bash
   docker-compose -f docker-compose.yml exec web python manage.py createsuperuser
   ```

6. **Useful development commands**
   ```bash
   # Make migrations
   docker-compose -f docker-compose.yml exec web python manage.py makemigrations
   
   # Apply migrations
   docker-compose -f docker-compose.yml exec web python manage.py migrate
   
   # Access shell
   docker-compose -f docker-compose.yml exec web python manage.py shell
   
   # Stop containers
   docker-compose -f docker-compose.yml down
   
   # View logs
   docker-compose -f docker-compose.yml logs -f
   ```

### Production Environment

1. **Prepare production environment**
   ```bash
   cp .env.example .env.prod
   # Edit .env.prod with your production settings
   ```

2. **Build and run production containers**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d --build
   ```

3. **Create superuser**
   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
   ```

4. **Useful production commands**
   ```bash
   # Collect static files
   docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
   
   # Apply migrations
   docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
   
   # View logs
   docker-compose -f docker-compose.prod.yml logs -f
   
   # Stop containers
   docker-compose -f docker-compose.prod.yml down
   
   # Restart containers
   docker-compose -f docker-compose.prod.yml restart
   ```

## Quick Commands Reference

### Development
```bash
# Start development server
docker-compose -f docker-compose.yml up

# Stop development server
docker-compose -f docker-compose.yml down
```

### Production
```bash
# Start production server
docker-compose -f docker-compose.prod.yml up -d

# Stop production server
docker-compose -f docker-compose.prod.yml down
```