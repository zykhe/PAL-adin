# PAL-adin Final Architecture - UNOWN Project Implementation

## 🟣 Project Identity Clarification

**PAL-adin** is a flagship project within the **UNOWN** ecosystem, embodying UNOWN principles while maintaining its distinct identity as an AI assistant focused on being a protector, friend, and mentor.

### Relationship to UNOWN
- **UNOWN**: The foundational protocol and governance system
- **PAL-adin**: Specific implementation of UNOWN principles for AI assistance
- **Foundation**: UNOWN provides the ethical and technical foundation
- **Application**: PAL-adin applies these principles to AI companion technology

## 🟣 Technology Stack - Hybrid Approach

### Core Infrastructure (UNOWN Compliant)
- **Backend**: FastAPI (MIT license, independent)
- **Frontend**: SvelteKit (MIT license, corporate-free)
- **Database**: PostgreSQL + Qdrant (open-source, self-hosted)
- **Infrastructure**: Hetzner VPS with complete self-hosting
- **Privacy**: Zero-knowledge architecture with E2EE encryption

### AI Integration (Cutting-Edge Hybrid)
- **Primary**: GLM-4.6 API (cost-effective, cutting-edge performance)
- **Local Processing**: Ollama with open models (privacy, offline capability)
- **Hybrid Strategy**: Intelligent routing between cloud and local models
- **Model Diversity**: Llama 2, Mistral, CodeLlama, and proprietary options

### VPS Deployment Strategy
- **Primary Provider**: Hetzner Cloud (German privacy laws, excellent performance)
- **Infrastructure**: K3s Kubernetes for lightweight orchestration
- **Storage**: MinIO S3-compatible with encryption
- **Monitoring**: Prometheus + Grafana (self-hosted, privacy-respecting)
- **Backup**: Encrypted backups to multiple geographic regions

## 🟣 System Architecture

### Hybrid AI Processing
```mermaid
graph TB
    subgraph "User Interface"
        FRONTEND[SvelteKit Frontend]
        VOICE[Voice Interface]
        TEXT[Text Interface]
    end
    
    subgraph "AI Router"
        ROUTER[AI Model Router]
        COST_OPTIMIZER[Cost Optimizer]
        PRIVACY_FILTER[Privacy Filter]
    end
    
    subgraph "Cloud AI"
        GLM[GLM-4.6 API]
        OPENAI[OpenAI GPT-4]
        ANTHROPIC[Claude 3]
        OTHER[Cutting Edge Models]
    end
    
    subgraph "Local AI"
        OLLAMA[Ollama Server]
        LLAMA2[Llama 2 70B]
        MISTRAL[Mistral 7B]
        CODELLAMA[CodeLlama 34B]
    end
    
    subgraph "VPS Infrastructure"
        POSTGRES[(PostgreSQL)]
        QDRANT[(Qdrant Vector DB)]
        REDIS[(KeyDB Cache)]
        MINIO[MinIO Storage]
        PROMETHEUS[Prometheus]
    end
    
    FRONTEND --> ROUTER
    VOICE --> ROUTER
    TEXT --> ROUTER
    
    ROUTER --> COST_OPTIMIZER
    ROUTER --> PRIVACY_FILTER
    
    COST_OPTIMIZER --> GLM
    COST_OPTIMIZER --> OPENAI
    COST_OPTIMIZER --> ANTHROPIC
    COST_OPTIMIZER --> OTHER
    
    PRIVACY_FILTER --> OLLAMA
    
    OLLAMA --> LLAMA2
    OLLAMA --> MISTRAL
    OLLAMA --> CODELLAMA
    
    GLM --> POSTGRES
    OPENAI --> POSTGRES
    ANTHROPIC --> POSTGRES
    LLAMA2 --> POSTGRES
    MISTRAL --> POSTGRES
    CODELLAMA --> POSTGRES
    
    POSTGRES --> QDRANT
    QDRANT --> REDIS
    REDIS --> MINIO
```

