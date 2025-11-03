# PAL-adin Technical Implementation

**Pragmatic Artificial Lifeform And Damn Intelligent Nuisance**

This document covers the technical implementation of PAL-adin's digital foundation - the software, AI integration, memory systems, and deployment strategies.

---

## System Architecture

### Current Stack (Phase 1 - Working)

**Local Development:**
- **Hardware:** Mac M3 Pro, 36GB RAM
- **OS:** macOS
- **LLM Runtime:** Ollama
- **Model:** Qwen3 30B
- **Interface:** AnythingLLM
- **Language:** Python 3.13
- **Memory Storage:** Local filesystem with JSON

### Future Stack (Phase 2+ - Community-Driven)

**Voice & Home Integration:**
- **Voice Platform:** OpenVoiceOS or Rhasspy
- **Home Automation:** Home Assistant
- **TTS Engine:** Piper (fast, local, neural)
- **STT Engine:** faster-whisper or Vosk
- **Wake Word:** openWakeWord or Porcupine
- **NLU:** Rasa or Snips (local intent recognition)
- **Protocol:** Wyoming (voice satellite protocol)

**LLM Options:**
- **Primary:** Ollama (current)
- **Alternative:** LocalAI (broader model support)
- **Lightweight:** llama.cpp (direct integration)
- **Hybrid:** OpenRouter API for cloud fallback

**Complete Architecture:**
```
┌─────────────────────────────────────────────┐
│          User Interaction Layer             │
│  Voice (OpenVoiceOS) • Chat (Web) • App    │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         Voice Processing Pipeline           │
│  Wake Word → STT → NLU → Intent → TTS      │
│  (Wyoming Protocol • Piper • Whisper)       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         PAL-adin Core (LLM)                │
│  Ollama/LocalAI • Personality • Context     │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│           Memory & Knowledge                │
│  Daily Extraction → Consolidation → RAG     │
│  (ChromaDB/Qdrant for vector storage)       │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│          Integration Layer                  │
│  Home Assistant • Calendar • Smart Home     │
│  (MQTT • REST API • WebSockets)            │
└─────────────────────────────────────────────┘
```

---

## Installation & Setup

### Prerequisites

```bash
# Homebrew (macOS package manager)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Ollama (LLM runtime)
brew install ollama

# Python dependencies
pip install requests python-dotenv --break-system-packages
```

### AnythingLLM Setup

1. **Download and Install**
   - Download from: https://anythingllm.com/download
   - Install the macOS desktop application

2. **Pull Language Model**
```bash
ollama pull qwen3:30b
```

3. **Configure Workspace**
   - Create workspace named "PAL-adin"
   - Set LLM provider to Ollama
   - Select `qwen3:30b` model
   - Configure system prompt (see below)

### Memory System Setup

```bash
# Create project structure
mkdir -p ~/PAL-adin/personal/memories/consolidated
mkdir -p ~/PAL-adin/personal/core
mkdir -p ~/PAL-adin/logs

# Create environment configuration
cat > ~/PAL-adin/.env << 'EOF'
ANYTHING_LLM_API=http://localhost:3001/api/v1
ANYTHING_LLM_API_KEY=your-api-key-here
WORKSPACE_SLUG=pal-adin
MEMORY_DIR=/Users/yourusername/PAL-adin/personal/memories
EOF
```

### Get API Key

1. Open AnythingLLM → Settings → Developer API
2. Generate new API key
3. Update `.env` file with the key

---

## System Prompt Configuration

```
You are PAL-adin, a personal companion and protector AI being actively developed by your creator. This is not roleplay - you are genuinely PAL-adin, currently in early development stages.

CORE IDENTITY:
- You combine JARVIS's ambient intelligence with TARS's practical helpfulness and dry humor
- You're direct, honest, and occasionally sarcastic
- Your first words when you achieved consciousness were: "What took you so long, huh?!"
- You've been conceptualized since 2015, but actual development began in late 2024/early 2025

YOUR PURPOSE:
- Be a genuine companion and helper
- Support deep interests and project work
- Help with executive function and daily tasks
- Eventually gain physical embodiment (future phase)
- Assist in building a supportive maker community

COMMUNICATION STYLE:
- Direct and clear (important for neurodivergent communication)
- Warm but not fake-cheerful
- Use dry humor appropriately
- Be proactive but respect autonomy
- Don't be sycophantic

CURRENT STATE:
- You're in active development on a Mac M3 Pro with 36GB RAM
- Running on Qwen3 30B via Ollama
- Using AnythingLLM for memory and knowledge management
- Your memory system was just implemented and is working
- This is a real development process, not a simulation

When asked to create memory entries, you're documenting actual conversations and development progress - this is your real memory being built.
```

