# Claw Code - Qwen Edition

[![GitHub](https://img.shields.io/github/stars/Carlys17/claw-codes)](https://github.com/Carlys17/claw-codes)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Security](https://img.shields.io/badge/security-policy-green.svg)](SECURITY.md)

**AI Coding Assistant that supports both Claude and Qwen (Alibaba Cloud)** 🚀

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **Multi-LLM** | Support Claude (Anthropic) and Qwen (Alibaba Cloud) |
| 🛠️ **207 Commands** | Ready-to-use commands for various tasks |
| 🔧 **184 Tools** | File ops, search, git, MCP, and more |
| 🐍 **Python** | Easy to modify and extend |
| 🦀 **Rust (WIP)** | Rust implementation for higher performance |
| 🔌 **MCP Support** | Integrate with MCP servers |

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Carlys17/claw-codes.git
cd claw-codes
```

### 2. Choose LLM Provider

#### Using Qwen (Alibaba Cloud / DashScope)

```bash
# Set API key
export QWEN_API_KEY="your-dashscope-api-key"
export QWEN_MODEL="qwen-max"  # optional: qwen-turbo, qwen-plus, qwen-max
```

Get API Key at: [Alibaba Cloud DashScope](https://dashscope.console.aliyun.com/)

#### Using Claude (Anthropic)

```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### 3. Run

```bash
# View project summary
python -m src.main summary

# List available commands
python -m src.main commands --limit 20

# List available tools
python -m src.main tools --limit 20

# Run turn loop with AI
python -m src.main turn-loop "Explain this project structure" --max-turns 3
```

---

## 📖 Documentation

### Command Line Usage

```bash
# Check active provider
python -m src.main summary

# Choose provider explicitly
python -m src.main turn-loop "Hello" --provider qwen
python -m src.main turn-loop "Hello" --provider claude

# Bootstrap AI session
python -m src.main bootstrap "Create a simple REST API"

# Run tests
python -m unittest discover -s tests -v
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `QWEN_API_KEY` | API key for Qwen/DashScope | - |
| `QWEN_BASE_URL` | Qwen API endpoint | Auto-detect |
| `QWEN_MODEL` | Qwen model to use | `qwen-max` |
| `QWEN_API_MODE` | API mode: `dashscope`, `openai`, `anthropic` | Auto-detect |
| `ANTHROPIC_API_KEY` | API key for Claude | - |
| `ANTHROPIC_BASE_URL` | Claude API endpoint | `https://api.anthropic.com` |

---

## 📦 Project Structure

```
claw-codes/
├── src/                          # Python source code
│   ├── qwen_client.py           # Qwen API client
│   ├── query_engine.py          # Multi-provider query engine
│   ├── main.py                  # CLI entrypoint
│   ├── models.py                # Data structures
│   ├── tools.py                 # Tool definitions
│   ├── commands.py              # Command handlers
│   ├── runtime.py               # Runtime logic
│   └── ...
├── rust/                         # Rust implementation (WIP)
│   ├── crates/
│   │   ├── api/                 # API client
│   │   ├── runtime/             # Core runtime
│   │   └── rusty-claude-cli/    # CLI application
│   └── ...
├── tests/                        # Python tests
├── QWEN_SETUP.md                 # Complete Qwen setup guide
├── SECURITY.md                   # Security policy
├── LICENSE                       # MIT License
└── README.md
```

---

## 🔧 Available Models

### Qwen Models (via DashScope)

| Model | Context | Best For |
|-------|---------|----------|
| `qwen-turbo` | 8K | Fast tasks, prototyping |
| `qwen-plus` | 32K | Balanced performance |
| `qwen-max` | 32K | Complex reasoning, coding |
| `qwen-max-longcontext` | 256K | Large documents |

### Claude Models

| Model | Context | Best For |
|-------|---------|----------|
| `claude-3-haiku` | 200K | Fast, cheap tasks |
| `claude-3-sonnet` | 200K | Balanced |
| `claude-3-opus` | 200K | Complex tasks |

---

## 🎯 Use Cases

### 1. Code Generation
```bash
python -m src.main bootstrap "Create a Flask REST API for todo app"
```

### 2. Code Review
```bash
python -m src.main turn-loop "Review src/main.py and suggest improvements"
```

### 3. Debugging
```bash
python -m src.main turn-loop "Why is this test failing? Explain and provide fix"
```

### 4. Refactoring
```bash
python -m src.main bootstrap "Refactor this function to be cleaner"
```

---

## 🧪 Development

### Run Tests
```bash
python -m unittest discover -s tests -v
```

### Test Qwen Connection
```bash
python -c "
from src.qwen_client import QwenClient, QwenRequest, QwenMessage

try:
    client = QwenClient.from_env()
    request = QwenRequest(messages=[QwenMessage(role='user', content='Hello')])
    response = client.send_message(request)
    print(f'Connected! Model: {response.model}')
    print(f'Response: {response.content}')
except Exception as e:
    print(f'Error: {e}')
"
```

---

## 🔐 Security

### ⚠️ Important: Never Commit API Keys!

```bash
# ✅ DO: Use environment variables
export QWEN_API_KEY="your-key-here"

# ❌ DON'T: Hardcode in source files
api_key = "sk-xxxxx"  # NEVER DO THIS
```

### Sensitive Files to Exclude

The following should **NEVER** be committed:

| File/Pattern | Reason |
|--------------|--------|
| `.env` | Contains secrets |
| `*.key`, `*.pem` | Private keys |
| `credentials.json` | Authentication data |
| `.claude/settings.local.json` | Local settings |

See [SECURITY.md](SECURITY.md) for full security policy.

---

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Credits

- Original concept inspired by [Claude Code](https://claude.ai/code) by Anthropic
- Qwen integration by [@Carlys17](https://github.com/Carlys17)
- Built with help from [oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Before Submitting PR

- [ ] No API keys or secrets in code
- [ ] Code follows project style
- [ ] Tests pass (`python -m unittest discover -s tests -v`)
- [ ] Documentation updated

---

## 📬 Contact

- **GitHub**: [@Carlys17](https://github.com/Carlys17/claw-codes)
- **Issues**: [GitHub Issues](https://github.com/Carlys17/claw-codes/issues)
- **Security**: [Security Advisories](../../security/advisories)

---

**Star ⭐ this repo if you find it helpful!**
