# PAL-adin Deployment Strategy

## Overview

PAL-adin's deployment strategy is designed to provide secure, scalable, and flexible deployment options across multiple platforms while maintaining the highest standards of privacy and performance. The strategy supports development, staging, and production environments with automated deployment pipelines and comprehensive monitoring.

## Deployment Architecture

```mermaid
graph TB
    subgraph "Development Environment"
        DEV_LOCAL[Local Development]
        DEV_DOCKER[Docker Compose Dev]
        DEV_VAGRANT[Vagrant Boxes]
    end
    
    subgraph "CI/CD Pipeline"
        GITHUB[GitHub Actions]
        BUILD[Build & Test]
        SECURITY[Security Scans]
        PACKAGE[Package Artifacts]
    end
    
    subgraph "Staging Environment"
        STAGE_K8S[Kubernetes Staging]
        STAGE_VPS[VPS Staging]
        STAGE_MONITOR[Staging Monitor]
    end
    
    subgraph "Production Environments"
        PROD_K8S[Kubernetes Production]
        PROD_VPS[VPS Production]
        PROD_EDGE[Edge Locations]
    end
    
    subgraph "Infrastructure Providers"
        HETZNER[Hetzner Cloud]
        DIGITAL_OCEAN[Digital Ocean]
        AWS[AWS (Optional)]
        COOLIFY[Coolify Management]
    end
    
    DEV_LOCAL --> GITHUB
    DEV_DOCKER --> GITHUB
    DEV_VAGRANT --> GITHUB
    
    GITHUB --> BUILD
    BUILD --> SECURITY
    SECURITY --> PACKAGE
    
    PACKAGE --> STAGE_K8S
    PACKAGE --> STAGE_VPS
    
    STAGE_K8S --> PROD_K8S
    STAGE_VPS --> PROD_VPS
    
    PROD_K8S --> HETZNER
    PROD_VPS --> HETZNER
    PROD_EDGE --> DIGITAL_OCEAN
    
    COOLIFY --> STAGE_K8S
    COOLIFY --> PROD_K8S
    COOLIFY --> STAGE_VPS
    COOLIFY --> PROD_VPS
```

## Environment Configurations

### 1. Development Environment

#### Local Development Setup
```bash
# scripts/setup-dev.sh
#!/bin/bash

# PAL-adin Local Development Setup

set -e

echo "🚀 Setting up PAL-adin development environment..."

# Check prerequisites
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed."; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose is required but not installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3.11+ is required but not installed."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js 18+ is required but not installed."; exit 1; }

# Clone repository if not exists
if [ ! -d "paladin" ]; then
    echo "📥 Cloning PAL-adin repository..."
    git clone https://github.com/paladin-ai/paladin.git
    cd paladin
else
    cd paladin
    echo "📥 Updating PAL-adin repository..."
    git pull origin main
fi

# Setup environment
echo "⚙️ Setting up environment..."
cp .env.example .env

# Start development services
echo "🐳 Starting development services..."
docker-compose -f docker-compose.dev.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Install backend dependencies
echo "🐍 Setting up Python backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/dev.txt

# Install frontend dependencies
echo "📦 Setting up Node.js frontend..."
cd ../frontend
npm install

# Initialize database
echo "🗄️ Initializing database..."
cd ../backend
source venv/bin/activate
python scripts/init_db.py

# Run initial tests
echo "🧪 Running initial tests..."
pytest tests/ -v

cd ../frontend
npm test

echo "✅ Development environment setup complete!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🗄️ Database: localhost:5432"
echo "🔴 Redis: localhost:6379"
echo ""
echo "🎯 Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run 'npm run dev' in frontend directory"
echo "3. Run 'uvicorn app.main:app --reload' in backend directory"
```

