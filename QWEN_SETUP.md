# Qwen / Alibaba Cloud Setup Guide

Panduan ini menjelaskan cara mengkonfigurasi **claw-code** untuk menggunakan **Qwen** (via Alibaba Cloud DashScope atau Coding Plan) sebagai alternatif Claude API.

---

## 📋 Prerequisites

1. **API Key** dari Alibaba Cloud (DashScope atau Coding Plan)
2. **Python 3.8+** untuk Python client
3. **Internet connection** untuk akses API

---

## 🔑 Cara Mendapatkan API Key

### Opsi 1: Alibaba Cloud Coding Plan (Recommended for Coding)

Coding Plan adalah API khusus untuk coding assistant dengan endpoint yang kompatibel dengan OpenAI dan Anthropic.

1. Kunjungi [Alibaba Cloud Coding Plan](https://modelstudio.console.alibabacloud.com/ap-southeast-1?tab=coding-plan)
2. Login atau daftar akun Alibaba Cloud
3. Aktifkan service Coding Plan
4. Buat API Key di dashboard

**Coding Plan Endpoints:**

| Mode | Endpoint | Protocol |
|------|----------|----------|
| OpenAI-compatible | `https://coding-intl.dashscope.aliyuncs.com/v1` | OpenAI API format |
| Anthropic-compatible | `https://coding-intl.dashscope.aliyuncs.com/apps/anthropic` | Anthropic API format |

### Opsi 2: DashScope (Standard Qwen API)

1. Kunjungi [Alibaba Cloud DashScope](https://dashscope.console.aliyun.com/)
2. Login atau daftar akun Alibaba Cloud
3. Buka **API Key Management**
4. Klik **Create New API Key**
5. Copy dan simpan API key Anda

---

## ⚙️ Konfigurasi Environment

### Mode Coding Plan - OpenAI Compatible

```bash
# Linux / macOS
export QWEN_API_KEY="your-api-key-here"
export QWEN_API_MODE="openai"
export QWEN_BASE_URL="https://coding-intl.dashscope.aliyuncs.com/v1"
export QWEN_MODEL="qwen-coder-plus"  # atau model coding lainnya
```

### Mode Coding Plan - Anthropic Compatible

```bash
# Linux / macOS
export QWEN_API_KEY="your-api-key-here"
export QWEN_API_MODE="anthropic"
export QWEN_BASE_URL="https://coding-intl.dashscope.aliyuncs.com/apps/anthropic"
export QWEN_MODEL="qwen-coder-plus"
```

### Mode DashScope (Standard)

```bash
# Linux / macOS
export QWEN_API_KEY="your-api-key-here"
export QWEN_API_MODE="dashscope"
export QWEN_BASE_URL="https://dashscope.aliyuncs.com/api/v1"
export QWEN_MODEL="qwen-max"
```

### Windows (PowerShell)

```powershell
$env:QWEN_API_KEY="your-api-key-here"
$env:QWEN_API_MODE="openai"
$env:QWEN_BASE_URL="https://coding-intl.dashscope.aliyuncs.com/v1"
$env:QWEN_MODEL="qwen-coder-plus"
```

### Windows (Command Prompt)

```cmd
set QWEN_API_KEY=your-api-key-here
set QWEN_API_MODE=openai
set QWEN_BASE_URL=https://coding-intl.dashscope.aliyuncs.com/v1
set QWEN_MODEL=qwen-coder-plus
```

---

## 🚀 Menjalankan dengan Qwen

### Cek Provider Aktif

```bash
cd claw-codes
python -m src.main summary
```

Output akan menampilkan **Active Provider: qwen** jika API key terdeteksi.

### Menjalankan Turn Loop dengan Qwen

```bash
# Menggunakan Qwen (otomatis jika QWEN_API_KEY set)
python -m src.main turn-loop "Jelaskan struktur project ini" --max-turns 2

# Explicit memilih provider
python -m src.main turn-loop "Hello" --provider qwen
python -m src.main turn-loop "Hello" --provider claude
```

---

## 📦 Available Models (Coding Plan)

Alibaba Cloud Coding Plan offers the latest and most powerful programming models. With its powerful Coding Agent, you can switch between models on demand.

**Your current plan supports these models:**

| Brand | Model | Capabilities |
|-------|-------|--------------|
| **Qwen** | `qwen3.5-plus` | Text Generation, Deep Thinking, Visual Understanding |
| | `qwen3-max-2026-01-23` | Text Generation, Deep Thinking |
| | `qwen3-coder-next` | Text Generation |
| | `qwen3-coder-plus` | Text Generation |
| **Zhipu** | `glm-5` | Text Generation, Deep Thinking |
| | `glm-4.7` | Text Generation, Deep Thinking |
| **Kimi** | `kimi-k2.5` | Text Generation, Deep Thinking, Visual Understanding |
| **MiniMax** | `MiniMax-M2.5` | Text Generation, Deep Thinking |

### Recommended Models for Coding

| Model | Best For |
|-------|----------|
| `qwen3-coder-plus` | Complex coding tasks, multi-file refactoring |
| `qwen3-coder-next` | Fast code completion, quick fixes |
| `qwen3.5-plus` | General purpose with visual understanding |
| `glm-5` | Alternative for complex reasoning tasks |

---

## 🔍 Troubleshooting

### Error: "Qwen API key not configured"

```bash
# Cek apakah environment variable ter-set
echo $QWEN_API_KEY  # Linux/macOS
echo %QWEN_API_KEY%  # Windows CMD
echo $env:QWEN_API_KEY  # PowerShell
```

### Error: "Connection error"

- Pastikan internet connection aktif
- Cek firewall/proxy settings
- Verify base URL benar

### Error: "Invalid API Key"

- Pastikan API key tidak ada typo
- Cek apakah API key sudah activated di dashboard
- Pastikan ada quota/credit yang cukup

---

## 💰 Pricing (DashScope)

| Model | Input (per 1K tokens) | Output (per 1K tokens) |
|-------|----------------------|----------------------|
| qwen-turbo | ~$0.0003 | ~$0.0006 |
| qwen-plus | ~$0.001 | ~$0.002 |
| qwen-max | ~$0.003 | ~$0.006 |

*Harga approximate, cek official pricing untuk update terbaru*

---

## 🧪 Testing Connection

Test koneksi ke Qwen API:

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

## 🔗 Resources

- [DashScope Documentation](https://help.aliyun.com/zh/dashscope/)
- [Qwen Model Family](https://help.aliyun.com/zh/dashscope/developer-reference/qwen)
- [Alibaba Cloud Model Studio](https://www.alibabacloud.com/en/product/model-studio)

---

## 🆚 Claude vs Qwen Comparison

| Feature | Claude (Anthropic) | Qwen (Alibaba) |
|---------|-------------------|----------------|
| Context Window | 200K tokens | Up to 256K tokens |
| Max Output | 8K tokens | 8K tokens |
| Multilingual | Excellent | Excellent (strong in Chinese) |
| Code Generation | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| API Latency | ~500ms-2s | ~300ms-1.5s |
| Pricing | $$ | $ |

---

**Happy coding with claw-code + Qwen! 🚀**