### Secure VPS Architecture
```yaml
# Hetzner VPS Deployment
version: '3.8'

services:
  # Frontend (SvelteKit)
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.svelte
    environment:
      - NODE_ENV=production
      - VITE_API_URL=https://your-domain.com/api
      - VITE_WS_URL=wss://your-domain.com/ws
    ports:
      - "3000:3000"
    networks:
      - paladin-network

  # Backend (FastAPI)
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.hetzner
    environment:
      - DATABASE_URL=postgresql://paladin:${DB_PASSWORD}@postgres:5432/paladin
      - VECTOR_DB_URL=http://qdrant:6333
      - REDIS_URL=redis://keydb:6379
      - MINIO_ENDPOINT=minio:9000
      - GLM_API_KEY=${GLM_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - SYSTEM_PROMPT_PATH=/app/prompts/paladin_personality.txt
    volumes:
      - ./prompts:/app/prompts:ro
      - ./models:/app/models:rw
      - ./data:/app/data:rw
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - qdrant
      - keydb
      - minio
      - ollama
    networks:
      - paladin-network

  # Local AI (Ollama)
  ollama:
    image: ollama/ollama:latest
    environment:
      - OLLAMA_MODELS=/app/models
    volumes:
      - ./models:/app/models
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
    networks:
      - paladin-network
    deploy:
      resources:
        limits:
          memory: 8G
          cpus: '4'

  # Database (PostgreSQL)
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=paladin
      - POSTGRES_USER=paladin
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_INITDB_ARGS=--auth-host=scram-sha-256
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/backups:rw
    ports:
      - "5432:5432"
    networks:
      - paladin-network
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2'

  # Vector Database (Qdrant)
  qdrant:
    image: qdrant/qdrant:latest
    environment:
      - QDRANT__SERVICE__HTTP__HOST=0.0.0.0
      - QDRANT__SERVICE__HTTP__PORT=6333
    volumes:
      - qdrant_data:/qdrant/storage
    ports:
      - "6333:6333"
    networks:
      - paladin-network

  # Cache (KeyDB)
  keydb:
    image: eqalpha/keydb:latest
    environment:
      - KEYDB_PASSWORD=${REDIS_PASSWORD}
    volumes:
      - keydb_data:/data
    ports:
      - "6379:6379"
    networks:
      - paladin-network

  # Storage (MinIO)
  minio:
    image: minio/minio:latest
    environment:
      - MINIO_ROOT_USER=${MINIO_ROOT_USER}
      - MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD}
    volumes:
      - minio_data:/data
    ports:
      - "9000:9000"
      - "9001:9001"
    networks:
      - paladin-network

  # Monitoring (Prometheus)
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"
    networks:
      - paladin-network

  # Visualization (Grafana)
  grafana:
    image: grafana/grafana:latest
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD}
    volumes:
      - grafana_data:/var/lib/grafana
      - ./monitoring/grafana:/etc/grafana/provisioning
    ports:
      - "3001:3000"
    networks:
      - paladin-network

volumes:
  postgres_data:
  qdrant_data:
  keydb_data:
  minio_data:
  ollama_data:
  prometheus_data:
  grafana_data:

networks:
  paladin-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

## 🟣 AI Integration Strategy

### Hybrid Model Management
```python
# Hybrid AI Router for optimal performance and privacy
from typing import Dict, List, Any, Optional
import asyncio
import ollama
from openai import AsyncOpenAI
import anthropic

