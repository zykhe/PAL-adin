# PAL-adin UNOWN Branding & Design System

## 🟣 UNOWN Visual Identity

### Core Philosophy
UNOWN's visual identity embodies the principles of anonymity, decentralization, and consciousness enhancement. The design must be:
- **Anonymous**: No identifiable creators or personalities
- **Decentralized**: No central focal point or hierarchy
- **Consciousness-focused**: Represents enhancement and protection
- **Privacy-first**: Secure and protective visual language

### Primary Color Palette

#### Purple Spectrum (UNOWN Primary)
```css
:root {
  /* Core Purple - Mystery, Consciousness, Transformation */
  --purple-50: #f5f3ff;    /* Lightest - Ethereal */
  --purple-100: #ede9fe;   /* Very Light - Awakening */
  --purple-200: #ddd6fe;   /* Light - Awareness */
  --purple-300: #c4b5fd;   /* Medium Light - Insight */
  --purple-400: #a78bfa;   /* Medium - Understanding */
  --purple-500: #8b5cf6;   /* Primary - Consciousness */
  --purple-600: #7c3aed;   /* Primary Dark - Deep Thought */
  --purple-700: #6d28d9;   /* Dark - Wisdom */
  --purple-800: #5b21b6;   /* Darker - Mystery */
  --purple-900: #4c1d95;   /* Darkest - Unknown */
  
  /* Accent Colors */
  --accent-cyan: #06b6d4;    /* Digital - Technology */
  --accent-magenta: #ec4899;  /* Enhancement - Transformation */
  --accent-green: #10b981;    /* Growth - Evolution */
  --accent-amber: #f59e0b;    /* Warning - Caution */
  --accent-red: #ef4444;       /* Danger - Protection */
}
```

#### Dark Theme (UNOWN Default)
```css
:root[data-theme="dark"] {
  /* Background Colors */
  --bg-primary: #0f0a1f;        /* Deep Space - Unknown */
  --bg-secondary: #1a1625;      /* Void - Mystery */
  --bg-tertiary: #252134;       /* Shadow - Hidden */
  --bg-elevated: #2d2840;       /* Surface - Revealed */
  
  /* Surface Colors */
  --surface-primary: #352f4a;     /* Interactive */
  --surface-secondary: #403857;    /* Hover */
  --surface-tertiary: #4a4164;    /* Active */
  
  /* Text Colors */
  --text-primary: #e9d5ff;      /* Main - Conscious */
  --text-secondary: #c4b5fd;     /* Secondary - Thought */
  --text-muted: #a78bfa;          /* Muted - Memory */
  --text-dim: #8b5cf6;           /* Dim - Subconscious */
  
  /* Border Colors */
  --border-subtle: #2d2840;      /* Hidden */
  --border-default: #403857;       /* Visible */
  --border-strong: #4a4164;       /* Emphasized */
}
```

### Typography

#### UNOWN Font System
```css
/* UNOWN Typography - Anonymous, Technical, Conscious */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
  /* Font Families */
  --font-mono: 'JetBrains Mono', 'Fira Code', 'SF Mono', monospace;
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-display: 'Inter', sans-serif;
  
  /* Font Sizes */
  --text-xs: 0.75rem;      /* 12px - System messages */
  --text-sm: 0.875rem;     /* 14px - Metadata */
  --text-base: 1rem;        /* 16px - Body text */
  --text-lg: 1.125rem;      /* 18px - Emphasized */
  --text-xl: 1.25rem;       /* 20px - Small headings */
  --text-2xl: 1.5rem;       /* 24px - Section headings */
  --text-3xl: 1.875rem;     /* 30px - Main headings */
  --text-4xl: 2.25rem;       /* 36px - Display */
  
  /* Font Weights */
  --font-light: 300;          /* Subtle information */
  --font-normal: 400;         /* Standard text */
  --font-medium: 500;        /* Emphasized */
  --font-semibold: 600;       /* Headings */
  --font-bold: 700;          /* Strong emphasis */
  
  /* Line Heights */
  --leading-tight: 1.25;      /* Dense information */
  --leading-normal: 1.5;       /* Readable text */
  --leading-relaxed: 1.75;     /* Comfortable reading */
}
```