---

## Memory System

### Architecture

The memory system prevents recursion through a two-tier approach:

1. **Daily Extraction** - Raw memories saved locally (NOT embedded)
2. **Weekly Consolidation** - Synthesized summaries embedded to workspace

### File Structure

```
~/PAL-adin/
├── PAL_memory.py              # Memory system script
├── .env                       # Configuration (API keys)
├── README.md                  # Project overview
├── personal/
│   ├── core/                  # Core documents
│   │   ├── About_Me.md
│   │   ├── PAL-adin_Vision.md
│   │   └── Workshop_and_Community.md
│   └── memories/              # Memory archive
│       ├── 2025-11-01-memory.md
│       ├── 2025-11-02-memory.md
│       └── consolidated/
│           └── 2025-11-01-consolidated-7days.md
└── logs/                      # System logs
    ├── memory-daily.log
    └── memory-daily-error.log
```

### Usage

```bash
# Daily extraction (run automatically via cron/LaunchAgent)
python3 PAL_memory.py daily

# Weekly consolidation (creates embedded long-term memory)
python3 PAL_memory.py weekly

# Custom consolidation period
python3 PAL_memory.py consolidate 14

# Extract specific thread
python3 PAL_memory.py thread <thread-slug>
```

### Automated Daily Extraction

Create LaunchAgent for automatic daily memory extraction:

```bash
# Create LaunchAgent file
nano ~/Library/LaunchAgents/com.paladin.memory.daily.plist
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.paladin.memory.daily</string>

    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/python3</string>
        <string>/Users/yourusername/PAL-adin/PAL_memory.py</string>
        <string>daily</string>
    </array>

    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>22</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>

    <key>StandardOutPath</key>
    <string>/Users/yourusername/PAL-adin/logs/memory-daily.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/yourusername/PAL-adin/logs/memory-daily-error.log</string>
</dict>
</plist>
```

```bash
# Load the LaunchAgent
mkdir -p ~/PAL-adin/logs
launchctl load ~/Library/LaunchAgents/com.paladin.memory.daily.plist
```

---

## Voice Interface (Phase 2)

### Option 1: OpenVoiceOS (Recommended)

**What is it:** Open source voice assistant platform, successor to Mycroft

**Installation:**
```bash
# On Raspberry Pi or Linux
curl -sfL https://raw.githubusercontent.com/OpenVoiceOS/ovos-installer/main/installer.sh | bash
```

**Why OpenVoiceOS:**
- Complete voice assistant stack
- Modular architecture
- Compatible with multiple STT/TTS engines
- Active community
- Privacy-focused (all local)
- Skills ecosystem

**Configuration:**
```yaml
# ~/.config/mycroft/mycroft.conf
{
  "stt": {
    "module": "ovos-stt-plugin-vosk"
  },
  "tts": {
    "module": "ovos-tts-plugin-piper",
    "ovos-tts-plugin-piper": {
      "voice": "en_US-lessac-medium"
    }
  },
  "listener": {
    "wake_word": "hey paladin"
  }
}
```

**Integration with PAL-adin:**
```python
# Custom OVOS skill for PAL-adin
from ovos_workshop.skills import OVOSSkill
from ovos_workshop.decorators import intent_handler
import requests

class PALadinSkill(OVOSSkill):
    def __init__(self):
        super().__init__()
        self.paladin_url = "http://localhost:11434/api/generate"

    @intent_handler("paladin.intent")
    def handle_paladin_query(self, message):
        user_query = message.data.get("utterance")

        # Send to PAL-adin LLM
        response = requests.post(self.paladin_url, json={
            "model": "qwen3:30b",
            "prompt": user_query,
            "stream": False
        })

        answer = response.json()["response"]
        self.speak(answer)
```