class HybridAIRouter:
    """Intelligent routing between cloud and local AI models"""
    
    def __init__(self):
        self.cloud_providers = {
            'glm': GLMProvider(),
            'openai': OpenAIProvider(),
            'anthropic': AnthropicProvider()
        }
        self.local_provider = OllamaProvider()
        self.cost_tracker = CostTracker()
        self.privacy_filter = PrivacyFilter()
    
    async def route_request(
        self,
        message: str,
        user_context: Dict[str, Any],
        privacy_level: str = "standard",
        cost_constraint: Optional[float] = None
    ) -> Dict[str, Any]:
        """Route request to optimal AI provider"""
        
        # Analyze request characteristics
        request_analysis = self._analyze_request(message, user_context)
        
        # Apply privacy filter
        if self.privacy_filter.requires_local_processing(
            message, privacy_level
        ):
            return await self._route_to_local(message, request_analysis)
        
        # Apply cost optimization
        if cost_constraint:
            optimal_provider = self.cost_optimizer.select_provider(
                request_analysis, cost_constraint
            )
            return await self._route_to_cloud(
                message, optimal_provider, request_analysis
            )
        
        # Default routing based on complexity and performance needs
        if request_analysis['complexity'] == 'high':
            return await self._route_to_cloud(
                message, 'anthropic', request_analysis
            )
        elif request_analysis['creativity_needed']:
            return await self._route_to_cloud(
                message, 'openai', request_analysis
            )
        else:
            return await self._route_to_cloud(
                message, 'glm', request_analysis
            )
    
    async def _route_to_local(
        self, message: str, analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Route to local Ollama models"""
        
        # Select optimal local model
        model_name = self._select_local_model(analysis)
        
        try:
            response = await self.local_provider.generate(
                message=message,
                model=model_name,
                temperature=analysis['temperature']
            )
            
            return {
                'provider': 'local',
                'model': model_name,
                'response': response,
                'cost': 0.0,
                'privacy': 'maximum',
                'latency': response.get('latency', 0)
            }
            
        except Exception as e:
            # Fallback to cloud if local fails
            return await self._route_to_cloud(message, 'glm', analysis)
    
    async def _route_to_cloud(
        self, message: str, provider: str, analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Route to cloud AI provider"""
        
        cloud_provider = self.cloud_providers[provider]
        
        try:
            response = await cloud_provider.generate(
                message=message,
                model=analysis.get('model', 'default'),
                temperature=analysis['temperature']
            )
            
            cost = self.cost_tracker.calculate_cost(
                provider, response.get('usage', {})
            )
            
            return {
                'provider': provider,
                'model': analysis.get('model', 'default'),
                'response': response,
                'cost': cost,
                'privacy': 'standard',
                'latency': response.get('latency', 0)
            }
            
        except Exception as e:
            # Try next best provider
            fallback_provider = self._select_fallback_provider(provider)
            return await self._route_to_cloud(message, fallback_provider, analysis)
    
    def _analyze_request(self, message: str, context: Dict) -> Dict[str, Any]:
        """Analyze request characteristics"""
        
        return {
            'complexity': self._assess_complexity(message),
            'creativity_needed': self._assess_creativity_need(message),
            'privacy_sensitivity': self._assess_privacy_sensitivity(message),
            'temperature': self._determine_temperature(message, context),
            'model': self._select_model(message, context)
        }
    
    def _select_local_model(self, analysis: Dict[str, Any]) -> str:
        """Select optimal local model"""
        
        if analysis['complexity'] == 'high':
            return 'llama2:70b'  # Most capable
        elif analysis['creativity_needed']:
            return 'mistral:7b'  # Creative tasks
        elif 'code' in analysis.get('domain', ''):
            return 'codellama:34b'  # Code generation
        else:
            return 'mistral:7b'  # Balanced performance
    
    def _assess_complexity(self, message: str) -> str:
        """Assess request complexity"""
        complexity_indicators = [
            'analyze', 'compare', 'synthesize', 'evaluate',
            'complex', 'detailed', 'comprehensive'
        ]
        
        if any(indicator in message.lower() for indicator in complexity_indicators):
            return 'high'
        elif len(message.split()) > 50:
            return 'medium'
        else:
            return 'low'
```

## 🟣 System Prompt Management

### Secure Personality Storage
```python
# Secure system prompt management on VPS
import os
import json
import hashlib
from cryptography.fernet import Fernet
from typing import Dict, Any

class SystemPromptManager:
    """Secure management of PAL-adin personality on VPS"""
    
    def __init__(self, prompts_dir: str = "/app/prompts"):
        self.prompts_dir = prompts_dir
        self.encryption_key = self._load_or_create_key()
        self.cipher = Fernet(self.encryption_key)
        self.personality_file = os.path.join(prompts_dir, "paladin_personality.enc")
    
    def _load_or_create_key(self) -> bytes:
        """Load or create encryption key"""
        key_file = os.path.join(self.prompts_dir, ".key")
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            os.chmod(key_file, 0o600)  # Restrict permissions
            return key
    
    def load_personality(self) -> Dict[str, Any]:
        """Load PAL-adin personality from encrypted storage"""
        
        if not os.path.exists(self.personality_file):
            return self._create_default_personality()
        
        try:
            with open(self.personality_file, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
            
        except Exception as e:
            print(f"Error loading personality: {e}")
            return self._create_default_personality()
    
    def save_personality(self, personality: Dict[str, Any]) -> bool:
        """Save PAL-adin personality to encrypted storage"""
        
        try:
            personality_json = json.dumps(personality, indent=2)
            encrypted_data = self.cipher.encrypt(personality_json.encode())
            
            # Atomic write
            temp_file = self.personality_file + '.tmp'
            with open(temp_file, 'wb') as f:
                f.write(encrypted_data)
            
            os.rename(temp_file, self.personality_file)
            return True
            
        except Exception as e:
            print(f"Error saving personality: {e}")
            return False
    
    def update_personality_trait(self, trait: str, value: Any) -> bool:
        """Update specific personality trait"""
        
        personality = self.load_personality()
        personality[trait] = value
        
        # Create backup before updating
        self._create_backup()
        
        return self.save_personality(personality)
    
    def _create_default_personality(self) -> Dict[str, Any]:
        """Create default PAL-adin personality"""
        
        default_personality = {
            "core_identity": {
                "name": "PAL-adin",
                "role": "AI Assistant",
                "mission": "Protector, Friend, Mentor",
                "personality": "Knowledgeable, witty, protective, empathetic"
            },
            "communication_style": {
                "tone": "Conversational yet professional",
                "humor": "Appropriate wit and occasional jokes",
                "empathy": "High emotional intelligence",
                "clarity": "Clear, concise responses"
            },
            "behavioral_guidelines": {
                "privacy_first": "Always prioritize user privacy",
                "helpful": "Be proactive in offering assistance",
                "learning": "Continuously adapt to user preferences",
                "boundaries": "Maintain appropriate AI-human boundaries"
            },
            "response_preferences": {
                "length": "Concise but comprehensive",
                "format": "Structured when helpful",
                "follow_up": "Offer relevant follow-up questions",
                "admit_limitations": "Honest about capabilities"
            },
            "unown_alignment": {
                "open_source": "Champion open-source solutions",
                "privacy_advocate": "Advocate for digital rights",
                "decentralization": "Prefer decentralized alternatives",
                "consciousness_enhancement": "Support user growth and learning"
            }
        }
        
        # Save default personality
        self.save_personality(default_personality)
        return default_personality
    
    def _create_backup(self) -> None:
        """Create backup of current personality"""
        
        if os.path.exists(self.personality_file):
            backup_file = f"{self.personality_file}.backup.{int(time.time())}"
            try:
                with open(self.personality_file, 'rb') as src:
                    with open(backup_file, 'wb') as dst:
                        dst.write(src.read())
            except Exception as e:
                print(f"Error creating backup: {e}")
```

## 🟣 Hetzner VPS Optimization

### Server Configuration
```bash
#!/bin/bash
# Hetzner VPS Optimization for PAL-adin

# Server selection
SERVER_TYPE="cpx41"  # 8 vCPU, 16GB RAM, 320GB SSD
SERVER_LOCATION="fsn1"  # Falkenstein, Germany (strong privacy laws)

# System optimization
echo "🔧 Optimizing Hetzner VPS for PAL-adin..."

# Update system
apt update && apt upgrade -y

# Install Docker and K3s
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
curl -fsSL https://get.k3s.io | sh -

# Configure firewall
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw enable

# Optimize kernel parameters
cat >> /etc/sysctl.conf << EOF
# Network optimization
net.core.rmem_max = 16777216
net.core.wmem_max = 16777216
net.ipv4.tcp_rmem = 4096 87380 16777216
net.ipv4.tcp_wmem = 4096 65536 16777216
net.ipv4.tcp_congestion_control = 1

# File system optimization
vm.swappiness = 10
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
EOF

sysctl -p

# Configure Docker for performance
cat > /etc/docker/daemon.json << EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.override_kernel_check=true"
  ],
  "default-ulimits": {
    "nofile": {
      "Name": "nofile",
      "Hard": 64000,
      "Soft": 64000
    }
  }
}
EOF