#### Docker Compose Development
```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: paladin-postgres-dev
    environment:
      POSTGRES_DB: paladin_dev
      POSTGRES_USER: paladin
      POSTGRES_PASSWORD: dev_password_123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data_dev:/var/lib/postgresql/data
      - ./backend/scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - paladin-dev

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: paladin-redis-dev
    ports:
      - "6379:6379"
    volumes:
      - redis_data_dev:/data
    networks:
      - paladin-dev

  # Elasticsearch (for search)
  elasticsearch:
    image: elasticsearch:8.8.0
    container_name: paladin-elasticsearch-dev
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data_dev:/usr/share/elasticsearch/data
    networks:
      - paladin-dev

  # MinIO (S3-compatible storage)
  minio:
    image: minio/minio:latest
    container_name: paladin-minio-dev
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin123
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data_dev:/data
    command: server /data --console-address ":9001"
    networks:
      - paladin-dev

  # Backend Development Server
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    container_name: paladin-backend-dev
    environment:
      - DATABASE_URL=postgresql://paladin:dev_password_123@postgres:5432/paladin_dev
      - REDIS_URL=redis://redis:6379
      - ELASTICSEARCH_URL=http://elasticsearch:9200
      - MINIO_ENDPOINT=minio:9000
      - MINIO_ACCESS_KEY=minioadmin
      - MINIO_SECRET_KEY=minioadmin123
      - DEBUG=true
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - /app/venv
    depends_on:
      - postgres
      - redis
      - elasticsearch
      - minio
    networks:
      - paladin-dev
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  # Frontend Development Server
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    container_name: paladin-frontend-dev
    environment:
      - REACT_APP_API_URL=http://localhost:8000
      - REACT_APP_WS_URL=ws://localhost:8000
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - backend
    networks:
      - paladin-dev
    command: npm run dev

volumes:
  postgres_data_dev:
  redis_data_dev:
  elasticsearch_data_dev:
  minio_data_dev:

networks:
  paladin-dev:
    driver: bridge
```

### 2. Production Environment

#### Kubernetes Deployment
```yaml
# deployment/kubernetes/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: paladin
  labels:
    name: paladin
    environment: production

---
# deployment/kubernetes/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: paladin-config
  namespace: paladin
data:
  DATABASE_HOST: "postgres-service"
  DATABASE_PORT: "5432"
  DATABASE_NAME: "paladin_prod"
  REDIS_HOST: "redis-service"
  REDIS_PORT: "6379"
  ELASTICSEARCH_HOST: "elasticsearch-service"
  ELASTICSEARCH_PORT: "9200"
  LOG_LEVEL: "INFO"
  ENVIRONMENT: "production"

---
# deployment/kubernetes/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: paladin-secrets
  namespace: paladin
type: Opaque
data:
  DATABASE_PASSWORD: <base64-encoded-password>
  REDIS_PASSWORD: <base64-encoded-password>
  JWT_SECRET_KEY: <base64-encoded-jwt-secret>
  ENCRYPTION_KEY: <base64-encoded-encryption-key>
  GLM_API_KEY: <base64-encoded-glm-api-key>

---
# deployment/kubernetes/postgres-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: paladin
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        env:
        - name: POSTGRES_DB
          valueFrom:
            configMapKeyRef:
              name: paladin-config
              key: DATABASE_NAME
        - name: POSTGRES_USER
          value: "paladin"
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: paladin-secrets
              key: DATABASE_PASSWORD
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc

---
# deployment/kubernetes/postgres-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: postgres-service
  namespace: paladin
spec:
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432
  type: ClusterIP

---
# deployment/kubernetes/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: paladin
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: paladin/backend:latest
        envFrom:
        - configMapRef:
            name: paladin-config
        env:
        - name: DATABASE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: paladin-secrets
              key: DATABASE_PASSWORD
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: paladin-secrets
              key: JWT_SECRET_KEY
        - name: ENCRYPTION_KEY
          valueFrom:
            secretKeyRef:
              name: paladin-secrets
              key: ENCRYPTION_KEY
        - name: GLM_API_KEY
          valueFrom:
            secretKeyRef:
              name: paladin-secrets
              key: GLM_API_KEY
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

---
# deployment/kubernetes/backend-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: backend-service
  namespace: paladin
spec:
  selector:
    app: backend
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP

---
# deployment/kubernetes/frontend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: paladin
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: paladin/frontend:latest
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"

---
# deployment/kubernetes/frontend-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  namespace: paladin
spec:
  selector:
    app: frontend
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP

---
# deployment/kubernetes/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: paladin-ingress
  namespace: paladin
  annotations:
    kubernetes.io/ingress.class: "nginx"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/security-headers: "true"
    nginx.ingress.kubernetes.io/content-security-policy: "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' wss: https:;"
spec:
  tls:
  - hosts:
    - paladin.ai
    - api.paladin.ai
    secretName: paladin-tls
  rules:
  - host: paladin.ai
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 80
  - host: api.paladin.ai
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: backend-service
            port:
              number: 8000
```

