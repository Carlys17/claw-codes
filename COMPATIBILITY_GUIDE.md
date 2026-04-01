# Claude Code Compatibility Reference

This document lists the **public interface** of Claude Code for compatibility reference.
Used to guide the Python/Rust reimplementation effort.

**Note:** This is a clean-room compatibility guide. No source code is copied.

---

## 📋 Command Reference

These are public command names and their intended functionality.

### Core Commands

| Command | Description | Status |
|---------|-------------|--------|
| `/help` | Show help information | ✅ Ported |
| `/compact` | Compact conversation history | ✅ Ported |
| `/config` | Manage configuration | ✅ Ported |
| `/cost` | Show token/cost usage | ✅ Ported |
| `/clear` | Clear current session | ✅ Ported |
| `/exit` | Exit the application | ✅ Ported |
| `/login` | Authenticate | ✅ Ported |
| `/logout` | Clear authentication | ✅ Ported |

### Code Commands

| Command | Description | Status |
|---------|-------------|--------|
| `/commit` | Create git commit | ✅ Ported |
| `/diff` | Show file differences | ✅ Ported |
| `/copy` | Copy code to clipboard | ⏳ Planned |
| `/rename` | Rename files | ⏳ Planned |

### AI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `/review` | Code review | ✅ Ported |
| `/autofix-pr` | Auto-fix pull request | ⏳ Planned |
| `/security-review` | Security audit | ⏳ Planned |
| `/bughunter` | Bug detection | ⏳ Planned |

### Session Commands

| Command | Description | Status |
|---------|-------------|--------|
| `/session` | Manage sessions | ✅ Ported |
| `/resume` | Resume previous session | ✅ Ported |
| `/share` | Share session | ⏳ Planned |
| `/export` | Export conversation | ⏳ Planned |

### Tool Commands

| Command | Description | Status |
|---------|-------------|--------|
| `/mcp` | MCP server management | ✅ Ported |
| `/tasks` | Task management | ✅ Ported |
| `/memory` | Memory management | ✅ Ported |
| `/skills` | Skill management | ✅ Ported |

### UI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `/theme` | Change color theme | ⏳ Planned |
| `/keybindings` | Configure shortcuts | ⏳ Planned |
| `/ide` | IDE integration | ⏳ Planned |
| `/desktop` | Desktop app mode | ⏳ Planned |
| `/mobile` | Mobile mode | ⏳ Planned |

### Network Commands

| Command | Description | Status |
|---------|-------------|--------|
| `/teleport` | Remote execution | ✅ Ported |
| `/remote` | Remote control | ✅ Ported |
| `/install-github-app` | Install GitHub integration | ⏳ Planned |
| `/install-slack-app` | Install Slack integration | ⏳ Planned |

### Info Commands

| Command | Description | Status |
|---------|-------------|--------|
| `/status` | Show status | ✅ Ported |
| `/usage` | Usage statistics | ✅ Ported |
| `/doctor` | Diagnostic check | ✅ Ported |
| `/version` | Show version | ⏳ Planned |
| `/release-notes` | Show changelog | ⏳ Planned |

### Other Commands

| Command | Description | Status |
|---------|-------------|--------|
| `/btw` | Quick question mode | ⏳ Planned |
| `/good-claude` | Toggle assistant mode | ⏳ Planned |
| `/feedback` | Submit feedback | ⏳ Planned |
| `/onboarding` | First-time setup | ⏳ Planned |
| `/init` | Initialize project | ✅ Ported |
| `/vim` | Vim mode toggle | ⏳ Planned |
| `/voice` | Voice mode | ⏳ Planned |

---

## 🔧 Tool Reference

Public tool names for compatibility.

### File Tools

| Tool | Description | Status |
|------|-------------|--------|
| `Read` | Read file contents | ✅ Ported |
| `Edit` | Edit file | ✅ Ported |
| `Write` | Write file | ✅ Ported |
| `Bash` | Run shell commands | ✅ Ported |
| `Glob` | Find files by pattern | ✅ Ported |
| `Grep` | Search file contents | ✅ Ported |

### Git Tools

| Tool | Description | Status |
|------|-------------|--------|
| `git` | Git operations | ⏳ Planned |
| `commit` | Create commits | ⏳ Planned |
| `push` | Push to remote | ⏳ Planned |
| `pr` | Pull request ops | ⏳ Planned |

### Agent Tools

| Tool | Description | Status |
|------|-------------|--------|
| `AgentTool` | Spawn sub-agent | ✅ Ported |
| `generalPurposeAgent` | General agent | ✅ Ported |
| `exploreAgent` | Exploration agent | ✅ Ported |
| `claudeCodeGuideAgent` | Help agent | ✅ Ported |

### Web Tools

| Tool | Description | Status |
|------|-------------|--------|
| `WebFetch` | Fetch URL content | ⏳ Planned |
| `WebSearch` | Web search | ⏳ Planned |

---

## 🏷️ Feature Flags

Runtime feature toggles for conditional functionality.

| Flag | Description |
|------|-------------|
| `PROACTIVE` | Proactive suggestions |
| `KAIROS` | Kairos mode features |
| `KAIROS_BRIEF` | Brief mode |
| `VOICE_MODE` | Voice interaction |
| `HISTORY_SNIP` | History snippets |
| `WORKFLOW_SCRIPTS` | Custom workflows |
| `DAEMON` | Background daemon |
| `BRIDGE_MODE` | Bridge connectivity |
| `EXPERIMENTAL_SKILL_SEARCH` | Skill search beta |
| `CCR_REMOTE_SETUP` | Remote setup |

---

## 📊 Compatibility Status

| Category | Total | Ported | Planned | Coverage |
|----------|-------|--------|---------|----------|
| Commands | 50+ | 25 | 25 | ~50% |
| Tools | 30+ | 15 | 15 | ~50% |
| Feature Flags | 10 | 0 | 10 | Future |

---

## 📝 Notes

1. **This is a reference document only** - no implementation code is copied
2. Command names and interfaces are functional specifications, not creative works
3. Implementation should be original and clean-room
4. Status should be updated as porting progresses

---

## 🔗 Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude-code/)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Anthropic API Docs](https://docs.anthropic.com/)
