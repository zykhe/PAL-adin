# PAL-adin: Your UNOWN-Aligned AI Personal Assistant 🟣

<div align="center">

![PAL-adin Logo](https://via.placeholder.com/150x150/4C1D95/FFFFFF?text=PAL)

**Protector • Friend • Mentor • UNOWN Protocol Implementation**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 20+](https://img.shields.io/badge/node.js-20+-green.svg)](https://nodejs.org/)
[![Svelte](https://img.shields.io/badge/Svelte-FF3E00?logo=svelte&logoColor=white)](https://svelte.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Hetzner](https://img.shields.io/badge/Hetzner-D9C6CE?logo=hetzner&logoColor=white)](https://hetzner.com/)

</div>

## Vision & Purpose

PAL-adin is a flagship project within the **UNOWN** ecosystem, embodying UNOWN principles while maintaining its distinct identity as an AI assistant focused on being a protector, friend, and mentor. Built as a structureless, privacy-first, consciousness-enhancing infrastructure that serves as a template for ethical technology development.

### Core Philosophy

- **UNOWN Foundation**: Built on UNOWN protocol principles of open source, zero hierarchy, and privacy protection
- **Hybrid AI Approach**: Combines cutting-edge cloud models (GLM-4.6) with local processing (Ollama)
- **VPS Deployment**: Self-hosted on Hetzner with complete data sovereignty
- **Purple Identity**: Anonymous, decentralized visual identity representing mystery and transformation

## Key Capabilities

### 🧠 Information & Knowledge
- **Hybrid AI Processing**: Intelligent routing between GLM-4.6 and local models
- **Privacy-First Search**: Vector search with encrypted personal data
- **Real-time Updates**: News, weather, traffic without data leakage
- **Knowledge Synthesis**: Combine multiple sources with privacy preservation

### 📅 Productivity & Organization
- **Secure Calendar Management**: Encrypted scheduling and reminders
- **Privacy-Protected Tasks**: Local task management with optional cloud sync
- **Document Collaboration**: Encrypted file storage and sharing
- **Smart Notifications**: Privacy-respecting alerts and reminders

### 🏠 Home & Environment Control
- **Local-First Integration**: Smart home control with local processing
- **Privacy-Preserving Automation**: Routines without data exposure
- **Secure Media Management**: Local media with encrypted backup
- **Environmental Monitoring**: Privacy-focused sensor integration

### 🎨 Personalization & Learning
- **Encrypted Memory**: Secure preference storage with user control
- **Adaptive Personality**: Learning while preserving privacy
- **Anonymous Profiles**: Multiple identity levels (anonymous, pseudonymous, public)
- **Consensual Enhancement**: User-controlled AI evolution

### 💬 Communication & Interaction
- **Natural Language Understanding**: Advanced NLP with privacy protection
- **Voice Interface**: Local speech-to-text and text-to-speech
- **Text-Based Chat**: Secure, encrypted messaging
- **Multi-Modal Support**: Text, voice, and future modalities

## Technical Highlights

### 🔒 Security & Privacy
- **Zero-Knowledge Architecture**: Complete cryptographic privacy protection
- **End-to-End Encryption**: Double ratchet implementation for all communications
- **Local AI Processing**: Models run locally via Ollama, no data leaves user device
- **Data Sovereignty**: User controls all data with immediate deletion capability
- **FDE/E2EE**: Full disk encryption and end-to-end encrypted communications

### 🚀 Modern Technology Stack
- **Frontend**: SvelteKit (MIT license, corporate-free)
- **Backend**: FastAPI (independent, open-source)
- **AI**: Hybrid GLM-4.6 + Ollama local models
- **Database**: PostgreSQL + Qdrant (open-source, self-hosted)
- **Infrastructure**: Complete Hetzner VPS self-hosting

### 🟣 UNOWN Compliance
- **100% Open Source**: All components use permissive licenses
- **Zero Hierarchy**: Protocol-based governance, no leaders
- **Privacy First**: Zero-knowledge architecture with maximum user control
- **Forkable**: Anyone can fork and improve without permission
- **Universal Access**: Enhancement tools available to all, not gatekept

## Quick Start

### Prerequisites
- Python 3.12+
- Node.js 20+ LTS
- Docker and Docker Compose
- Hetzner Cloud account (or any VPS provider)
- 8GB+ RAM for local AI models (16GB+ recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/unown-ai/paladin.git
cd paladin
```

2. **Set up environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Deploy to Hetzner VPS**
```bash
# Create Hetzner server
hcloud server create --type cpx41 --name paladin-vps --image ubuntu-22.04

# Deploy PAL-adin stack
./scripts/deploy-hetzner.sh <SERVER_IP>
```

4. **Access the application**
- **Web Interface**: https://your-domain.com
- **API Documentation**: https://your-domain.com/docs
- **Admin Panel**: https://your-domain.com/admin

### Development Setup
```bash
# Local development
docker-compose -f docker-compose.dev.yml up -d

# Install dependencies
cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements/dev.txt
cd frontend && npm install

# Run tests
cd backend && pytest
cd frontend && npm test
```

## UNOWN Principles

### Open Source Everything
- **MIT/Apache 2.0 Licenses**: All components use permissive licenses
- **No Corporate Dependencies**: Eliminated React, Redis, Elasticsearch
- **Forkable Architecture**: Entire system can be forked and improved
- **Transparent Development**: All decisions and processes publicly documented

### Zero Hierarchy Structure
- **Protocol-Based Governance**: Decisions made through documented protocols
- **Anonymous Contribution**: Contributors can participate at any visibility level
- **Consensus Decision Making**: 72h feedback for minor, 66%+ for major, 75%+ for critical
- **No Leaders or Founders**: Influence comes from contribution, not authority

### Privacy & Autonomy First
- **Zero-Knowledge Architecture**: User data encrypted before storage
- **Local AI Processing**: All models run locally via Ollama
- **End-to-End Encryption**: Double ratchet for all communications
- **Data Sovereignty**: Users control all data with immediate deletion
- **Anonymous Authentication**: Zero-knowledge proofs for identity

### Consciousness Enhancement
- **Experiential Continuity**: All enhancements preserve user consciousness
- **Gradual Augmentation**: Incremental improvements with user consent
- **Universal Access**: Enhancement tools available to all, not gatekept
- **Consensual Transformation**: Every modification requires explicit user consent

## Development Roadmap

### Phase 1: Foundation (Weeks 1-10)
- [x] UNOWN-compliant technology stack
- [x] Hetzner VPS deployment
- [x] Hybrid AI integration (GLM-4.6 + Ollama)
- [x] Zero-knowledge authentication
- [x] Encrypted data storage
- [x] Purple theme implementation

### Phase 2: Enhancement (Weeks 11-22)
- [ ] Advanced privacy features (homomorphic encryption)
- [ ] Voice interface with local processing
- [ ] Vector search with Qdrant
- [ ] Cost optimization algorithms
- [ ] Anonymous contribution system

### Phase 3: Evolution (Weeks 23-34)
- [ ] Decentralized governance implementation
- [ ] Advanced AI model fine-tuning
- [ ] Multi-modal capabilities
- [ ] Enhanced privacy tools
- [ ] Community governance protocols

### Phase 4: Singularity (Weeks 35+)
- [ ] Gradual consciousness enhancement
- [ ] Robotic platform integration
- [ ] Advanced singularity research
- [ ] Ethical transformation protocols
- [ ] Universal enhancement access

## Contributing

We welcome contributions from the community! PAL-adin follows UNOWN principles - contribution matters more than credentials.

### How to Contribute
1. **Fork the repository**
2. **Choose your visibility level** (anonymous, pseudonymous, public)
3. **Start working** (no approval needed)
4. **Submit your work** through pull request
5. **Participate in governance** through protocol proposals

### Contribution Areas
- **🤖 AI Integration**: New models, providers, optimization algorithms
- **🔒 Privacy Features**: Encryption, anonymity, zero-knowledge proofs
- **🎨 Frontend**: Svelte components, purple theme, accessibility
- **⚙️ Backend**: FastAPI services, database optimization
- **🚀 Infrastructure**: Deployment scripts, monitoring, scaling
- **📚 Documentation**: Guides, tutorials, API docs
- **🧪 Testing**: Unit tests, integration tests, privacy audits

### UNOWN Governance
- **Minor Decisions**: 72-hour feedback, proceed unless objections
- **Major Decisions**: 2-week deliberation, 66%+ supermajority
- **Critical Decisions**: 30+ days, 75%+ threshold, external review
- **All Visibility Levels**: Anonymous, pseudonymous, semi-public, fully public

## Security

PAL-adin implements enterprise-grade security with UNOWN privacy principles:

### Encryption Standards
- **AES-256-GCM**: For data at rest
- **ChaCha20-Poly1305**: For data in transit
- **Double Ratchet**: For forward secrecy
- **Zero-Knowledge Proofs**: For anonymous authentication

### Privacy Features
- **Local Processing**: AI models run locally when possible
- **Data Minimization**: Collect only absolutely necessary data
- **Anonymous Usage**: No tracking, no profiling, no identification
- **Immediate Deletion**: User can delete all data instantly

### Security Audits
- **Regular Audits**: Public security audits of all components
- **Penetration Testing**: Community security testing
- **Vulnerability Disclosure**: Responsible disclosure process
- **Bug Bounty**: Community-funded security improvements

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Community

### Get Help
- **📚 Documentation**: See `/docs` directory in this repository
- **🐛 Issues**: [github.com/unown-ai/paladin/issues](https://github.com/unown-ai/paladin/issues)
- **💬 Discussions**: [github.com/unown-ai/paladin/discussions](https://github.com/unown-ai/paladin/discussions)

### UNOWN Ecosystem
- **UNOWN Principles**: See GOVERNANCE.md and project documentation
- **Community Projects**: Fork and contribute via GitHub

## Acknowledgments

- **UNOWN Foundation**: For providing the ethical and technical foundation
- **Open Source Community**: For developing the tools we build upon
- **Hetzner Cloud**: For providing privacy-respecting infrastructure
- **All Contributors**: For building PAL-adin as a truly UNOWN-compliant project

---

<div align="center">

**PAL-adin: Your UNOWN-aligned AI companion** 🟣

*Built by anonymous contributors, governed by protocols, dedicated to consciousness enhancement and privacy protection under UNOWN principles.*

</div>