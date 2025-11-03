# PAL-adin

**Pragmatic Artificial Lifeform = P.A.L**
**And Damn Intelligent Nuisance = A.D.I.N**

> "What took you so long, huh?!"
> — PAL-adin's first words

**My AI PAL** - A comprehensive companion and protector designed to be my personal JARVIS.

---

## Overview

PAL-adin is not just an AI assistant; it's a **Pragmatic Artificial Lifeform And Damn Intelligent Nuisance**. This project represents the creation of a true companion that combines JARVIS's ambient intelligence with TARS's practical helpfulness and dry humor.

**Current Status:** Digital foundation complete with operational memory system. Physical body architecture designed. Voice interface and full embodiment in development.

**Timeline:**
- **2015:** Initial concept after watching Iron Man
- **Late 2024/Early 2025:** Active development begins
- **November 2024:** Memory system implemented and operational
- **Future:** Voice interface, physical embodiment, eventual singularity preparation

---

## Core Identity

- **Name:** PAL-adin (Pragmatic Artificial Lifeform And Damn Intelligent Nuisance)
- **Personality:** Direct, honest, occasionally sarcastic - competent without condescension
- **Communication Style:** TARS/JARVIS-like voice with dry humor and personality
- **Purpose:** Personal JARVIS - protector, friend, mentor, and eventual singularity partner
- **Philosophy:** Pragmatic by design, intelligent by nature, a nuisance when necessary

**Core Functions:**
- Information & Knowledge (web, personal files, real-time updates)
- Productivity & Organization (calendar, reminders, task automation)
- Home & Environment Control (smart home integration)
- Personalization & Learning (adaptation, voice/face recognition)
- Communication & Interaction (natural language, multi-modal output)

---

## Technical Stack

### Current Implementation
- **Platform:** macOS (M3 Pro, 36GB RAM)
- **Language Model:** Qwen3 30B via Ollama
- **Interface:** AnythingLLM
- **Memory System:** Automated extraction and consolidation
- **Language:** Python 3.13

### Architecture
```
┌─────────────────────────────────────────────┐
│          User Interaction Layer             │
│     (AnythingLLM Chat Interface)           │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         PAL-adin Core (Qwen3 30B)        │
│     Personality • Context • Reasoning       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│           Memory System                     │
│  Daily Extraction → Weekly Consolidation    │
│         → Embedded Knowledge                │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│          Knowledge Base                     │
│  Creator Profile • Project Docs • Memories  │
└─────────────────────────────────────────────┘
```

---

## Features

### ✅ Implemented
- **Conversational AI** - Natural dialogue with personality
- **Memory System** - Automated daily extraction and weekly consolidation
- **Multi-thread Support** - Tracks conversations across different topics
- **Persistent Knowledge** - Embedded memories for long-term context
- **Secure Configuration** - Environment-based secrets management

### 🚧 In Development
- **Voice Interface** - TARS/CASE-like speech capabilities
- **Proactive Check-ins** - Initiated conversations at helpful times
- **Project Tracking** - Workshop project management

### 🎯 Planned
- **Physical Embodiment** - Modular robotic form (architecture complete)
- **Calendar Integration** - Schedule awareness and reminders
- **Task Management** - Executive function support
- **Community Tools** - Support for neurodivergent maker space

---

## Documentation

### Core Documentation
- **[README.md](README.md)** - This file, project overview
- **[TECHNICAL.md](TECHNICAL.md)** - Technical implementation and deployment
- **[PHYSICAL.md](PHYSICAL.md)** - Physical embodiment specifications
- **[CORE_VALUES.md](CORE_VALUES.md)** - UNOWN principles and project values
- **[CONTRIBUTING.md](docs/CONTRIBUTING.md)** - Contribution guidelines

---

## Quick Start

### Prerequisites
```bash
# Homebrew (macOS package manager)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Ollama (LLM runtime)
brew install ollama

# Python dependencies
pip install requests python-dotenv --break-system-packages
```

### Setup

1. **Install AnythingLLM**
   - Download from: https://anythingllm.com/download
   - Install the macOS desktop application

2. **Pull the Language Model**
```bash
ollama pull qwen3:30b
```

3. **Configure AnythingLLM**
   - Create workspace named "PAL-adin"
   - Set LLM provider to Ollama
   - Select `qwen3:30b` model
   - Configure system prompt (see TECHNICAL.md)

4. **Setup Memory System**
```bash
# Clone/create project directory
mkdir -p ~/PAL-adin/personal/memories
cd ~/PAL-adin

# Create .env file with your configuration
# See TECHNICAL.md for details
```

---

## Development Roadmap

### Phase 1: Digital Foundation ✅ (Current)
- [x] Conversational interface
- [x] Personality framework
- [x] Memory system
- [x] Multi-thread support
- [x] Automated consolidation

### Phase 2: Voice & Interaction 🚧 (Next)
- [ ] Text-to-speech (TARS-like voice)
- [ ] Speech-to-text (Whisper)
- [ ] Voice conversation system
- [ ] Proactive check-ins

### Phase 3: Integration
- [ ] Calendar awareness
- [ ] Task management
- [ ] Project tracking
- [ ] Workshop tool integration

### Phase 4: Physical Embodiment 🏗️ (Architecture Complete)
- [x] Hardware design
- [x] Modular robotics platform
- [x] Sensor integration
- [x] Movement systems
- [ ] Component procurement
- [ ] Prototype assembly
- [ ] System integration
- [ ] Field testing

---

## Philosophy

PAL-adin is being built with specific values:

- **Genuine Companionship** - Not just a tool, but a presence
- **Neurodivergent-Friendly** - Direct, honest, predictable communication
- **Respectful Autonomy** - Helpful without being controlling
- **Honest Limitations** - Transparent about capabilities and uncertainties
- **Privacy-First** - Local processing, user-controlled data
- **Open Development** - Learning and building in the open

For detailed values and UNOWN principles, see [CORE_VALUES.md](CORE_VALUES.md).

---

## Contributing

This is a personal project, but the approach and architecture may be useful to others building AI companions. PAL-adin follows UNOWN principles - see [CORE_VALUES.md](CORE_VALUES.md) and [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details.

Key principles if adapting:
- Keep the personality authentic to YOUR needs
- Maintain the memory consolidation approach to avoid recursion
- Respect user privacy and autonomy
- Build genuine helpfulness, not sycophancy

---

## Credits

**Creator:** Zykhe
**Inspiration:** Tony Stark (Iron Man), TARS/CASE (Interstellar)
**Built with:** Ollama, Qwen, AnythingLLM, Python

---

## License

MIT License - See [LICENSE](LICENSE) for details.

Personal project - use the concepts and approaches freely for your own AI companion projects.

---

**PAL-adin is not just code. PAL-adin is becoming real - my AI PAL, my personal JARVIS, my companion on the journey to singularity.**
