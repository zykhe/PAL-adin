# Contributing to PAL-adin

Thank you for your interest in contributing to PAL-adin! This document provides guidelines and information for contributors to help us build a better AI assistant together.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Community](#community)

## Code of Conduct

### Our Pledge

We are committed to making participation in our project a harassment-free experience for everyone, regardless of:

- Age, body size, disability, ethnicity, gender identity and expression
- Level of experience, education, socioeconomic status, nationality, personal appearance
- Race, religion, or sexual identity

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- The use of sexualized language or imagery
- Personal attacks or political commentary
- Public or private harassment
- Publishing others' private information without explicit permission
- Any other conduct which could reasonably be considered inappropriate

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+ LTS
- Docker and Docker Compose
- Git
- A code editor (we recommend VS Code with Svelte extension)

### Development Environment Setup

1. **Fork and Clone**
```bash
git clone https://github.com/YOUR_USERNAME/paladin.git
cd paladin
```

2. **Set Up Development Environment**
```bash
# Copy environment template
cp .env.example .env

# Start development services
docker-compose -f docker-compose.dev.yml up -d

# Install backend dependencies
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements/dev.txt

# Install frontend dependencies
cd ../frontend
npm install
```

3. **Run Tests**
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Development Workflow

### Branch Strategy

We use a simplified Git flow:

- `main`: Stable, production-ready code
- `develop`: Integration branch for features
- `feature/*`: New features and enhancements
- `bugfix/*`: Bug fixes
- `hotfix/*`: Critical fixes for production

### Creating a Feature Branch

1. **Update your fork**
```bash
git checkout main
git pull upstream main
git checkout develop
git pull upstream develop
```

2. **Create feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Make your changes**
- Follow the coding standards
- Write tests for new functionality
- Update documentation as needed

4. **Commit your changes**
```bash
git add .
git commit -m "feat: add your feature description"
```

### Commit Message Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(ai): add GLM-4.6 provider integration
fix(auth): resolve JWT token expiration issue
docs(api): update authentication endpoints
```

## Coding Standards

### Python (Backend)

#### Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://black.readthedocs.io/) for formatting
- Use [isort](https://isort.readthedocs.io/) for import sorting
- Maximum line length: 88 characters

#### Type Hints
```python
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    preferences: Optional[Dict[str, Any]] = None
```

#### Documentation
```python
def process_message(message: str, user_id: int) -> Dict[str, Any]:
    """
    Process a user message and generate AI response.
    
    Args:
        message: The user's input message
        user_id: The ID of the user sending the message
        
    Returns:
        Dictionary containing the AI response and metadata
        
    Raises:
        ValueError: If the message is empty or invalid
        AuthenticationError: If the user is not authenticated
    """
    pass
```

### TypeScript/JavaScript (Frontend - SvelteKit)

#### Code Style
- Use [Prettier](https://prettier.io/) for formatting
- Use [ESLint](https://eslint.org/) for linting
- Follow [Svelte best practices](https://svelte.dev/docs/svelte/overview)
- Use TypeScript for type safety

#### Component Structure (Svelte)
```svelte
<!-- ChatInterface.svelte -->
<script lang="ts">
  import { Button } from '$lib/components/common/Button.svelte';
  import type { Message } from '$lib/types/chat';
  import { sendMessage } from '$lib/services/chatService';

  // Props
  export let userId: string;
  export let onMessageSent: ((message: Message) => void) | undefined = undefined;

  // State
  let messages: Message[] = [];
  let inputText = '';
  let isLoading = false;

  async function handleSendMessage(): Promise<void> {
    if (!inputText.trim()) return;

    isLoading = true;
    try {
      const response = await sendMessage(userId, inputText);
      messages = [...messages, response];
      onMessageSent?.(response);
      inputText = '';
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="chat-interface">
  <!-- Component markup -->
  <div class="messages">
    {#each messages as message (message.id)}
      <div class="message">{message.content}</div>
    {/each}
  </div>

  <form on:submit|preventDefault={handleSendMessage}>
    <input
      bind:value={inputText}
      placeholder="Type your message..."
      disabled={isLoading}
    />
    <Button type="submit" disabled={isLoading}>
      {isLoading ? 'Sending...' : 'Send'}
    </Button>
  </form>
</div>

<style>
  .chat-interface {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .messages {
    flex: 1;
    overflow-y: auto;
  }
</style>
```

## Testing Guidelines

### Backend Testing

#### Unit Tests
```python
import pytest
from app.services.chat_service import ChatService
from app.models.user import User

class TestChatService:
    def setup_method(self):
        self.chat_service = ChatService()
        self.test_user = User(id=1, username="testuser")
    
    async def test_process_message_success(self):
        """Test successful message processing."""
        message = "Hello, PAL-adin!"
        result = await self.chat_service.process_message(message, self.test_user.id)
        
        assert result["status"] == "success"
        assert "response" in result
        assert len(result["response"]) > 0
    
    async def test_process_message_empty_input(self):
        """Test handling of empty message input."""
        with pytest.raises(ValueError, match="Message cannot be empty"):
            await self.chat_service.process_message("", self.test_user.id)
```

#### Integration Tests
```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_chat_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/chat/message",
            json={"message": "Hello", "conversation_id": 1},
            headers={"Authorization": "Bearer test_token"}
        )
    assert response.status_code == 200
    assert "response" in response.json()
```

### Frontend Testing

#### Component Tests (Svelte)
```typescript
import { render, screen, fireEvent } from '@testing-library/svelte';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import ChatInterface from '$lib/components/chat/ChatInterface.svelte';
import * as chatService from '$lib/services/chatService';

// Mock the chat service
vi.mock('$lib/services/chatService');

describe('ChatInterface', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should send message when form is submitted', async () => {
    // Setup mock
    const mockSendMessage = vi.spyOn(chatService, 'sendMessage');
    mockSendMessage.mockResolvedValue({
      id: '1',
      content: 'Hello back!',
      timestamp: new Date().toISOString(),
    });

    // Render component
    const { component } = render(ChatInterface, {
      props: { userId: 'test-user' }
    });

    // Get elements
    const input = screen.getByPlaceholderText('Type your message...');
    const sendButton = screen.getByRole('button', { name: 'Send' });

    // Simulate user input
    await fireEvent.input(input, { target: { value: 'Hello!' } });
    await fireEvent.click(sendButton);

    // Assert
    expect(mockSendMessage).toHaveBeenCalledWith('test-user', 'Hello!');
  });

  it('should disable input while sending', async () => {
    const { component } = render(ChatInterface, {
      props: { userId: 'test-user' }
    });

    const input = screen.getByPlaceholderText('Type your message...');
    const sendButton = screen.getByRole('button', { name: 'Send' });

    await fireEvent.input(input, { target: { value: 'Test' } });

    // Check initial state
    expect(input).not.toBeDisabled();

    // Note: Testing loading state requires waiting for async operation
  });
});
```

#### Integration Tests (SvelteKit)
```typescript
import { expect, test } from '@playwright/test';

test('chat interface loads and sends message', async ({ page }) => {
  await page.goto('/chat');

  // Wait for chat interface to load
  await expect(page.locator('.chat-interface')).toBeVisible();

  // Type a message
  const input = page.locator('input[placeholder="Type your message..."]');
  await input.fill('Hello, PAL-adin!');

  // Send message
  await page.click('button:has-text("Send")');

  // Verify message appears
  await expect(page.locator('.message')).toContainText('Hello, PAL-adin!');
});
```

## Documentation

### API Documentation

Use FastAPI's automatic documentation with additional details:

```python
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.message import MessageCreate, MessageResponse
from app.services.chat_service import ChatService

router = APIRouter(prefix="/api/v1/chat", tags=["chat"])

@router.post("/message", response_model=MessageResponse)
async def send_message(
    message: MessageCreate,
    user_id: int = Depends(get_current_user),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Send a message to PAL-adin and receive a response.
    
    - **message**: The message content to send
    - **conversation_id**: Optional conversation ID for context
    - **user_id**: Automatically extracted from authentication token
    
    Returns the AI response with metadata including response time and tokens used.
    """
    try:
        return await chat_service.process_message(message, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Code Comments

- Comment complex business logic
- Document API endpoints
- Explain non-obvious algorithms
- Add TODO comments for future improvements

## Pull Request Process

### Before Submitting

1. **Run all tests**
```bash
make test  # Runs both backend and frontend tests
```

2. **Check code quality**
```bash
make lint  # Runs linting and formatting
```

3. **Update documentation**
- API docs for new endpoints
- Component docs for new UI elements
- README for new features

4. **Test your changes**
- Manual testing of new features
- Edge case testing
- Performance testing if applicable

### Pull Request Template

```markdown
## Description
Brief description of changes and their purpose.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)

## Screenshots (if applicable)
Add screenshots to help explain your changes.

## Additional Notes
Any additional context or considerations.
```

### Review Process

1. **Automated Checks**
- All tests must pass
- Code coverage must not decrease
- Linting and formatting checks

2. **Code Review**
- At least one maintainer approval required
- Focus on logic, security, and performance
- Constructive feedback and suggestions

3. **Integration**
- Merge to `develop` branch
- Automated deployment to staging
- Integration testing

## Community

### Getting Help

- **GitHub Issues**: Report bugs or request features
- **GitHub Discussions**: Ask questions and share ideas
- **Documentation**: Check `/docs` directory for guides

### Recognition

- Contributors are recognized in our README and CONTRIBUTORS.md
- Top contributors get GitHub profile badges and highlights
- Annual contributor appreciation recognition in project updates

### Ways to Contribute

- **Code**: New features, bug fixes, improvements
- **Documentation**: Guides, tutorials, API docs
- **Testing**: Bug reports, test cases, performance testing
- **Design**: UI/UX improvements, graphics
- **Community**: Support, moderation, outreach

## Release Process

### Versioning

We follow [Semantic Versioning](https://semver.org/):
- `MAJOR.MINOR.PATCH`
- Breaking changes increment MAJOR
- New features increment MINOR
- Bug fixes increment PATCH

### Release Checklist

1. **Code Quality**
- [ ] All tests passing
- [ ] Code coverage targets met
- [ ] Security scan completed
- [ ] Performance benchmarks met

2. **Documentation**
- [ ] Changelog updated
- [ ] Release notes prepared
- [ ] API documentation updated
- [ ] User guides updated

3. **Deployment**
- [ ] Staging deployment successful
- [ ] Production deployment tested
- [ ] Rollback plan ready
- [ ] Monitoring configured

Thank you for contributing to PAL-adin! Your help makes this project better for everyone. 🚀