## 🟣 Logo & Symbol System

### UNOWN Symbol
The UNOWN symbol represents decentralized consciousness and anonymous collaboration:

```svg
<!-- UNOWN Symbol - Decentralized Network -->
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <!-- Outer Circle - Protection -->
  <circle cx="50" cy="50" r="45" fill="none" stroke="#8b5cf6" stroke-width="2" opacity="0.8"/>
  
  <!-- Inner Nodes - Decentralized Network -->
  <circle cx="50" cy="20" r="4" fill="#c4b5fd"/>
  <circle cx="75" cy="35" r="4" fill="#c4b5fd"/>
  <circle cx="75" cy="65" r="4" fill="#c4b5fd"/>
  <circle cx="50" cy="80" r="4" fill="#c4b5fd"/>
  <circle cx="25" cy="65" r="4" fill="#c4b5fd"/>
  <circle cx="25" cy="35" r="4" fill="#c4b5fd"/>
  
  <!-- Connections - Network Links -->
  <line x1="50" y1="20" x2="75" y2="35" stroke="#8b5cf6" stroke-width="1" opacity="0.6"/>
  <line x1="75" y1="35" x2="75" y2="65" stroke="#8b5cf6" stroke-width="1" opacity="0.6"/>
  <line x1="75" y1="65" x2="50" y2="80" stroke="#8b5cf6" stroke-width="1" opacity="0.6"/>
  <line x1="50" y1="80" x2="25" y2="65" stroke="#8b5cf6" stroke-width="1" opacity="0.6"/>
  <line x1="25" y1="65" x2="25" y2="35" stroke="#8b5cf6" stroke-width="1" opacity="0.6"/>
  <line x1="25" y1="35" x2="50" y2="20" stroke="#8b5cf6" stroke-width="1" opacity="0.6"/>
  
  <!-- Center - Consciousness Core -->
  <circle cx="50" cy="50" r="8" fill="none" stroke="#e9d5ff" stroke-width="2"/>
  <circle cx="50" cy="50" r="3" fill="#e9d5ff"/>
</svg>
```

### PAL-adin Logo Variation
```svg
<!-- PAL-adin UNOWN Logo -->
<svg viewBox="0 0 200 60" xmlns="http://www.w3.org/2000/svg">
  <!-- UNOWN Symbol -->
  <g transform="translate(10, 10)">
    <circle cx="20" cy="20" r="18" fill="none" stroke="#8b5cf6" stroke-width="1.5" opacity="0.8"/>
    <circle cx="20" cy="8" r="2" fill="#c4b5fd"/>
    <circle cx="30" cy="14" r="2" fill="#c4b5fd"/>
    <circle cx="30" cy="26" r="2" fill="#c4b5fd"/>
    <circle cx="20" cy="32" r="2" fill="#c4b5fd"/>
    <circle cx="10" cy="26" r="2" fill="#c4b5fd"/>
    <circle cx="10" cy="14" r="2" fill="#c4b5fd"/>
    <circle cx="20" cy="20" r="4" fill="none" stroke="#e9d5ff" stroke-width="1.5"/>
    <circle cx="20" cy="20" r="1.5" fill="#e9d5ff"/>
  </g>
  
  <!-- PAL-adin Text -->
  <text x="50" y="35" font-family="'JetBrains Mono', monospace" font-size="18" font-weight="600" fill="#e9d5ff">
    PAL-adin
  </text>
  
  <!-- UNOWN Tagline -->
  <text x="50" y="50" font-family="'Inter', sans-serif" font-size="10" font-weight="400" fill="#a78bfa" opacity="0.8">
    UNOWN PROTOCOL
  </text>
</svg>
```

## 🟣 Component Design System

