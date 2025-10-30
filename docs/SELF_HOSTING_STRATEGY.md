# PAL-adin Self-Hosting Strategy

## 🏠 Self-Hosting Philosophy

PAL-adin is designed to be completely self-hostable, giving users complete control over their AI assistant infrastructure. This aligns with UNOWN principles of data sovereignty, privacy, and independence from corporate services.

### Core Principles
- **Complete Data Control**: User owns all data, no third-party access
- **Privacy by Default**: All processing happens locally when possible
- **Infrastructure Independence**: No reliance on cloud services or SaaS
- **Cost Transparency**: Users know exactly what they're paying for
- **Customization Freedom**: Modify, extend, or fork as needed

## 🏠 Self-Hosting Options

### Option 1: Single Server Deployment
**Best For**: Individual users or small groups wanting maximum control

#### Hardware Requirements
- **Minimum**: 4-core CPU, 8GB RAM, 100GB SSD
- **Recommended**: 8-core CPU, 16GB RAM, 500GB NVMe SSD
- **Network**: Stable broadband connection (25Mbps+ upload)

#### Software Stack
```yaml
# docker-compose.self-hosted.yml
version: '3.8'

services:
  # PAL-adin Backend
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.self-hosted
    environment:
      - DATABASE_URL=postgresql://paladin:${DB_PASSWORD}@postgres:5432/paladin
      - REDIS_URL=redis://redis:6379
      - AI_MODELS_PATH=/app/models
      - LOCAL_AI_ONLY=true
    volumes:
      - ./data:/app/data
      - ./models:/app/models
      - ./config:/app/config
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
      - ollama
    restart: unless-stopped

  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=paladin
      - POSTGRES_USER=paladin
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  # Redis Cache
  redis:
    image: eqalpha/keydb:latest
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    restart: unless-stopped

  # Local AI Models (Ollama)
  ollama:
    image: ollama/ollama:latest
    environment:
      - OLLAMA_MODELS=/app/models
    volumes:
      - ollama_data:/root/.ollama
      - ./models:/app/models
    ports:
      - "11434:11434"
    restart: unless-stopped

  # Web Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.self-hosted
    environment:
      - VITE_API_URL=http://localhost:8000
      - VITE_WS_URL=ws://localhost:8000
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  ollama_data:
  models:
  config:
  data:

networks:
  default:
    driver: bridge
```