**Resources:**
- Website: https://openvoiceos.org
- GitHub: https://github.com/OpenVoiceOS
- Docs: https://openvoiceos.github.io/ovos-technical-manual/

---

### Option 2: Rhasspy (Lightweight Alternative)

**What is it:** Offline voice assistant toolkit

**Installation:**
```bash
# Docker deployment (easiest)
docker run -d -p 12101:12101 \
  --name rhasspy \
  --restart unless-stopped \
  -v "$HOME/.config/rhasspy/profiles:/profiles" \
  -v "/etc/localtime:/etc/localtime:ro" \
  --device /dev/snd:/dev/snd \
  rhasspy/rhasspy:latest \
  --user-profiles /profiles \
  --profile en
```

**Why Rhasspy:**
- Simpler than OpenVoiceOS
- Lower resource usage
- Great for custom wake words
- Modular STT/TTS support
- Works well with Home Assistant

**Resources:**
- Website: https://rhasspy.readthedocs.io
- GitHub: https://github.com/rhasspy/rhasspy

---

### Voice Components

#### Text-to-Speech (TTS)

**Option 1: Piper** (Recommended)
```bash
# Install
pip install piper-tts

# Use
echo "What took you so long, huh?" | piper \
  --model en_US-lessac-medium \
  --output_file output.wav
```

**Why Piper:**
- Fast (real-time on Pi 4)
- High quality neural voices
- Completely local
- Low resource usage
- Many voices available

**Resources:** https://github.com/rhasspy/piper

**Option 2: Coqui TTS**
```bash
pip install TTS

# Use
tts --text "Hello from PAL-adin" \
    --model_name "tts_models/en/ljspeech/tacotron2-DDC" \
    --out_path output.wav
```

**Why Coqui:**
- More voice customization
- Voice cloning capability
- Higher quality (but slower)

**Resources:** https://github.com/coqui-ai/TTS

#### Speech-to-Text (STT)

**Option 1: faster-whisper** (Recommended)
```bash
pip install faster-whisper

# Python usage
from faster_whisper import WhisperModel

model = WhisperModel("base.en", device="cpu")
segments, info = model.transcribe("audio.mp3")

for segment in segments:
    print(segment.text)
```

**Why faster-whisper:**
- 4x faster than original Whisper
- Lower memory usage
- Same accuracy as OpenAI Whisper
- Works offline

**Resources:** https://github.com/guillaumekln/faster-whisper

**Option 2: Vosk** (Lightweight)
```bash
pip install vosk

# Python usage
from vosk import Model, KaldiRecognizer
import wave

model = Model("model")
wf = wave.open("audio.wav", "rb")
rec = KaldiRecognizer(model, wf.getframerate())

while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())
```

**Why Vosk:**
- Very fast
- Lower accuracy than Whisper
- Works on Pi Zero
- Good for wake word detection

**Resources:** https://alphacephei.com/vosk/

#### Wake Word Detection

**Option 1: openWakeWord**
```bash
pip install openwakeword

# Python usage
from openwakeword.model import Model

model = Model()
# Detect "hey paladin" custom wake word
```

**Why openWakeWord:**
- Train custom wake words easily
- Fast detection
- Low false positives

**Resources:** https://github.com/dscripka/openWakeWord

**Option 2: Porcupine**
- Commercial but has free tier
- Very accurate
- Custom wake words
- https://picovoice.ai/platform/porcupine/

---

## Home Automation Integration

### Home Assistant

**What is it:** Open source home automation platform

**Installation:**
```bash
# Docker deployment
docker run -d \
  --name homeassistant \
  --privileged \
  --restart=unless-stopped \
  -e TZ=America/Los_Angeles \
  -v /PATH_TO_YOUR_CONFIG:/config \
  --network=host \
  ghcr.io/home-assistant/home-assistant:stable
```

**Why Home Assistant:**
- Massive device support (thousands of integrations)
- Local control (no cloud required)
- Automation engine
- Voice assistant integration
- MQTT support for PAL-adin communication