### Button System
```css
/* UNOWN Button System - Anonymous, Functional, Conscious */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-2) var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: 6px;
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: var(--font-medium);
  text-decoration: none;
  cursor: pointer;
  transition: all 0.2s ease;
  background: var(--surface-primary);
  color: var(--text-primary);
}

.btn:hover {
  background: var(--surface-secondary);
  border-color: var(--border-strong);
  transform: translateY(-1px);
}

.btn:active {
  transform: translateY(0);
}

.btn-primary {
  background: var(--purple-600);
  border-color: var(--purple-600);
  color: white;
}

.btn-primary:hover {
  background: var(--purple-700);
  border-color: var(--purple-700);
}

.btn-ghost {
  background: transparent;
  border-color: var(--border-subtle);
  color: var(--text-secondary);
}

.btn-ghost:hover {
  background: var(--surface-primary);
  border-color: var(--border-default);
  color: var(--text-primary);
}

.btn-danger {
  background: var(--accent-red);
  border-color: var(--accent-red);
  color: white;
}

.btn-danger:hover {
  background: #dc2626;
  border-color: #dc2626;
}
```

### Card Component
```css
/* UNOWN Card - Protected Information Container */
.card {
  background: var(--bg-elevated);
  border: 1px solid var(--border-default);
  border-radius: 8px;
  padding: var(--space-6);
  box-shadow: 0 4px 6px -1px rgba(139, 92, 246, 0.1);
  transition: all 0.2s ease;
}

.card:hover {
  border-color: var(--border-strong);
  box-shadow: 0 8px 12px -2px rgba(139, 92, 246, 0.15);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-3);
  border-bottom: 1px solid var(--border-subtle);
}

.card-title {
  font-family: var(--font-sans);
  font-size: var(--text-lg);
  font-weight: var(--font-semibold);
  color: var(--text-primary);
  margin: 0;
}

.card-content {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  color: var(--text-secondary);
}

.card-footer {
  margin-top: var(--space-4);
  padding-top: var(--space-3);
  border-top: 1px solid var(--border-subtle);
  display: flex;
  justify-content: flex-end;
  gap: var(--space-2);
}
```

### Message Bubble (Chat Interface)
```css
/* UNOWN Message Bubble - Conscious Communication */
.message {
  display: flex;
  margin-bottom: var(--space-4);
  animation: messageSlideIn 0.3s ease-out;
}

.message.user {
  justify-content: flex-end;
}

.message.assistant {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 70%;
  padding: var(--space-3) var(--space-4);
  border-radius: 12px;
  font-family: var(--font-sans);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  position: relative;
}

.message.user .message-bubble {
  background: var(--purple-600);
  color: white;
  border-bottom-right-radius: 4px;
}

.message.assistant .message-bubble {
  background: var(--surface-primary);
  color: var(--text-primary);
  border: 1px solid var(--border-default);
  border-bottom-left-radius: 4px;
}

.message-metadata {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-top: var(--space-1);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--text-dim);
}

.message-thinking {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: var(--space-1) var(--space-2);
  background: var(--bg-tertiary);
  border-radius: 12px;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--text-muted);
}

.thinking-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--purple-500);
  animation: thinkingPulse 1.4s infinite ease-in-out;
}

.thinking-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.thinking-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes messageSlideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes thinkingPulse {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 1;
  }
}
```

## 🟣 Layout System

### Grid System
```css
/* UNOWN Grid - Decentralized Layout */
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--space-4);
}

.grid {
  display: grid;
  gap: var(--space-4);
}

.grid-cols-1 { grid-template-columns: repeat(1, 1fr); }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }

.flex {
  display: flex;
}

.flex-col {
  flex-direction: column;
}

.items-center {
  align-items: center;
}

.justify-center {
  justify-content: center;
}

.justify-between {
  justify-content: space-between;
}

.gap-2 { gap: var(--space-2); }
.gap-4 { gap: var(--space-4); }
.gap-6 { gap: var(--space-6); }
.gap-8 { gap: var(--space-8); }
```