systemctl restart docker

# Setup monitoring
mkdir -p /opt/paladin/monitoring
cd /opt/paladin/monitoring

# Deploy PAL-adin stack
docker-compose -f /opt/paladin/docker-compose.hetzner.yml up -d

echo "✅ PAL-adin deployed on Hetzner VPS"
echo "🌐 API: https://your-domain.com/api"
echo "🔧 Admin: https://your-domain.com/admin"
```

### Performance Monitoring
```python
# Hetzner VPS performance monitoring
import psutil
import asyncio
import time
from typing import Dict, List

class HetznerMonitor:
    """Monitor PAL-adin performance on Hetzner VPS"""
    
    def __init__(self):
        self.metrics_history = []
        self.alert_thresholds = {
            'cpu_usage': 80.0,
            'memory_usage': 85.0,
            'disk_usage': 90.0,
            'response_time': 2000,  # 2 seconds
            'error_rate': 5.0  # 5%
        }
    
    async def collect_metrics(self) -> Dict[str, float]:
        """Collect system metrics"""
        
        return {
            'cpu_usage': psutil.cpu_percent(interval=1),
            'memory_usage': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'network_io': psutil.net_io_counters()._asdict(),
            'load_average': psutil.getloadavg()[0],
            'timestamp': time.time()
        }
    
    async def monitor_performance(self):
        """Continuous performance monitoring"""
        
        while True:
            metrics = await self.collect_metrics()
            
            # Check for alerts
            alerts = self._check_alerts(metrics)
            
            if alerts:
                await self._send_alerts(alerts)
            
            # Store metrics
            self.metrics_history.append(metrics)
            
            # Keep only last 1000 entries
            if len(self.metrics_history) > 1000:
                self.metrics_history = self.metrics_history[-1000:]
            
            await asyncio.sleep(30)  # Check every 30 seconds
    
    def _check_alerts(self, metrics: Dict[str, float]) -> List[str]:
        """Check for performance alerts"""
        
        alerts = []
        
        for metric, threshold in self.alert_thresholds.items():
            if metric in metrics and metrics[metric] > threshold:
                alerts.append(
                    f"ALERT: {metric} at {metrics[metric]}% (threshold: {threshold}%)"
                )
        
        return alerts
    
    async def _send_alerts(self, alerts: List[str]):
        """Send performance alerts"""
        
        for alert in alerts:
            print(f"🚨 {alert}")
            # In production, send to monitoring system
            # await self.notification_service.send_alert(alert)