## CI/CD Pipeline

### 1. GitHub Actions Workflow

#### Main Pipeline
```yaml
# .github/workflows/deploy.yml
name: Build and Deploy PAL-adin

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11]
        node-version: [18]
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Set up Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
        cache-dependency-path: frontend/package-lock.json
    
    - name: Install Python dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements/dev.txt
    
    - name: Install Node.js dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Run backend tests
      run: |
        cd backend
        pytest tests/ -v --cov=app --cov-report=xml
    
    - name: Run frontend tests
      run: |
        cd frontend
        npm test -- --coverage --watchAll=false
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        files: ./backend/coverage.xml,./frontend/coverage/lcov.info

  security-scan:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'
    
    - name: Run CodeQL Analysis
      uses: github/codeql-action/analyze@v2
      with:
        languages: python, javascript

  build-and-push:
    runs-on: ubuntu-latest
    needs: [test, security-scan]
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Log in to Container Registry
      uses: docker/login-action@v3
      with:
        registry: ${{ env.REGISTRY }}
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=sha,prefix={{branch}}-
          type=raw,value=latest,enable={{is_default_branch}}
    
    - name: Build and push backend image
      uses: docker/build-push-action@v5
      with:
        context: ./backend
        push: true
        tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/backend:${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
    
    - name: Build and push frontend image
      uses: docker/build-push-action@v5
      with:
        context: ./frontend
        push: true
        tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/frontend:${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy-staging:
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.ref == 'refs/heads/develop'
    environment: staging
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Configure kubectl
      uses: azure/k8s-set-context@v3
      with:
        method: kubeconfig
        kubeconfig: ${{ secrets.KUBE_CONFIG_STAGING }}
    
    - name: Deploy to staging
      run: |
        sed -i 's|IMAGE_TAG|${{ github.sha }}|g' deployment/kubernetes/backend-deployment.yaml
        sed -i 's|IMAGE_TAG|${{ github.sha }}|g' deployment/kubernetes/frontend-deployment.yaml
        kubectl apply -f deployment/kubernetes/ -n paladin-staging
        kubectl rollout status deployment/backend -n paladin-staging
        kubectl rollout status deployment/frontend -n paladin-staging

  deploy-production:
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v4
    
    - name: Configure kubectl
      uses: azure/k8s-set-context@v3
      with:
        method: kubeconfig
        kubeconfig: ${{ secrets.KUBE_CONFIG_PROD }}
    
    - name: Deploy to production
      run: |
        sed -i 's|IMAGE_TAG|${{ github.sha }}|g' deployment/kubernetes/backend-deployment.yaml
        sed -i 's|IMAGE_TAG|${{ github.sha }}|g' deployment/kubernetes/frontend-deployment.yaml
        kubectl apply -f deployment/kubernetes/ -n paladin
        kubectl rollout status deployment/backend -n paladin
        kubectl rollout status deployment/frontend -n paladin
    
    - name: Run smoke tests
      run: |
        chmod +x scripts/smoke-tests.sh
        ./scripts/smoke-tests.sh https://paladin.ai
```

### 2. Smoke Tests