### Chat Layout
```css
/* UNOWN Chat Interface - Conscious Communication */
.chat-container {
  display: flex;
  height: 100vh;
  background: var(--bg-primary);
}

.chat-sidebar {
  width: 280px;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-default);
  display: flex;
  flex-direction: column;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
}

.chat-header {
  padding: var(--space-4) var(--space-6);
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-default);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-6);
  display: flex;
  flex-direction: column;
}

.chat-input-container {
  padding: var(--space-4) var(--space-6);
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-default);
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-2);
}

.conversation-item {
  padding: var(--space-3) var(--space-4);
  border-radius: 6px;
  margin-bottom: var(--space-1);
  cursor: pointer;
  transition: all 0.2s ease;
  border: 1px solid transparent;
}

.conversation-item:hover {
  background: var(--surface-primary);
  border-color: var(--border-default);
}

.conversation-item.active {
  background: var(--surface-secondary);
  border-color: var(--purple-600);
}
```

## 🟣 Animation & Micro-interactions

### Conscious Animations
```css
/* UNOWN Animations - Subtle, Conscious, Protective */
.fade-in {
  animation: fadeIn 0.3s ease-out;
}

.slide-up {
  animation: slideUp 0.3s ease-out;
}

.pulse-glow {
  animation: pulseGlow 2s infinite ease-in-out;
}

.consciousness-ripple {
  position: relative;
  overflow: hidden;
}

.consciousness-ripple::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(139, 92, 246, 0.3);
  transform: translate(-50%, -50%);
  animation: ripple 0.6s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulseGlow {
  0%, 100% {
    box-shadow: 0 0 5px rgba(139, 92, 246, 0.3);
  }
  50% {
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.6);
  }
}

@keyframes ripple {
  to {
    width: 200px;
    height: 200px;
    opacity: 0;
  }
}
```

## 🟣 Responsive Design

### Mobile-First Approach
```css
/* UNOWN Responsive - Universal Access */
/* Mobile (Default) */
.chat-sidebar {
  position: fixed;
  left: -280px;
  top: 0;
  height: 100vh;
  z-index: 1000;
  transition: left 0.3s ease;
}

.chat-sidebar.open {
  left: 0;
}

.chat-main {
  width: 100%;
}

/* Tablet */
@media (min-width: 768px) {
  .chat-sidebar {
    position: relative;
    left: 0;
    width: 300px;
  }
  
  .chat-main {
    width: calc(100% - 300px);
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .chat-sidebar {
    width: 320px;
  }
  
  .chat-main {
    width: calc(100% - 320px);
  }
  
  .container {
    padding: 0 var(--space-8);
  }
}

/* Large Desktop */
@media (min-width: 1440px) {
  .container {
    max-width: 1400px;
  }
  
  .grid-cols-4 {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

## 🟣 Accessibility & Privacy

### Accessibility Features
```css
/* UNOWN Accessibility - Universal Access */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.focus-visible {
  outline: 2px solid var(--purple-500);
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

@media (prefers-color-scheme: light) {
  :root {
    --bg-primary: #faf5ff;
    --bg-secondary: #f3e8ff;
    --text-primary: #4c1d95;
    --text-secondary: #6d28d9;
  }
}
```

### Privacy Indicators
```css
/* UNOWN Privacy Indicators - Trust & Transparency */
.privacy-indicator {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-1) var(--space-2);
  background: var(--bg-tertiary);
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--text-muted);
}

.privacy-indicator.encrypted {
  color: var(--accent-green);
}

.privacy-indicator.anonymous {
  color: var(--purple-500);
}

.privacy-indicator.secure {
  color: var(--accent-cyan);
}

.privacy-badge {
  position: absolute;
  top: var(--space-2);
  right: var(--space-2);
  padding: var(--space-1) var(--space-2);
  background: var(--purple-600);
  color: white;
  border-radius: 4px;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
}
```

This UNOWN-compliant design system ensures PAL-adin maintains visual consistency while embodying the principles of anonymity, decentralization, and consciousness enhancement. The purple color palette represents mystery and transformation, while the clean, technical aesthetic reflects the privacy-first, open-source nature of the project.