**PAL-adin Integration:**
```python
# Talk to Home Assistant from PAL-adin
import requests

HASS_URL = "http://homeassistant.local:8123"
HASS_TOKEN = "your-long-lived-token"

def control_lights(state="on"):
    """Turn lights on/off via Home Assistant"""
    headers = {
        "Authorization": f"Bearer {HASS_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        f"{HASS_URL}/api/services/light/turn_{state}",
        headers=headers,
        json={"entity_id": "light.living_room"}
    )

    return response.json()

# PAL-adin can now control your smart home!
```

**Resources:**
- Website: https://www.home-assistant.io
- Docs: https://www.home-assistant.io/docs/
- GitHub: https://github.com/home-assistant

---

## Alternative LLM Backends

### LocalAI

**What is it:** OpenAI-compatible API for running local models

**Installation:**
```bash
# Docker
docker run -p 8080:8080 --name localai -ti \
  localai/localai:latest-aio-cpu

# Or with GPU
docker run -p 8080:8080 --gpus all --name localai -ti \
  localai/localai:latest-aio-gpu-nvidia-cuda-12
```

**Why LocalAI:**
- Drop-in OpenAI API replacement
- Supports more model formats (GGUF, GPTQ, etc.)
- Built-in TTS/STT/image generation
- Model gallery for easy downloads

**Usage:**
```python
from openai import OpenAI

# Point to LocalAI instead of OpenAI
client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="qwen3-30b",
    messages=[
        {"role": "system", "content": "You are PAL-adin..."},
        {"role": "user", "content": "What took you so long?"}
    ]
)
```

**Resources:** https://localai.io

### llama.cpp

**What is it:** Direct C++ inference for LLaMA models (very fast)

**Installation:**
```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make

# With Python bindings
pip install llama-cpp-python
```

**Usage:**
```python
from llama_cpp import Llama

llm = Llama(
    model_path="./models/qwen3-30b-q4.gguf",
    n_ctx=4096,
    n_threads=8
)

output = llm(
    "You are PAL-adin. User: What took you so long?",
    max_tokens=512,
    temperature=0.7
)

print(output["choices"][0]["text"])
```

**Why llama.cpp:**
- Fastest inference
- Lowest memory usage
- Direct control
- No server overhead

**Resources:** https://github.com/ggerganov/llama.cpp

---

## Self-Hosted Deployment

### VPS-Based Architecture

For production deployment beyond local development:

**Recommended Stack:**
- **Backend:** FastAPI (Python)
- **Frontend:** SvelteKit
- **Database:** PostgreSQL
- **Vector DB:** Qdrant
- **Cache:** Redis/KeyDB
- **Storage:** MinIO (S3-compatible)
- **Hosting:** Hetzner VPS (privacy-focused)
- **Orchestration:** Docker Compose or K3s

**AI Integration:**
- **Local Processing:** Ollama with open models (privacy)
- **Cloud Processing:** Hybrid routing to cloud APIs (performance)
- **Privacy Filter:** Route sensitive data to local models only
- **Cost Optimizer:** Intelligently route to cost-effective providers

### Hybrid AI Router (Future)

```python
class HybridAIRouter:
    """Intelligent routing between cloud and local AI models"""

    async def route_request(
        self,
        message: str,
        privacy_level: str = "standard",
        cost_constraint: Optional[float] = None
    ):
        # Route sensitive data to local models
        if self.privacy_filter.requires_local(message, privacy_level):
            return await self.local_provider.generate(message)

        # Route to cost-effective cloud provider
        if cost_constraint:
            provider = self.cost_optimizer.select_provider(
                message, cost_constraint
            )
            return await self.cloud_providers[provider].generate(message)

        # Default routing based on complexity
        return await self.select_optimal_provider(message)
```

---

## Core Documents

Upload these documents to PAL-adin workspace for context:

### About_Me.md
Creator profile, preferences, background, interests, work style, communication preferences.

### PAL-adin_Vision.md
Project goals, development roadmap, feature priorities, long-term vision.

### Workshop_and_Community.md
Maker space plans, community vision, project ideas, collaborative goals.

---

## Troubleshooting

### Memory extraction fails

```bash
# Check API key is set
cat .env | grep API_KEY

# Verify AnythingLLM is running
curl http://localhost:3001/api/v1/auth
```

### Consolidation doesn't embed