#### Installation Script
```bash
#!/bin/bash
# install-self-hosted.sh
# PAL-adin Self-Hosting Installation Script

set -e

echo "🏠 Installing PAL-adin Self-Hosted Edition..."

# Check system requirements
check_requirements() {
    echo "🔍 Checking system requirements..."
    
    # Check Docker
    if ! command -v docker; then
        echo "❌ Docker is required. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose; then
        echo "❌ Docker Compose is required. Please install Docker Compose first."
        exit 1
    fi
    
    # Check available disk space
    available_space=$(df -BG / | awk 'NR==1 {print $4}')
    if [ "$available_space" -lt 100 ]; then
        echo "⚠️ Warning: Less than 100GB available disk space detected."
    fi
    
    echo "✅ System requirements check passed"
}

# Create directory structure
setup_directories() {
    echo "📁 Creating directory structure..."
    
    mkdir -p paladin/{backend,frontend,data,models,config,backups}
    cd paladin
    
    echo "✅ Directory structure created"
}

# Generate secure passwords
generate_passwords() {
    echo "🔐 Generating secure passwords..."
    
    # Generate database password
    DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-32)
    
    # Generate encryption keys
    ENCRYPTION_KEY=$(openssl rand -base64 64)
    JWT_SECRET=$(openssl rand -base64 64)
    
    # Save to .env file
    cat > .env << EOF
# PAL-adin Self-Hosted Configuration
DATABASE_URL=postgresql://paladin:${DB_PASSWORD}@postgres:5432/paladin
REDIS_URL=redis://redis:6379
ENCRYPTION_KEY=${ENCRYPTION_KEY}
JWT_SECRET=${JWT_SECRET}
LOCAL_AI_ONLY=true
EOF
    
    chmod 600 .env
    echo "✅ Secure configuration generated"
}

# Download and setup components
setup_components() {
    echo "📦 Setting up PAL-adin components..."
    
    # Clone repository
    if [ ! -d "backend" ]; then
        git clone https://github.com/unown-ai/paladin.git .
    fi
    
    # Download AI models
    echo "🤖 Downloading AI models..."
    mkdir -p models
    
    # Download Llama 2 7B (4-bit quantized)
    wget -O models/llama2-7b-q4_0.gguf "https://huggingface.co/TheBloke/openllama/resolve/main/llama-2-7b-chat.gguf"
    
    # Download Mistral 7B (4-bit quantized)
    wget -O models/mistral-7b-instruct-v0.1.Q4_K_M.gguf "https://huggingface.co/TheBloke/mistral-7B-Instruct-v0.1/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
    
    echo "✅ AI models downloaded"
}

# Deploy services
deploy_services() {
    echo "🚀 Deploying PAL-adin services..."
    
    # Build and start services
    docker-compose -f docker-compose.self-hosted.yml up -d
    
    # Wait for services to be ready
    echo "⏳ Waiting for services to start..."
    sleep 30
    
    # Check service health
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ PAL-adin backend is healthy"
    else
        echo "❌ PAL-adin backend failed to start"
        return 1
    fi
    
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        echo "✅ PAL-adin frontend is accessible"
    else
        echo "❌ PAL-adin frontend failed to start"
        return 1
    fi
    
    echo "✅ PAL-adin deployment completed"
    echo ""
    echo "🌐 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
}

# Setup automatic updates
setup_updates() {
    echo "🔄 Setting up automatic updates..."
    
    # Create update script
    cat > update-paladin.sh << 'EOF'
#!/bin/bash
# PAL-adin Auto-Updater

echo "🔄 Checking for PAL-adin updates..."

# Backup current data
docker-compose exec postgres pg_dump -U paladin paladin > backup_\$(date +%Y%m%d_%H%M%S).sql

# Pull latest changes
git pull origin main

# Update services
docker-compose pull
docker-compose up -d

echo "✅ PAL-adin updated successfully"
EOF
    
    chmod +x update-paladin.sh
    
    # Add to crontab (weekly updates)
    (crontab -l 2>/dev/null; echo "0 3 * * 1 /path/to/paladin/update-paladin.sh") | crontab -
    
    echo "✅ Automatic updates configured"
}

# Main installation flow
main() {
    echo "🏠 PAL-adin Self-Hosting Installation"
    echo "======================================"
    
    check_requirements
    setup_directories
    generate_passwords
    setup_components
    deploy_services
    setup_updates
    
    echo ""
    echo "🎉 PAL-adin Self-Hosted Edition installation completed!"
    echo ""
    echo "📖 Next steps:"
    echo "1. Access PAL-adin at http://localhost:3000"
    echo "2. Create your account and complete setup"
    echo "3. Configure AI models and privacy settings"
    echo "4. Enjoy your private AI assistant!"
    echo ""
    echo "📚 Documentation: https://docs.paladin.ai/self-hosting"
    echo "🐛 Issues: https://github.com/unown-ai/paladin/issues"
    echo "======================================"
}

# Run installation
main "$@"
```

### Option 2: Raspberry Pi Cluster
**Best For**: Privacy-focused users wanting low-cost, low-power setup

#### Hardware Requirements
- **Minimum**: Raspberry Pi 4B (4GB RAM, 2GHz ARM Cortex-A72)
- **Recommended**: 3x Raspberry Pi 4B (12GB total RAM)
- **Storage**: 256GB+ microSD card or USB SSD
- **Network**: Ethernet connection preferred

#### Cluster Configuration
```yaml
# docker-compose.pi-cluster.yml
version: '3.8'

services:
  # Load Balancer (Pi 1)
  load-balancer:
    build:
      context: ./load-balancer
      dockerfile: Dockerfile.pi
    environment:
      - BACKEND_NODES=pi2:8000,pi3:8000
    ports:
      - "80:80"
    depends_on:
      - backend-pi2
      - backend-pi3
    restart: unless-stopped
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.hostname == pi1

  # Backend Nodes (Pi 2 & 3)
  backend-pi2:
    build:
      context: ./backend
      dockerfile: Dockerfile.pi
    environment:
      - DATABASE_URL=sqlite:///data/paladin.db
      - AI_MODELS_PATH=/app/models
      - LOCAL_AI_ONLY=true
      - CLUSTER_MODE=true
    volumes:
      - ./data-pi2:/app/data
      - ./models:/app/models
    ports:
      - "8000:8000"
    restart: unless-stopped
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.hostname == pi2

  backend-pi3:
    build:
      context: ./backend
      dockerfile: Dockerfile.pi
    environment:
      - DATABASE_URL=sqlite:///data/paladin.db
      - AI_MODELS_PATH=/app/models
      - LOCAL_AI_ONLY=true
      - CLUSTER_MODE=true
    volumes:
      - ./data-pi3:/app/data
      - ./models:/app/models
    ports:
      - "8000:8000"
    restart: unless-stopped
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.hostname == pi3

  # Shared Storage
  shared-storage:
    image: nginx:alpine
    volumes:
      - ./shared-data:/usr/share/nginx/html
    ports:
      - "8080:80"
    restart: unless-stopped

volumes:
  data-pi2:
  data-pi3:
  models:
  shared-data:

networks:
  default:
    driver: bridge
```

