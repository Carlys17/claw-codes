# Claw Code - Qwen Edition

[![GitHub](https://img.shields.io/github/stars/Carlys17/claw-codes)](https://github.com/Carlys17/claw-codes)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**AI Coding Assistant yang bisa menggunakan Claude atau Qwen (Alibaba Cloud)** 🚀

---

## ✨ Fitur Utama

| Fitur | Deskripsi |
|-------|-----------|
| 🤖 **Multi-LLM** | Support Claude (Anthropic) dan Qwen (Alibaba Cloud) |
| 🛠️ **207 Commands** | Perintah siap pakai untuk berbagai task |
| 🔧 **184 Tools** | File ops, search, git, MCP, dan lebih banyak lagi |
| 🐍 **Python** | Mudah dimodifikasi dan extend |
| 🦀 **Rust (WIP)** | Implementasi Rust untuk performa lebih tinggi |
| 🔌 **MCP Support** | Integrasikan dengan MCP servers |

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Carlys17/claw-codes.git
cd claw-codes
```

### 2. Pilih LLM Provider

#### Pakai Qwen (Alibaba Cloud / DashScope)

```bash
# Set API key
export QWEN_API_KEY="your-dashscope-api-key"
export QWEN_MODEL="qwen-max"  # optional: qwen-turbo, qwen-plus, qwen-max
```

Dapatkan API Key di: [Alibaba Cloud DashScope](https://dashscope.console.aliyun.com/)

#### Pakai Claude (Anthropic)

```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### 3. Jalankan

```bash
# Lihat ringkasan project
python -m src.main summary

# List available commands
python -m src.main commands --limit 20

# List available tools
python -m src.main tools --limit 20

# Jalankan turn loop dengan AI
python -m src.main turn-loop "Jelaskan struktur project ini" --max-turns 3
```

---

## 📖 Dokumentasi

### Command Line Usage

```bash
# Cek provider aktif
python -m src.main summary

# Pilih provider secara eksplisit
python -m src.main turn-loop "Hello" --provider qwen
python -m src.main turn-loop "Hello" --provider claude

# Bootstrap session AI
python -m src.main bootstrap "Buatkan REST API sederhana"

# Run tests
python -m unittest discover -s tests -v
```

### Environment Variables

| Variable | Deskripsi | Default |
|----------|-----------|---------|
| `QWEN_API_KEY` | API key untuk Qwen/DashScope | - |
| `QWEN_BASE_URL` | Qwen API endpoint | `https://dashscope.aliyuncs.com/api/v1` |
| `QWEN_MODEL` | Model Qwen yang digunakan | `qwen-max` |
| `ANTHROPIC_API_KEY` | API key untuk Claude | - |
| `ANTHROPIC_BASE_URL` | Claude API endpoint | `https://api.anthropic.com` |

---

## 📦 Struktur Project

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
├── QWEN_SETUP.md                 # Panduan lengkap setup Qwen
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
python -m src.main bootstrap "Buatkan Flask REST API untuk todo app"
```

### 2. Code Review
```bash
python -m src.main turn-loop "Review file src/main.py dan suggest improvements"
```

### 3. Debugging
```bash
python -m src.main turn-loop "Kenapa test ini fail? Jelaskan dan beri fix"
```

### 4. Refactoring
```bash
python -m src.main bootstrap "Refactor fungsi ini jadi lebih clean"
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
client = QwenClient.from_env()
request = QwenRequest(messages=[QwenMessage(role='user', content='Hello')])
response = client.send_message(request)
print(f'Model: {response.model}')
print(f'Response: {response.content}')
"
```

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

---

## 📬 Contact

- **GitHub**: [@Carlys17](https://github.com/Carlys17/claw-codes)
- **Issues**: [GitHub Issues](https://github.com/Carlys17/claw-codes/issues)

---

**Star ⭐ repo ini kalau kamu merasa project ini membantu!**