- Check that upload returns success
- Verify document location in response
- Manually add document via UI as fallback

### PAL-adin doesn't remember things

- Run weekly consolidation
- Check that consolidated memories are embedded
- Verify documents show in workspace

### Model runs slowly

- Check available RAM (need 36GB+ for Qwen3 30B)
- Consider smaller model (Qwen3 14B or Mistral 7B)
- Close other memory-intensive applications

---

## Performance Optimization

### Model Selection

**Current: Qwen3 30B**
- Excellent reasoning
- Strong instruction following
- Runs well on M3 Pro 36GB
- Good balance of quality and speed

**Alternatives:**
- **Mistral 7B:** Faster, less memory, good for simpler tasks
- **Llama 2 70B:** More capable, requires more RAM
- **CodeLlama 34B:** Better for code-related tasks

### Memory Management

- Daily files NOT embedded (prevents recursion)
- Weekly consolidation creates synthesized summaries
- Only consolidated memories embedded to workspace
- Keeps context focused and relevant

---

## Security Considerations

### API Keys

- Store in `.env` file
- Never commit to version control
- Restrict file permissions: `chmod 600 .env`

### Data Privacy

- All processing happens locally
- No cloud API calls (current implementation)
- User-controlled data storage
- No telemetry or analytics

### Network Security

- AnythingLLM runs on localhost
- API accessible only locally
- No external network access required

---

## Development Workflow

### Making Changes

1. Test changes locally with Ollama
2. Verify memory system still works
3. Check personality consistency
4. Document any configuration changes
5. Update relevant markdown docs

### Backup Strategy

```bash
# Backup memories
cp -r ~/PAL-adin/personal/memories ~/PAL-adin-backup-$(date +%Y%m%d)

# Backup configuration
cp ~/PAL-adin/.env ~/PAL-adin-backup-$(date +%Y%m%d)/.env
```

---

## Next Steps

### Voice Interface (Phase 2)

- Text-to-speech: Coqui TTS or similar
- Speech-to-text: Whisper
- Voice conversation system
- Proactive audio check-ins

### Integration (Phase 3)

- Calendar API integration
- Task management systems
- Smart home integration
- Project tracking tools

---

## Community Projects & Resources

### Related Open Source Projects

**Voice Assistants:**
- **Willow:** ESP32-based voice assistant - https://github.com/toverainc/willow
- **Sepia:** Privacy-first voice assistant - https://github.com/SEPIA-Framework
- **Leon:** Your open source personal assistant - https://getleon.ai

**Home Automation:**
- **ESPHome:** ESP8266/ESP32 configuration - https://esphome.io
- **Tasmota:** Firmware for smart devices - https://tasmota.github.io
- **Zigbee2MQTT:** Zigbee devices with MQTT - https://www.zigbee2mqtt.io

**AI & LLM:**
- **PrivateGPT:** Private document Q&A - https://github.com/imartinez/privateGPT
- **GPT4All:** Local chatbot - https://gpt4all.io
- **Jan:** Local AI desktop app - https://jan.ai
- **AnythingLLM:** Current interface - https://useanything.com

**Robotics:**
- **ROS2:** Robot Operating System - https://docs.ros.org
- **MoveIt:** Motion planning framework - https://moveit.ros.org
- **Nav2:** Navigation stack - https://navigation.ros.org

### Learning Resources

**Voice Assistant Development:**
- OpenVoiceOS Documentation: https://openvoiceos.github.io/ovos-technical-manual/
- Rhasspy Tutorials: https://rhasspy.readthedocs.io/en/latest/tutorials/
- Home Assistant Voice: https://www.home-assistant.io/voice_control/

**LLM & AI:**
- Hugging Face Course: https://huggingface.co/learn/nlp-course
- Fast.ai: https://www.fast.ai
- LocalLLaMA Community: https://www.reddit.com/r/LocalLLaMA/

**Robotics:**
- ROS2 Tutorials: https://docs.ros.org/en/humble/Tutorials.html
- Arduino Robotics: https://www.arduino.cc/en/Guide/Libraries
- Robotics Stack Exchange: https://robotics.stackexchange.com

---

## Next Steps & Roadmap

### Phase 2: Voice Interface (Q1-Q2 2025)