### Option 3: Hybrid Cloud + Local
**Best For**: Users wanting cloud convenience with local privacy

#### Architecture
```mermaid
graph TB
    subgraph "Local Infrastructure"
        LOCAL_AI[Local AI Models]
        LOCAL_DB[Local Database]
        LOCAL_STORAGE[Local Storage]
    end
    
    subgraph "Cloud Infrastructure"
        CLOUD_API[Cloud API Gateway]
        CLOUD_DB[Cloud Database]
        CLOUD_STORAGE[Cloud Storage]
    end
    
    subgraph "User Interface"
        FRONTEND[Web/Mobile Frontend]
        SYNC[Sync Service]
    end
    
    FRONTEND --> SYNC
    SYNC --> LOCAL_AI
    SYNC --> LOCAL_DB
    SYNC --> LOCAL_STORAGE
    
    FRONTEND --> CLOUD_API
    CLOUD_API --> CLOUD_DB
    CLOUD_API --> CLOUD_STORAGE
```

#### Configuration
```python
# hybrid_config.py
class HybridConfig:
    """Configuration for hybrid cloud + local deployment"""
    
    def __init__(self):
        self.privacy_settings = {
            'local_processing': True,
            'cloud_fallback': True,
            'data_encryption': True,
            'sync_encryption': True
        }
        
        self.ai_routing = {
            'privacy_sensitive': 'local_only',
            'computation_intensive': 'cloud',
            'creative_tasks': 'local',
            'factual_queries': 'hybrid',
        }
        
        self.sync_settings = {
            'real_time': True,
            'bandwidth_optimization': True,
            'conflict_resolution': 'local_wins',
        }
    
    def should_process_locally(self, request_type: str, content: str) -> bool:
        """Determine if request should be processed locally"""
        
        # Privacy-sensitive content always local
        if self._is_privacy_sensitive(content):
            return True
        
        # Check routing rules
        routing_rule = self.ai_routing.get(request_type, 'hybrid')
        
        if routing_rule == 'local_only':
            return True
        elif routing_rule == 'cloud':
            return False
        else:  # hybrid
            return self._has_local_resources(request_type)
    
    def _is_privacy_sensitive(self, content: str) -> bool:
        """Check if content is privacy-sensitive"""
        
        privacy_keywords = [
            'personal', 'private', 'confidential',
            'medical', 'health', 'financial',
            'password', 'secret', 'diary'
        ]
        
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in privacy_keywords)
    
    def _has_local_resources(self, request_type: str) -> bool:
        """Check if local resources are available for request type"""
        
        # Check if local AI models are available
        if not self._local_models_available():
            return False
        
        # Check if local storage is available
        if not self._local_storage_available():
            return False
        
        return True
```

## 🔒 Security Considerations

### Network Security
```bash
# firewall-setup.sh
#!/bin/bash
# PAL-adin Self-Hosting Firewall Setup

echo "🔒 Configuring firewall for PAL-adin..."

# Basic rules
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 8000/tcp  # Backend API
ufw allow 3000/tcp  # Frontend

# Rate limiting
ufw limit 8000/tcp 100 60  # 100 connections per minute
ufw limit 3000/tcp 50 60   # 50 connections per minute

# Enable firewall
ufw enable

echo "✅ Firewall configured"
```