#### Automated Testing Script
```bash
# scripts/smoke-tests.sh
#!/bin/bash

# PAL-adin Smoke Tests

set -e

BASE_URL=${1:-"http://localhost:8000"}
FRONTEND_URL=${2:-"http://localhost:3000"}

echo "🧪 Running PAL-adin smoke tests..."
echo "🔧 Backend URL: $BASE_URL"
echo "🌐 Frontend URL: $FRONTEND_URL"

# Test backend health
echo "📊 Testing backend health..."
curl -f "$BASE_URL/health" || exit 1
echo "✅ Backend health check passed"

# Test backend readiness
echo "📊 Testing backend readiness..."
curl -f "$BASE_URL/ready" || exit 1
echo "✅ Backend readiness check passed"

# Test API documentation
echo "📚 Testing API documentation..."
curl -f "$BASE_URL/docs" || exit 1
echo "✅ API documentation accessible"

# Test frontend
echo "🌐 Testing frontend..."
curl -f "$FRONTEND_URL" || exit 1
echo "✅ Frontend accessible"

# Test database connection
echo "🗄️ Testing database connection..."
curl -f "$BASE_URL/test/db" || exit 1
echo "✅ Database connection successful"

# Test Redis connection
echo "🔴 Testing Redis connection..."
curl -f "$BASE_URL/test/redis" || exit 1
echo "✅ Redis connection successful"

# Test AI integration
echo "🤖 Testing AI integration..."
curl -f -X POST "$BASE_URL/api/v1/test/ai" \
  -H "Content-Type: application/json" \
  -d '{"message": "test"}' || exit 1
echo "✅ AI integration successful"

echo "🎉 All smoke tests passed!"
```

## Infrastructure Management

### 1. Coolify Integration

#### Coolify Configuration
```yaml
# coolify/compose.yml
version: '3.8'

services:
  coolify:
    image: coolify/coolify:latest
    container_name: coolify
    ports:
      - "8000:80"
    volumes:
      - coolify_data:/var/www/html/storage/app
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      - APP_NAME=PAL-adin
      - APP_ENV=production
      - APP_DEBUG=false
      - APP_URL=https://coolify.paladin.ai
    restart: unless-stopped

volumes:
  coolify_data:
```

#### Coolify Application Definition
```json
{
  "name": "PAL-adin Backend",
  "description": "PAL-adin AI Assistant Backend",
  "image": "paladin/backend:latest",
  "ports": [
    {
      "port": 8000,
      "protocol": "http"
    }
  ],
  "environment": {
    "DATABASE_URL": "{{POSTGRES_URL}}",
    "REDIS_URL": "{{REDIS_URL}}",
    "JWT_SECRET_KEY": "{{JWT_SECRET_KEY}}",
    "ENCRYPTION_KEY": "{{ENCRYPTION_KEY}}",
    "GLM_API_KEY": "{{GLM_API_KEY}}"
  },
  "volumes": [
    {
      "path": "/app/data",
      "size": "10GB"
    }
  ],
  "health_check": {
    "path": "/health",
    "interval": 30,
    "timeout": 10,
    "retries": 3
  },
  "deployment": {
    "strategy": "rolling",
    "replicas": 3,
    "auto_deploy": true
  }
}
```

### 2. VPS Deployment

