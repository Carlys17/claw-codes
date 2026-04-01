# Qwen / Alibaba Cloud Setup Guide

Panduan ini menjelaskan cara mengkonfigurasi **claw-code** untuk menggunakan **Qwen** (via Alibaba Cloud DashScope) sebagai alternatif Claude API.

---

## 📋 Prerequisites

1. **DashScope API Key** dari Alibaba Cloud
2. **Python 3.8+** untuk Python client
3. **Internet connection** untuk akses API

---

## 🔑 Cara Mendapatkan API Key

### Opsi 1: DashScope (Recommended)

1. Kunjungi [Alibaba Cloud DashScope](https://dashscope.console.aliyun.com/)
2. Login atau daftar akun Alibaba Cloud
3. Buka **API Key Management**
4. Klik **Create New API Key**
5. Copy dan simpan API key Anda

### Opsi 2: Alibaba Cloud International

1. Kunjungi [Alibaba Cloud Console](https://www.alibabacloud.com/)
2. Navigate ke **Model Studio** → **DashScope**
3. Aktifkan service DashScope
4. Buat API Key di dashboard

---

## ⚙️ Konfigurasi Environment

### Linux / macOS

```bash
# Set API key (tambahkan ke ~/.bashrc atau ~/.zshrc untuk permanent)
export QWEN_API_KEY="your-api-key-here"

# Optional: Set custom base URL (default: https://dashscope.aliyuncs.com/api/v1)
export QWEN_BASE_URL="https://dashscope.aliyuncs.com/api/v1"

# Optional: Set model (default: qwen-max)
export QWEN_MODEL="qwen-max"
```

### Windows (PowerShell)

```powershell
# Set API key (permanent via Environment Variables GUI atau tambahkan ke profile)
$env:QWEN_API_KEY="your-api-key-here"
$env:QWEN_BASE_URL="https://dashscope.aliyuncs.com/api/v1"
$env:QWEN_MODEL="qwen-max"
```

### Windows (Command Prompt)

```cmd
set QWEN_API_KEY=your-api-key-here
set QWEN_BASE_URL=https://dashscope.aliyuncs.com/api/v1
set QWEN_MODEL=qwen-max
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

## 📦 Available Qwen Models

| Model | Deskripsi | Use Case |
|-------|-----------|----------|
| `qwen-turbo` | Fastest, cheapest | Quick tasks, prototyping |
| `qwen-plus` | Balanced | General purpose |
| `qwen-max` | Most capable | Complex reasoning, coding |
| `qwen-max-longcontext` | 200K+ context | Large documents |
| `qwen2.5-72b-instruct` | Open weights | Self-hosted option |

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