### SSL/TLS Setup
```bash
# ssl-setup.sh
#!/bin/bash
# PAL-adin SSL/TLS Setup

DOMAIN=${1:-"localhost"}
EMAIL=${2:-"admin@localhost"}

echo "🔐 Setting up SSL/TLS for $DOMAIN..."

# Generate self-signed certificate (for development)
if [ "$DOMAIN" = "localhost" ]; then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout paladin.key -out paladin.crt \
        -subj "/C=US/ST=Local/L=Local/O=PAL-adin/CN=$DOMAIN/email=$EMAIL"
    
    echo "✅ Self-signed certificate generated"
else
    # Use Let's Encrypt for production
    certbot certonly --standalone -d $DOMAIN --email $EMAIL --agree-tos --non-interactive
    echo "✅ Let's Encrypt certificate obtained"
fi

# Configure nginx for SSL
cat > nginx-ssl.conf << EOF
server {
    listen 443 ssl http2;
    server_name $DOMAIN;
    
    ssl_certificate /etc/ssl/certs/paladin.crt;
    ssl_certificate_key /etc/ssl/private/paladin.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$ssl_client_s_dn;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}

server {
    listen 80;
    server_name $DOMAIN;
    return 301 https://\$server_name\$request_uri;
}
EOF

echo "✅ SSL configuration completed"
```

## 📊 Performance Optimization

### Resource Monitoring
```python
# performance_monitor.py
import psutil
import time
import asyncio
from typing import Dict, List

class PerformanceMonitor:
    """Monitor and optimize PAL-adin performance"""
    
    def __init__(self):
        self.metrics_history = []
        self.optimization_suggestions = []
    
    async def collect_metrics(self) -> Dict[str, float]:
        """Collect system performance metrics"""
        
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_io': psutil.net_io_counters()._asdict(),
            'temperature': self._get_temperature(),
            'gpu_usage': self._get_gpu_usage(),
            'timestamp': time.time()
        }
    
    async def optimize_performance(self):
        """Automatically optimize system performance"""
        
        while True:
            metrics = await self.collect_metrics()
            
            # Check for performance issues
            issues = self._identify_performance_issues(metrics)
            
            if issues:
                suggestions = self._generate_optimization_suggestions(issues)
                await self._apply_optimizations(suggestions)
            
            # Store metrics
            self.metrics_history.append(metrics)
            
            # Keep only last 1000 entries
            if len(self.metrics_history) > 1000:
                self.metrics_history = self.metrics_history[-1000:]
            
            await asyncio.sleep(60)  # Check every minute
    
    def _identify_performance_issues(self, metrics: Dict[str, float]) -> List[str]:
        """Identify performance issues"""
        
        issues = []
        
        if metrics['cpu_percent'] > 80:
            issues.append('high_cpu_usage')
        
        if metrics['memory_percent'] > 85:
            issues.append('high_memory_usage')
        
        if metrics['disk_usage'] > 90:
            issues.append('high_disk_usage')
        
        if metrics.get('temperature', 0) > 70:
            issues.append('high_temperature')
        
        if metrics.get('gpu_usage', 0) > 90:
            issues.append('high_gpu_usage')
        
        return issues
    
    def _generate_optimization_suggestions(self, issues: List[str]) -> List[str]:
        """Generate optimization suggestions"""
        
        suggestions = []
        
        for issue in issues:
            if issue == 'high_cpu_usage':
                suggestions.append('Reduce AI model complexity or use smaller models')
            elif issue == 'high_memory_usage':
                suggestions.append('Clear conversation history or increase swap space')
            elif issue == 'high_disk_usage':
                suggestions.append('Clean up old data or increase storage capacity')
            elif issue == 'high_temperature':
                suggestions.append('Improve cooling or reduce CPU load')
            elif issue == 'high_gpu_usage':
                suggestions.append('Use quantized models or reduce batch size')
        
        return suggestions
    
    async def _apply_optimizations(self, suggestions: List[str]):
        """Apply performance optimizations"""
        
        for suggestion in suggestions:
            if 'Reduce AI model complexity' in suggestion:
                # Switch to smaller model
                await self._switch_to_smaller_model()
            elif 'Clear conversation history' in suggestion:
                # Clear old conversations
                await self._clear_old_conversations()
            # Add more optimizations as needed
```

## 🔄 Maintenance & Updates

