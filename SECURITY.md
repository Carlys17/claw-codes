# Security Policy

## 🔒 Reporting a Vulnerability

We take the security of this project seriously. If you discover a security vulnerability, please report it privately.

**DO NOT** open a public issue for security vulnerabilities.

### How to Report

- **Email**: Open a security advisory on GitHub
- **GitHub**: Go to [Security tab](../../security/advisories) → "Report a vulnerability"

### What to Include

Please provide as much information as possible:

- Description of the vulnerability
- Steps to reproduce
- Affected versions
- Potential impact
- Suggested fix (if any)

### Response Time

We aim to respond to security reports within **7 days**.

---

## 🛡️ Security Best Practices for Users

### 1. API Keys & Credentials

**NEVER commit API keys or credentials to this repository!**

```bash
# ✅ DO: Use environment variables
export QWEN_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"

# ❌ DON'T: Hardcode in source files
api_key = "sk-xxxxx"  # NEVER DO THIS
```

### 2. Sensitive Files to Exclude

The following files should **NEVER** be committed:

| File/Pattern | Reason |
|--------------|--------|
| `.env` | Contains secrets |
| `*.key`, `*.pem` | Private keys |
| `credentials.json` | Authentication data |
| `config.local.json` | Local config with secrets |
| `.claude/settings.local.json` | Local Claude settings |

### 3. Verify Dependencies

Always verify third-party dependencies:

```bash
# Check for known vulnerabilities
pip audit  # For Python dependencies
cargo audit  # For Rust dependencies
```

---

## 🔐 Project Security Measures

| Measure | Status | Description |
|---------|--------|-------------|
| No hardcoded secrets | ✅ | All API keys via environment variables |
| .gitignore configured | ✅ | Sensitive files excluded |
| Dependency scanning | ⚠️ | Manual audit recommended |
| Security policy | ✅ | This document |

---

## 📋 Security Checklist for Contributors

Before submitting a PR, ensure:

- [ ] No API keys or secrets in code
- [ ] No credentials in config files
- [ ] Dependencies are from trusted sources
- [ ] No sensitive data in logs or error messages
- [ ] Code follows secure coding practices

---

## 🚨 Known Limitations

1. **Educational Project**: This is a learning/research project, not production-ready software
2. **No Warranty**: Use at your own risk
3. **API Dependencies**: Relies on external API providers (Anthropic, Alibaba Cloud)

---

## 🔗 Resources

- [GitHub Security Features](https://docs.github.com/en/code-security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://docs.python.org/3/library/security.html)

---

**Thank you for helping keep this project secure!** 🙏