#### Hetzner Cloud Setup
```bash
# scripts/setup-hetzner.sh
#!/bin/bash

# PAL-adin Hetzner Cloud Setup

set -e

# Configuration
SERVER_NAME="paladin-prod-1"
SERVER_TYPE="cpx31"  # 4 vCPU, 8GB RAM, 160GB SSD
SERVER_IMAGE="ubuntu-22.04"
SERVER_LOCATION="nbg1"  # Nuremberg, Germany
FIREWALL_NAME="paladin-firewall"

# Create firewall
echo "🔥 Creating firewall..."
hcloud firewall create --name $FIREWALL_NAME --rules '

[
  {
    "direction": "in",
    "source_ips": ["0.0.0.0/0", "::/0"],
    "destination_ips": ["0.0.0.0/0", "::/0"],
    "protocol": "tcp",
    "port": "22"
  },
  {
    "direction": "in",
    "source_ips": ["0.0.0.0/0", "::/0"],
    "destination_ips": ["0.0.0.0/0", "::/0"],
    "protocol": "tcp",
    "port": "80"
  },
  {
    "direction": "in",
    "source_ips": ["0.0.0.0/0", "::/0"],
    "destination_ips": ["0.0.0.0/0", "::/0"],
    "protocol": "tcp",
    "port": "443"
  }
]

'

# Create server
echo "🖥️ Creating server..."
hcloud server create \
  --name $SERVER_NAME \
  --type $SERVER_TYPE \
  --image $SERVER_IMAGE \
  --location $SERVER_LOCATION \
  --firewall $FIREWALL_NAME \
  --enable-backup \
  --ssh-key paladin-deploy

# Get server IP
SERVER_IP=$(hcloud server describe $SERVER_NAME -o format='{{ .PublicNet.IPv4.IP }}')
echo "🌐 Server IP: $SERVER_IP"

# Wait for server to be ready
echo "⏳ Waiting for server to be ready..."
sleep 60

# Setup server
echo "⚙️ Setting up server..."
ssh root@$SERVER_IP << 'EOF'
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
systemctl enable docker
systemctl start docker

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Create paladin user
useradd -m -s /bin/bash paladin
usermod -aG docker paladin

# Setup directories
mkdir -p /opt/paladin
chown paladin:paladin /opt/paladin

# Setup firewall
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# Setup fail2ban
apt install -y fail2ban
systemctl enable fail2ban
systemctl start fail2ban

EOF

echo "✅ Server setup complete!"
echo "🔑 SSH command: ssh paladin@$SERVER_IP"
```

#### VPS Deployment Script
```bash
# scripts/deploy-vps.sh
#!/bin/bash

# PAL-adin VPS Deployment

set -e

SERVER_IP=${1:-"your-server-ip"}
ENVIRONMENT=${2:-"production"}

echo "🚀 Deploying PAL-adin to VPS..."
echo "🖥️ Server: $SERVER_IP"
echo "🌍 Environment: $ENVIRONMENT"

# Copy files to server
echo "📤 Copying files..."
scp -r . paladin@$SERVER_IP:/opt/paladin/

# Deploy on server
ssh paladin@$SERVER_IP << EOF
cd /opt/paladin

# Pull latest images
docker-compose -f docker-compose.prod.yml pull

# Stop existing services
docker-compose -f docker-compose.prod.yml down

# Start new services
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
sleep 30

# Run database migrations
docker-compose -f docker-compose.prod.yml exec backend python scripts/migrate_db.py

# Check service health
docker-compose -f docker-compose.prod.yml ps

EOF

echo "✅ Deployment complete!"
echo "🌐 Check: https://$SERVER_IP"
```

## Monitoring and Observability

### 1. Prometheus Configuration

