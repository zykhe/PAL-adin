# PAL-adin Project Structure

## Repository Organization

```
paladin/
├── README.md                          # Project overview and getting started
├── LICENSE                            # Open source license (MIT/Apache 2.0)
├── .gitignore                         # Git ignore patterns
├── docker-compose.yml                 # Development environment setup
├── Dockerfile                         # Production container build
├── Makefile                           # Common development tasks
├── pyproject.toml                     # Python project configuration
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .github/                           # GitHub workflows and templates
│   ├── workflows/                     # CI/CD pipelines
│   │   ├── test.yml                   # Automated testing
│   │   ├── security.yml               # Security scanning
│   │   └── deploy.yml                 # Deployment automation
│   └── ISSUE_TEMPLATE/                # Issue templates
├── docs/                              # Documentation
│   ├── api/                           # API documentation
│   ├── deployment/                    # Deployment guides
│   ├── development/                   # Development guides
│   └── user-guide/                    # User documentation
├── backend/                           # FastAPI backend application
│   ├── app/                           # Main application code
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI application entry point
│   │   ├── config.py                  # Configuration management
│   │   ├── database.py                # Database connection and setup
│   │   ├── dependencies.py            # FastAPI dependencies
│   │   ├── middleware.py              # Custom middleware
│   │   ├── api/                       # API routes
│   │   │   ├── __init__.py
│   │   │   ├── v1/                    # API version 1
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py            # Authentication endpoints
│   │   │   │   ├── chat.py            # Chat endpoints
│   │   │   │   ├── users.py           # User management
│   │   │   │   ├── memory.py          # Memory management
│   │   │   │   └── tools.py           # Tool integrations
│   │   │   └── deps.py                # API dependencies
│   │   ├── core/                      # Core business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                # Authentication logic
│   │   │   ├── security.py            # Security utilities
│   │   │   ├── encryption.py          # Data encryption
│   │   │   └── exceptions.py          # Custom exceptions
│   │   ├── services/                  # Business services
│   │   │   ├── __init__.py
│   │   │   ├── chat_service.py        # Chat processing service
│   │   │   ├── ai_service.py          # AI integration service
│   │   │   ├── memory_service.py      # Memory management service
│   │   │   ├── user_service.py        # User management service
│   │   │   └── tools_service.py       # External tools service
│   │   ├── models/                    # Database models
│   │   │   ├── __init__.py
│   │   │   ├── user.py                # User model
│   │   │   ├── conversation.py        # Conversation model
│   │   │   ├── message.py             # Message model
│   │   │   ├── memory.py              # Memory model
│   │   │   └── tool_config.py         # Tool configuration model
│   │   ├── schemas/                   # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py                # User schemas
│   │   │   ├── conversation.py        # Conversation schemas
│   │   │   ├── message.py             # Message schemas
│   │   │   ├── memory.py              # Memory schemas
│   │   │   └── common.py              # Common schemas
│   │   ├── ai/                        # AI integration layer
│   │   │   ├── __init__.py
│   │   │   ├── langchain_integration.py # LangChain setup
│   │   │   ├── providers/             # AI provider implementations
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py            # Base provider interface
│   │   │   │   ├── glm_provider.py    # GLM-4.6 provider
│   │   │   │   ├── openai_provider.py # OpenAI provider
│   │   │   │   └── local_provider.py  # Local model provider
│   │   │   ├── prompts/               # Prompt templates
│   │   │   │   ├── __init__.py
│   │   │   │   ├── chat_prompts.py    # Chat-related prompts
│   │   │   │   ├── tool_prompts.py    # Tool-related prompts
│   │   │   │   └── system_prompts.py  # System prompts
│   │   │   └── tools/                 # AI tools and agents
│   │   │       ├── __init__.py
│   │   │       ├── web_search.py      # Web search tool
│   │   │       ├── calculator.py      # Calculator tool
│   │   │       ├── calendar.py        # Calendar integration
│   │   │       └── file_operations.py # File operations
│   │   └── utils/                     # Utility functions
│   │       ├── __init__.py
│   │       ├── logging.py             # Logging configuration
│   │       ├── validators.py          # Data validation
│   │       ├── helpers.py             # Helper functions
│   │       └── constants.py           # Application constants
│   ├── tests/                         # Test suite
│   │   ├── __init__.py
│   │   ├── conftest.py                # Pytest configuration
│   │   ├── test_auth.py               # Authentication tests
│   │   ├── test_chat.py               # Chat functionality tests
│   │   ├── test_ai.py                 # AI integration tests
│   │   ├── test_memory.py             # Memory system tests
│   │   └── test_tools.py              # Tools tests
│   ├── alembic/                       # Database migrations
│   │   ├── versions/                  # Migration files
│   │   ├── env.py                     # Alembic environment
│   │   └── script.py.mako             # Migration template
│   ├── scripts/                       # Utility scripts
│   │   ├── init_db.py                 # Database initialization
│   │   ├── create_user.py             # User creation script
│   │   └── backup.py                  # Backup script
│   └── requirements/                  # Requirements files
│       ├── base.txt                   # Base requirements
│       ├── dev.txt                    # Development requirements
│       └── prod.txt                   # Production requirements
├── frontend/                          # React frontend application
│   ├── public/                        # Static assets
│   │   ├── index.html                 # HTML template
│   │   ├── favicon.ico                # Favicon
│   │   └── manifest.json             # PWA manifest
│   ├── src/                           # Source code
│   │   ├── components/               # Reusable components
│   │   │   ├── common/                # Common components
│   │   │   │   ├── Button.tsx         # Button component
│   │   │   │   ├── Input.tsx          # Input component
│   │   │   │   ├── Modal.tsx          # Modal component
│   │   │   │   └── Loading.tsx        # Loading component
│   │   │   ├── chat/                  # Chat-specific components
│   │   │   │   ├── ChatInterface.tsx  # Main chat interface
│   │   │   │   ├── MessageList.tsx    # Message list
│   │   │   │   ├── MessageInput.tsx   # Message input
│   │   │   │   └── MessageBubble.tsx  # Individual message
│   │   │   ├── auth/                  # Authentication components
│   │   │   │   ├── LoginForm.tsx      # Login form
│   │   │   │   ├── RegisterForm.tsx   # Registration form
│   │   │   │   └── ProtectedRoute.tsx # Route protection
│   │   │   └── layout/                # Layout components
│   │   │       ├── Header.tsx         # Header component
│   │   │       ├── Sidebar.tsx        # Sidebar component
│   │   │       └── Layout.tsx         # Main layout
│   │   ├── pages/                     # Page components
│   │   │   ├── HomePage.tsx           # Home page
│   │   │   ├── ChatPage.tsx           # Chat page
│   │   │   ├── SettingsPage.tsx       # Settings page
│   │   │   └── ProfilePage.tsx        # Profile page
│   │   ├── hooks/                     # Custom React hooks
│   │   │   ├── useAuth.ts             # Authentication hook
│   │   │   ├── useChat.ts             # Chat functionality hook
│   │   │   ├── useWebSocket.ts        # WebSocket hook
│   │   │   └── useLocalStorage.ts     # Local storage hook
│   │   ├── services/                  # API services
│   │   │   ├── api.ts                 # API client configuration
│   │   │   ├── authService.ts         # Authentication service
│   │   │   ├── chatService.ts         # Chat service
│   │   │   └── userService.ts         # User service
│   │   ├── store/                     # State management
│   │   │   ├── index.ts               # Store configuration
│   │   │   ├── authSlice.ts           # Authentication state
│   │   │   ├── chatSlice.ts           # Chat state
│   │   │   └── uiSlice.ts             # UI state
│   │   ├── utils/                     # Utility functions
│   │   │   ├── constants.ts           # Application constants
│   │   │   ├── helpers.ts             # Helper functions
│   │   │   ├── validation.ts          # Form validation
│   │   │   └── encryption.ts          # Client-side encryption
│   │   ├── styles/                    # Styling
│   │   │   ├── globals.css            # Global styles
│   │   │   ├── variables.css          # CSS variables
│   │   │   └── components/            # Component-specific styles
│   │   ├── types/                     # TypeScript type definitions
│   │   │   ├── auth.ts                # Authentication types
│   │   │   ├── chat.ts                # Chat types
│   │   │   ├── user.ts                # User types
│   │   │   └── api.ts                 # API response types
│   │   ├── App.tsx                    # Main application component
│   │   ├── index.tsx                  # Application entry point
│   │   └── setupTests.ts              # Test setup
│   ├── package.json                   # Node.js dependencies
│   ├── tsconfig.json                  # TypeScript configuration
│   ├── tailwind.config.js             # Tailwind CSS configuration
│   ├── vite.config.ts                 # Vite build configuration
│   └── .eslintrc.js                   # ESLint configuration
├── deployment/                        # Deployment configurations
│   ├── docker/                        # Docker configurations
│   │   ├── Dockerfile.backend         # Backend Dockerfile
│   │   ├── Dockerfile.frontend        # Frontend Dockerfile
│   │   └── docker-compose.prod.yml    # Production compose file
│   ├── kubernetes/                    # Kubernetes manifests
│   │   ├── namespace.yaml             # Namespace
│   │   ├── configmap.yaml             # Configuration
│   │   ├── secret.yaml                # Secrets
│   │   ├── backend-deployment.yaml    # Backend deployment
│   │   ├── frontend-deployment.yaml   # Frontend deployment
│   │   ├── service.yaml               # Service definitions
│   │   └── ingress.yaml               # Ingress configuration
│   ├── nginx/                         # Nginx configuration
│   │   ├── nginx.conf                 # Main configuration
│   │   ├── ssl.conf                   # SSL configuration
│   │   └── security.conf              # Security headers
│   └── scripts/                       # Deployment scripts
│       ├── deploy.sh                  # Main deployment script
│       ├── backup.sh                  # Backup script
│       └── rollback.sh                # Rollback script
├── monitoring/                        # Monitoring and observability
│   ├── prometheus/                    # Prometheus configuration
│   │   ├── prometheus.yml             # Prometheus config
│   │   └── rules/                     # Alert rules
│   ├── grafana/                       # Grafana dashboards
│   │   ├── dashboards/                # Dashboard definitions
│   │   └── provisioning/              # Auto-provisioning
│   └── logs/                          # Log aggregation
│       ├── filebeat.yml               # Filebeat configuration
│       └── logstash.conf              # Logstash configuration
└── tools/                             # Development and utility tools
    ├── setup/                         # Setup scripts
    │   ├── install.sh                 # Installation script
    │   ├── configure.sh               # Configuration script
    │   └── test.sh                    # Test script
    ├── development/                   # Development tools
    │   ├── pre-commit-hook.sh         # Pre-commit hook
    │   ├── code-formatter.sh          # Code formatting
    │   └── dependency-check.sh        # Dependency checking
    └── security/                      # Security tools
        ├── vulnerability-scan.sh      # Vulnerability scanning
        ├── security-audit.sh          # Security auditing
        └── penetration-test.sh        # Penetration testing
```