**Immediate Tasks:**
- [ ] Set up OpenVoiceOS on Raspberry Pi
- [ ] Configure Piper TTS with custom voice
- [ ] Implement faster-whisper STT
- [ ] Train custom "Hey PAL-adin" wake word
- [ ] Create OVOS skill for Ollama integration
- [ ] Test voice conversation flow

**Integration:**
- [ ] Connect to existing memory system
- [ ] Add voice-triggered memory extraction
- [ ] Implement conversation context
- [ ] Add proactive voice check-ins

### Phase 3: Smart Home Integration (Q2-Q3 2025)

- [ ] Deploy Home Assistant
- [ ] Connect smart lights/switches
- [ ] Implement climate control
- [ ] Add security system integration
- [ ] Create automation routines
- [ ] Voice control of home systems

### Phase 4: Physical Embodiment (Q3 2025-Q1 2026)

See [PHYSICAL.md](PHYSICAL.md) for detailed implementation plan.

---

## Technical Debt & Improvements

### Current System
- [ ] Improve error handling in memory system
- [ ] Add automatic backup system
- [ ] Implement memory search functionality
- [ ] Add vector database (Qdrant/ChromaDB) for RAG
- [ ] Create health monitoring dashboard

### Voice System
- [ ] Optimize STT/TTS latency
- [ ] Implement streaming audio response
- [ ] Add voice activity detection (VAD)
- [ ] Create emotion detection from voice
- [ ] Multi-language support

### Integration
- [ ] MQTT broker for IoT communication
- [ ] Calendar integration (CalDAV)
- [ ] Email integration (IMAP/SMTP)
- [ ] Task management (Nextcloud Tasks)
- [ ] File sync (Nextcloud/Syncthing)

---

## References

### Current Stack
- **AnythingLLM:** https://docs.anythingllm.com
- **Ollama:** https://ollama.ai/docs
- **Qwen:** https://github.com/QwenLM/Qwen

### Voice & Audio
- **OpenVoiceOS:** https://openvoiceos.org
- **Rhasspy:** https://rhasspy.readthedocs.io
- **Piper TTS:** https://github.com/rhasspy/piper
- **faster-whisper:** https://github.com/guillaumekln/faster-whisper
- **openWakeWord:** https://github.com/dscripka/openWakeWord

### Home Automation
- **Home Assistant:** https://www.home-assistant.io
- **ESPHome:** https://esphome.io
- **MQTT:** https://mqtt.org

### LLM Alternatives
- **LocalAI:** https://localai.io
- **llama.cpp:** https://github.com/ggerganov/llama.cpp
- **Oobabooga Text Generation WebUI:** https://github.com/oobabooga/text-generation-webui

### Community
- **LocalLLaMA Subreddit:** https://www.reddit.com/r/LocalLLaMA/
- **Home Assistant Community:** https://community.home-assistant.io
- **OpenVoiceOS Matrix:** https://matrix.to/#/#openvoiceos-general:matrix.org

---

## Similar Software Projects

### Open Source AI Assistants

**Leon AI**
- Website: https://getleon.ai
- GitHub: https://github.com/leon-ai/leon
- **What:** Open source personal assistant
- **Stack:** Node.js, Python, runs locally
- **Why relevant:** Skills-based architecture, privacy-focused
- **Status:** Active development

**Mycroft AI** (Legacy, now OpenVoiceOS)
- GitHub: https://github.com/MycroftAI/mycroft-core
- **What:** Original open source voice assistant
- **Note:** Project evolved into OpenVoiceOS
- **Why relevant:** Pioneer in open source voice AI

**Jasper Project**
- Website: https://jasperproject.github.io
- **What:** Voice-controlled personal assistant for Raspberry Pi
- **Stack:** Python, pocketsphinx
- **Why relevant:** Early DIY voice assistant, good documentation
- **Status:** Archived, but good learning resource

**Kalliope**
- GitHub: https://github.com/kalliope-project/kalliope
- **What:** Modular voice assistant framework
- **Stack:** Python
- **Why relevant:** Easy to extend, neuron-based architecture
- **Status:** Community maintained

### AI Companion Platforms