#### Prometheus Setup
```yaml
# monitoring/prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "rules/*.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'paladin-backend'
    static_configs:
      - targets: ['backend-service:8000']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'paladin-frontend'
    static_configs:
      - targets: ['frontend-service:80']
    metrics_path: '/metrics'
    scrape_interval: 30s

  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']

  - job_name: 'redis'
    static_configs:
      - targets: ['redis-exporter:9121']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

#### Alert Rules
```yaml
# monitoring/prometheus/rules/paladin.yml
groups:
  - name: paladin.rules
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors per second"

      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
          description: "95th percentile response time is {{ $value }} seconds"

      - alert: DatabaseDown
        expr: up{job="postgres"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Database is down"
          description: "PostgreSQL database has been down for more than 1 minute"

      - alert: RedisDown
        expr: up{job="redis"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Redis is down"
          description: "Redis cache has been down for more than 1 minute"

      - alert: HighMemoryUsage
        expr: (node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes > 0.9
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High memory usage"
          description: "Memory usage is {{ $value | humanizePercentage }}"

      - alert: HighCPUUsage
        expr: 100 - (avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High CPU usage"
          description: "CPU usage is {{ $value }}%"
```

### 2. Grafana Dashboards

#### Dashboard Configuration
```json
{
  "dashboard": {
    "title": "PAL-adin Overview",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{status}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "50th percentile"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "singlestat",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m])",
            "legendFormat": "Error Rate"
          }
        ]
      },
      {
        "title": "Database Connections",
        "type": "graph",
        "targets": [
          {
            "expr": "pg_stat_database_numbackends",
            "legendFormat": "Active Connections"
          }
        ]
      },
      {
        "title": "Memory Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes) / node_memory_MemTotal_bytes",
            "legendFormat": "Memory Usage"
          }
        ]
      },
      {
        "title": "CPU Usage",
        "type": "graph",
        "targets": [
          {
            "expr": "100 - (avg by(instance) (rate(node_cpu_seconds_total{mode=\"idle\"}[5m])) * 100)",
            "legendFormat": "CPU Usage"
          }
        ]
      }
    ]
  }
}
```

## Security and Compliance

### 1. SSL/TLS Configuration

#### Nginx SSL Configuration
```nginx
# deployment/nginx/ssl.conf
server {
    listen 443 ssl http2;
    server_name paladin.ai api.paladin.ai;

    # SSL Configuration
    ssl_certificate /etc/ssl/certs/paladin.ai.crt;
    ssl_certificate_key /etc/ssl/private/paladin.ai.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self'; connect-src 'self' wss: https:;" always;

    # API Proxy
    location /api/ {
        proxy_pass http://backend-service:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Frontend
    location / {
        proxy_pass http://frontend-service:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name paladin.ai api.paladin.ai;
    return 301 https://$server_name$request_uri;
}
```

### 2. Backup and Recovery

#### Automated Backup Script
```bash
# scripts/backup.sh
#!/bin/bash

# PAL-adin Backup Script

set -e

BACKUP_DIR="/opt/backups/paladin"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="paladin_backup_$DATE"

# Create backup directory
mkdir -p $BACKUP_DIR

echo "🗄️ Starting PAL-adin backup..."

# Database backup
echo "💾 Backing up database..."
docker exec paladin-postgres pg_dump -U paladin paladin_prod | gzip > $BACKUP_DIR/${BACKUP_NAME}_db.sql.gz

# Redis backup
echo "🔴 Backing up Redis..."
docker exec paladin-redis redis-cli BGSAVE
docker cp paladin-redis:/data/dump.rdb $BACKUP_DIR/${BACKUP_NAME}_redis.rdb

# File storage backup
echo "📁 Backing up file storage..."
tar -czf $BACKUP_DIR/${BACKUP_NAME}_files.tar.gz /opt/paladin/data

# Configuration backup
echo "⚙️ Backing up configuration..."
tar -czf $BACKUP_DIR/${BACKUP_NAME}_config.tar.gz /opt/paladin/config

# Upload to cloud storage (optional)
if [ -n "$AWS_S3_BUCKET" ]; then
    echo "☁️ Uploading to S3..."
    aws s3 cp $BACKUP_DIR/${BACKUP_NAME}_db.sql.gz s3://$AWS_S3_BUCKET/backups/
    aws s3 cp $BACKUP_DIR/${BACKUP_NAME}_redis.rdb s3://$AWS_S3_BUCKET/backups/
    aws s3 cp $BACKUP_DIR/${BACKUP_NAME}_files.tar.gz s3://$AWS_S3_BUCKET/backups/
    aws s3 cp $BACKUP_DIR/${BACKUP_NAME}_config.tar.gz s3://$AWS_S3_BUCKET/backups/
fi

# Clean old backups (keep last 7 days)
echo "🧹 Cleaning old backups..."
find $BACKUP_DIR -name "paladin_backup_*" -mtime +7 -delete

echo "✅ Backup completed: $BACKUP_NAME"
```

This comprehensive deployment strategy ensures PAL-adin can be deployed securely, scaled efficiently, and monitored effectively across various environments while maintaining the highest standards of security and reliability.