## Modular Component Design

### Backend Modules

#### 1. Authentication Module (`backend/app/core/auth.py`)
- JWT token management
- User authentication
- Password hashing and verification
- Session management

#### 2. AI Integration Module (`backend/app/ai/`)
- Provider abstraction layer
- LangChain integration
- Tool and agent management
- Prompt template system

#### 3. Chat Service Module (`backend/app/services/chat_service.py`)
- Message processing
- Conversation management
- Real-time WebSocket handling
- Context management

#### 4. Memory Service Module (`backend/app/services/memory_service.py`)
- Long-term memory storage
- User preference management
- Context retrieval
- Personalization data

#### 5. Tools Service Module (`backend/app/services/tools_service.py`)
- External API integrations
- Web search capabilities
- Calendar management
- File operations

### Frontend Modules

#### 1. Authentication Components (`frontend/src/components/auth/`)
- Login/registration forms
- Route protection
- Token management
- User session handling

#### 2. Chat Interface (`frontend/src/components/chat/`)
- Message display
- Input handling
- Real-time updates
- Conversation history

#### 3. State Management (`frontend/src/store/`)
- Redux Toolkit configuration
- Slice definitions
- Middleware setup
- Persistence layer

#### 4. API Services (`frontend/src/services/`)
- HTTP client configuration
- Endpoint definitions
- Error handling
- Request/response interceptors

## Plugin Architecture

### Plugin System Structure
```
plugins/
├── weather/                          # Weather plugin
│   ├── __init__.py
│   ├── main.py                       # Plugin main logic
│   ├── config.py                     # Configuration
│   └── api.py                        # External API integration
├── news/                             # News plugin
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   └── api.py
└── calendar/                         # Calendar plugin
    ├── __init__.py
    ├── main.py
    ├── config.py
    └── api.py
```

### Plugin Interface
```python
# backend/app/plugins/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BasePlugin(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    @abstractmethod
    def get_name(self) -> str:
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        pass
    
    @abstractmethod
    async def execute(self, command: str, params: Dict[str, Any]) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_commands(self) -> List[str]:
        pass
```

## Configuration Management

### Environment-Based Configuration
```python
# backend/app/config.py
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str
    redis_url: str
    
    # Security
    jwt_secret_key: str
    encryption_key: str
    
    # AI Providers
    glm_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    # External Services
    weather_api_key: Optional[str] = None
    news_api_key: Optional[str] = None
    
    # Application
    debug: bool = False
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
```

This modular structure ensures PAL-adin can grow from a simple AI assistant to a comprehensive personal companion system while maintaining code quality, security, and extensibility.