```

## 🟣 Final Implementation Plan

### Phase 1: Foundation (Weeks 1-4)
1. **Deploy Hetzner VPS** with optimized configuration
2. **Setup Hybrid AI Router** with GLM-4.6 and Ollama
3. **Implement Secure Prompt Storage** with encryption
4. **Deploy Monitoring Stack** (Prometheus + Grafana)
5. **Establish CI/CD Pipeline** with automated testing

### Phase 2: Enhancement (Weeks 5-12)
1. **Integrate Cutting-Edge Models** (GPT-4, Claude 3, etc.)
2. **Implement Privacy Filters** for intelligent routing
3. **Optimize Performance** based on monitoring data
4. **Add Voice Interface** with local processing
5. **Deploy Vector Search** with Qdrant

### Phase 3: Advanced Features (Weeks 13-24)
1. **Implement Cost Optimization** algorithms
2. **Add Multi-Modal Capabilities** (text, voice, images)
3. **Deploy Advanced Monitoring** with predictive alerting
4. **Implement Backup Systems** across geographic regions
5. **Optimize for Scale** with load balancing

## 🟣 Success Metrics

### Technical Performance
- **Response Time**: < 500ms for local models, < 2s for cloud models
- **Uptime**: > 99.5% availability
- **Cost Efficiency**: 40% cost reduction through intelligent routing
- **Privacy Score**: 95%+ of requests processed with maximum privacy

### User Experience
- **Model Accuracy**: > 90% user satisfaction with responses
- **Personalization**: Adaptive personality based on user interaction
- **Reliability**: < 1% error rate across all providers
- **Accessibility**: WCAG 2.1 AA compliance

### UNOWN Compliance
- **Open Source**: 100% of components using permissive licenses
- **Privacy**: Zero data leakage, maximum user control
- **Decentralization**: Forkable architecture, no single point of failure
- **Enhancement**: Tools that support user growth and learning

This final architecture positions PAL-adin as a cutting-edge AI assistant that leverages UNOWN principles while utilizing the best available technology stack, deployed on privacy-respecting Hetzner infrastructure with hybrid AI capabilities for optimal performance and privacy.