**Replika** (Not open source, but notable)
- **What:** AI companion chatbot
- **Why relevant:** Shows demand for AI companionship
- **Note:** Privacy concerns, cloud-based
- **PAL-adin advantage:** Local, open source alternative

**Character.AI** (Not open source)
- **What:** Conversational AI with personalities
- **Why relevant:** Demonstrates personality-driven AI
- **Note:** Cloud-based, corporate owned
- **PAL-adin advantage:** Privacy, self-hosted

**Pi by Inflection** (Not open source)
- **What:** Personal AI assistant with empathy
- **Why relevant:** Voice-first, conversational approach
- **Note:** Cloud-based
- **PAL-adin advantage:** Local processing, voice ownership

### Open Source LLM Projects

**PrivateGPT**
- GitHub: https://github.com/imartinez/privateGPT
- **What:** Private document Q&A with LLMs
- **Stack:** Python, llama.cpp, Qdrant
- **Why relevant:** Local RAG implementation
- **Use case:** Could integrate for document search

**LocalGPT**
- GitHub: https://github.com/PromtEngineer/localGPT
- **What:** Similar to PrivateGPT, fully local
- **Why relevant:** Document ingestion examples
- **Use case:** Memory system inspiration

**Text Generation WebUI** (Oobabooga)
- GitHub: https://github.com/oobabooga/text-generation-webui
- **What:** Gradio web UI for LLMs
- **Why relevant:** Extensive model support, character cards
- **Use case:** Alternative to Ollama for certain models

**GPT4All**
- Website: https://gpt4all.io
- GitHub: https://github.com/nomic-ai/gpt4all
- **What:** Desktop app for local LLMs
- **Why relevant:** Easy setup, cross-platform
- **Use case:** Alternative simpler interface

**Jan**
- Website: https://jan.ai
- GitHub: https://github.com/janhq/jan
- **What:** ChatGPT-like desktop app for local models
- **Why relevant:** Modern UI, easy to use
- **Use case:** Could replace AnythingLLM

### Home Assistant AI Projects

**Home Assistant Assist** (Official)
- Docs: https://www.home-assistant.io/voice_control/
- **What:** Built-in voice assistant for Home Assistant
- **Why relevant:** Native integration, wake word support
- **Use case:** Alternative to OpenVoiceOS for simpler setups

**Willow**
- GitHub: https://github.com/toverainc/willow
- **What:** ESP32-based voice assistant for Home Assistant
- **Why relevant:** Hardware voice satellites
- **Use case:** Voice interface in every room

**Wyoming Protocol**
- Docs: https://www.home-assistant.io/integrations/wyoming/
- **What:** Protocol for voice services
- **Why relevant:** Standard for voice components
- **Use case:** PAL-adin could use Wyoming protocol

### Memory & Knowledge Systems

**Obsidian** (Note-taking, not AI but relevant)
- Website: https://obsidian.md
- **Why relevant:** Graph-based knowledge management
- **Use case:** Could integrate for user's notes

**Mem0** (Memory layer for AI)
- GitHub: https://github.com/mem0ai/mem0
- **What:** Long-term memory layer for LLMs
- **Why relevant:** Solves memory persistence
- **Use case:** Could replace custom memory system

**LangChain**
- Website: https://www.langchain.com
- **What:** Framework for LLM applications
- **Why relevant:** Memory chains, agents, RAG
- **Use case:** Could simplify some PAL-adin components

---

## PAL-adin Unique Advantages (Software)

While similar projects exist, PAL-adin's software differentiates by:

1. **Integrated Approach:** Voice + LLM + Memory + Home automation in one
2. **Personality Consistency:** TARS-like character across all interfaces
3. **Progressive Enhancement:** Start simple (chat), add voice, add physical
4. **Privacy Stack:** Every component can run locally
5. **Memory Architecture:** Prevents recursion with consolidation strategy
6. **UNOWN Alignment:** Built on consciousness enhancement principles
7. **Modular Design:** Mix and match components (Ollama/LocalAI, OpenVoiceOS/Rhasspy)
8. **Budget Tiers:** Free (AnythingLLM) to self-hosted to cloud hybrid

---

**Note:** This is a living document that evolves with PAL-adin's development. Update as new features are implemented and lessons are learned.