### Automated Backup System
```bash
# backup-system.sh
#!/bin/bash
# PAL-adin Automated Backup System

BACKUP_DIR="/opt/paladin/backups"
RETENTION_DAYS=30
ENCRYPTION_KEY_FILE="/opt/paladin/.backup_key"

echo "💾 Starting PAL-adin backup system..."

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Generate encryption key if not exists
if [ ! -f "$ENCRYPTION_KEY_FILE" ]; then
    openssl rand -out "$ENCRYPTION_KEY_FILE" 32
fi

# Backup database
echo "📊 Backing up database..."
docker exec postgres pg_dump -U paladin paladin | gzip > "$BACKUP_DIR/database_$(date +%Y%m%d_%H%M%S).sql.gz"

# Backup user data
echo "👤 Backing up user data..."
tar -czf "$BACKUP_DIR/user_data_$(date +%Y%m%d_%H%M%S).tar.gz" /opt/paladin/data

# Backup configuration
echo "⚙️ Backing up configuration..."
tar -czf "$BACKUP_DIR/config_$(date +%Y%m%d_%H%M%S).tar.gz" /opt/paladin/config

# Encrypt backups
echo "🔐 Encrypting backups..."
for backup in "$BACKUP_DIR"/*.gz; do
    openssl enc -aes-256-cbc -salt -in "$backup" -out "$backup.enc" -pass file:"$ENCRYPTION_KEY_FILE"
    rm "$backup"
done

# Clean old backups
echo "🧹 Cleaning old backups..."
find "$BACKUP_DIR" -name "*.enc" -mtime +$RETENTION_DAYS -delete

echo "✅ Backup completed"
```

### Update Management
```python
# update_manager.py
import asyncio
import hashlib
import requests
from typing import Dict, Any

class UpdateManager:
    """Manage PAL-adin updates with security verification"""
    
    def __init__(self):
        self.current_version = self._get_current_version()
        self.update_channel = "stable"
        self.security_keys = self._load_security_keys()
    
    async def check_for_updates(self) -> Dict[str, Any]:
        """Check for available updates"""
        
        try:
            # Fetch update manifest
            response = requests.get(
                "https://updates.paladin.ai/manifest.json",
                timeout=10
            )
            response.raise_for_status()
            
            manifest = response.json()
            
            # Verify manifest signature
            if not self._verify_manifest_signature(manifest):
                return {
                    'update_available': False,
                    'error': 'Manifest signature verification failed'
                }
            
            # Check for newer version
            latest_version = manifest['latest_version']
            if self._is_newer_version(latest_version, self.current_version):
                return {
                    'update_available': True,
                    'current_version': self.current_version,
                    'latest_version': latest_version,
                    'release_notes': manifest['release_notes'],
                    'download_url': manifest['download_url'],
                    'signature': manifest['signature']
                }
            else:
                return {
                    'update_available': False,
                    'current_version': self.current_version
                }
                
        except Exception as e:
            return {
                'update_available': False,
                'error': str(e)
            }
    
    async def download_update(self, update_info: Dict[str, Any]) -> bool:
        """Download and verify update"""
        
        try:
            # Download update package
            response = requests.get(
                update_info['download_url'],
                timeout=30,
                stream=True
            )
            response.raise_for_status()
            
            # Verify download integrity
            package_hash = hashlib.sha256(response.content).hexdigest()
            if package_hash != update_info['package_hash']:
                return False
            
            # Save update package
            update_file = f"/tmp/paladin_update_{update_info['latest_version']}.tar.gz"
            with open(update_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Verify package signature
            if not self._verify_package_signature(update_file, update_info['signature']):
                return False
            
            # Install update
            return await self._install_update(update_file)
            
        except Exception as e:
            print(f"Update download failed: {e}")
            return False
    
    def _verify_manifest_signature(self, manifest: Dict[str, Any]) -> bool:
        """Verify update manifest signature"""
        # Implementation would verify cryptographic signature
        # This is a simplified version
        return True
    
    def _verify_package_signature(self, package_file: str, signature: str) -> bool:
        """Verify update package signature"""
        # Implementation would verify cryptographic signature
        # This is a simplified version
        return True
    
    async def _install_update(self, update_file: str) -> bool:
        """Install update package"""
        
        try:
            # Extract update
            import tarfile
            with tarfile.open(update_file, 'r:gz') as tar:
                tar.extractall("/tmp/paladin_update")
            
            # Run update script
            import subprocess
            result = subprocess.run(
                ["/tmp/paladin_update/update.sh"],
                capture_output=True,
                text=True
            )
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"Update installation failed: {e}")
            return False
```

This self-hosting strategy ensures PAL-adin users have complete control over their AI assistant infrastructure while maintaining the highest standards of privacy, security, and performance, all in alignment with UNOWN principles.