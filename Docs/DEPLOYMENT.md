# AI Agent System - Deployment Guide

## Overview

This document provides comprehensive instructions for deploying the AI Agent System to various environments, from development to production.

## Deployment Environments

### 1. Development Environment

#### Local Development
- **Purpose**: Development and testing
- **Database**: Local MongoDB instance
- **Web Server**: Flask development server
- **Email**: Console output or test email service
- **Security**: Development keys and settings

#### Setup Instructions
```bash
# Clone repository
git clone <repository-url>
cd A_I-Agent-master

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with development settings

# Run application
python app.py
```

### 2. Staging Environment

#### Purpose
- Pre-production testing
- Quality assurance
- Performance testing
- User acceptance testing

#### Recommended Configuration
- **Server**: Cloud VM (AWS EC2, Google Cloud, Azure)
- **Database**: MongoDB Atlas or dedicated server
- **Web Server**: Gunicorn with Nginx reverse proxy
- **Email**: Production email service (Brevo)
- **Security**: Staging certificates and keys

### 3. Production Environment

#### Purpose
- Live user access
- High availability
- Performance optimization
- Security hardening

#### Recommended Configuration
- **Server**: Load-balanced cluster
- **Database**: MongoDB Atlas cluster or replica set
- **Web Server**: Gunicorn with Nginx reverse proxy
- **Email**: Production email service (Brevo)
- **Security**: SSL certificates, hardened configuration

## Deployment Options

### 1. Traditional Deployment

#### Server Requirements
- **Operating System**: Ubuntu 20.04 LTS or newer, CentOS 8+, or Windows Server 2019+
- **RAM**: 4GB minimum (8GB recommended)
- **Storage**: 20GB available disk space
- **Python**: 3.8 or higher
- **MongoDB**: 4.4 or higher

#### Installation Steps

##### 1. Server Preparation
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and Git
sudo apt install python3 python3-pip git -y

# Install MongoDB (if hosting locally)
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

##### 2. Application Deployment
```bash
# Create application user
sudo useradd -r -s /bin/false aiagent

# Clone repository
sudo mkdir -p /opt/ai-agent-system
sudo git clone <repository-url> /opt/ai-agent-system
sudo chown -R aiagent:aiagent /opt/ai-agent-system

# Create virtual environment
cd /opt/ai-agent-system
sudo -u aiagent python3 -m venv venv
sudo -u aiagent venv/bin/pip install -r requirements.txt

# Configure environment
sudo -u aiagent cp .env.example .env
# Edit .env with production settings
```

##### 3. Web Server Configuration (Nginx + Gunicorn)
```bash
# Install Nginx
sudo apt install nginx -y

# Install Gunicorn
sudo -u aiagent venv/bin/pip install gunicorn

# Create Gunicorn configuration
sudo tee /opt/ai-agent-system/gunicorn.conf.py << EOF
bind = "127.0.0.1:8000"
workers = 4
user = "aiagent"
group = "aiagent"
EOF

# Create systemd service
sudo tee /etc/systemd/system/aiagent.service << EOF
[Unit]
Description=AI Agent System
After=network.target

[Service]
User=aiagent
Group=aiagent
WorkingDirectory=/opt/ai-agent-system
ExecStart=/opt/ai-agent-system/venv/bin/gunicorn -c gunicorn.conf.py app:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
sudo tee /etc/nginx/sites-available/aiagent << EOF
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /opt/ai-agent-system/static/;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/aiagent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Start application
sudo systemctl enable aiagent
sudo systemctl start aiagent
```

### 2. Containerized Deployment (Docker)

#### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - MONGO_URI=mongodb://mongo:27017/ai_agent_system
      - SECRET_KEY=your-secret-key
    depends_on:
      - mongo
    volumes:
      - ./static:/app/static

  mongo:
    image: mongo:4.4
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

#### Deployment Commands
```bash
# Build and run
docker-compose up -d

# Scale web service
docker-compose up -d --scale web=3
```

### 3. Cloud Platform Deployment

#### Heroku
```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Set environment variables
heroku config:set MONGO_URI=your-mongo-uri
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main
```

#### AWS Elastic Beanstalk
1. Install EB CLI
2. Initialize application:
   ```bash
   eb init
   eb create aiagent-env
   eb deploy
   ```

#### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/aiagent
gcloud run deploy --image gcr.io/PROJECT-ID/aiagent --platform managed
```

## Database Deployment

### MongoDB Atlas (Recommended for Production)

#### Setup Steps
1. Create MongoDB Atlas account
2. Create new cluster
3. Configure database access:
   - Add database user
   - Configure network access
4. Get connection string
5. Update application configuration

#### Connection String Format
```
mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/ai_agent_system?retryWrites=true&w=majority
```

### Self-Hosted MongoDB

#### Replica Set Configuration
```javascript
// Initialize replica set
rs.initiate({
  _id: "aiagent-rs",
  members: [
    { _id: 0, host: "mongo1:27017" },
    { _id: 1, host: "mongo2:27017" },
    { _id: 2, host: "mongo3:27017" }
  ]
})
```

## SSL/TLS Configuration

### Let's Encrypt with Certbot
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Manual Certificate Installation
```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    ssl_prefer_server_ciphers off;
    
    # ... rest of configuration
}
```

## Monitoring and Logging

### Application Monitoring

#### Health Checks
```python
@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        db = get_db_connection()
        if db is None:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500
        
        # Check if collections exist
        collections = db.list_collection_names()
        required_collections = ['usertable', 'course_enrollments']
        missing_collections = [col for col in required_collections if col not in collections]
        
        if missing_collections:
            return jsonify({"status": "error", "message": f"Missing collections: {missing_collections}"}), 500
            
        return jsonify({"status": "healthy", "database": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
```

#### Logging Configuration
```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
if not app.debug:
    file_handler = RotatingFileHandler('logs/aiagent.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('AI Agent System startup')
```

### Infrastructure Monitoring

#### System Metrics
- CPU usage
- Memory usage
- Disk space
- Network I/O
- Application response times

#### Tools
- **Prometheus** + **Grafana** for metrics
- **ELK Stack** for log aggregation
- **New Relic** or **Datadog** for APM
- **UptimeRobot** for external monitoring

## Backup and Disaster Recovery

### Database Backup Strategy

#### MongoDB Backup
```bash
# Manual backup
mongodump --host localhost:27017 --db ai_agent_system --out /backup/

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
mongodump --host localhost:27017 --db ai_agent_system --out /backup/mongo_$DATE/
find /backup/ -name "mongo_*" -mtime +7 -exec rm -rf {} \;
```

#### Scheduled Backups with Cron
```bash
# Daily backup at 2 AM
0 2 * * * /opt/ai-agent-system/backup.sh
```

### Application Backup

#### Code and Configuration
- Version control all code
- Backup environment files (encrypted)
- Document deployment procedures
- Maintain infrastructure as code

### Disaster Recovery Plan

#### Recovery Steps
1. Restore database from latest backup
2. Deploy application code
3. Configure environment variables
4. Test application functionality
5. Update DNS records if needed

#### RTO and RPO
- **Recovery Time Objective (RTO)**: 4 hours
- **Recovery Point Objective (RPO)**: 24 hours

## Security Considerations for Deployment

### Production Security Hardening

#### Application-Level Security
- Set `DEBUG = False` in production
- Use strong, randomly generated secrets
- Implement proper error handling
- Sanitize all user inputs

#### Server-Level Security
- Keep system updated with security patches
- Configure firewall (ufw, iptables)
- Disable unnecessary services
- Use SSH key authentication only

#### Network Security
- Use private networks for internal communication
- Implement network segmentation
- Use VPN for administrative access
- Enable DDoS protection

## Performance Optimization

### Caching Strategy

#### In-Memory Caching
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/expensive-operation')
@cache.cached(timeout=300)  # Cache for 5 minutes
def expensive_operation():
    # Expensive operation here
    pass
```

#### CDN for Static Assets
- Use Cloudflare, AWS CloudFront, or Google Cloud CDN
- Configure cache headers for static files
- Enable compression (gzip, Brotli)

### Database Optimization

#### Indexing
```javascript
// Create compound indexes for common queries
db.course_enrollments.createIndex({ "user_id": 1, "course_id": 1 })
db.usertable.createIndex({ "email": 1, "status": 1 })
```

#### Query Optimization
- Use projection to limit returned fields
- Implement pagination for large result sets
- Monitor slow queries with profiling

## Scaling Strategies

### Horizontal Scaling

#### Load Balancing
```nginx
upstream aiagent_backend {
    server 10.0.0.10:8000;
    server 10.0.0.11:8000;
    server 10.0.0.12:8000;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://aiagent_backend;
        # ... proxy configuration
    }
}
```

#### Database Scaling
- MongoDB sharding for large datasets
- Read replicas for read-heavy workloads
- Connection pooling for efficient database access

### Vertical Scaling
- Upgrade server resources (CPU, RAM, storage)
- Optimize application code
- Database performance tuning

## Environment-Specific Configuration

### Configuration Management

#### Environment Variables
```python
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MONGO_URI = os.environ.get('MONGO_URI')
    BREVO_API_KEY = os.environ.get('BREVO_API_KEY')
    
class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
class TestingConfig(Config):
    TESTING = True
```

#### Configuration per Environment
- **Development**: Debug enabled, local database
- **Staging**: Production-like settings, test data
- **Production**: Optimized settings, real database

## Deployment Checklist

### Pre-Deployment
- [ ] Code review completed
- [ ] All tests passing
- [ ] Security scan performed
- [ ] Performance testing completed
- [ ] Backup strategy verified
- [ ] Rollback plan documented

### Deployment
- [ ] Maintenance window scheduled
- [ ] Database migrations applied
- [ ] Configuration updated
- [ ] Application deployed
- [ ] Smoke tests performed
- [ ] Monitoring configured

### Post-Deployment
- [ ] User acceptance testing
- [ ] Performance monitoring
- [ ] Error rate monitoring
- [ ] User feedback collection
- [ ] Documentation updated

## Troubleshooting Common Issues

### Deployment Failures
1. **Dependency Issues**: Verify requirements.txt and Python version
2. **Database Connection**: Check connection string and network access
3. **Permission Errors**: Verify file permissions and user accounts
4. **Port Conflicts**: Check for processes using required ports

### Runtime Issues
1. **Memory Leaks**: Monitor memory usage, restart workers periodically
2. **Database Locks**: Check for long-running queries, optimize indexes
3. **Slow Performance**: Profile application, optimize queries
4. **Email Delivery**: Verify API keys, check spam filters

## Conclusion

This deployment guide provides a comprehensive approach to deploying the AI Agent System across different environments. The key to successful deployment is careful planning, thorough testing, and continuous monitoring. Regular updates to this guide based on deployment experiences will help maintain a robust and reliable system.