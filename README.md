# Netro - Universal Claude Code Workflow Orchestrator

[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-blueviolet)](https://github.com/OmarAbdo/claude-netro-workflow)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive Claude Code plugin that provides:
- **Memory Persistence**: Survive context compaction and session restarts
- **Continuous Execution**: Work until done without stopping
- **Completion Enforcement**: Strict verification that tasks are 100% complete
- **Plugin Bundling**: Unified access to TDD, code review, and git workflow plugins
- **Codebase Health**: Comprehensive scanning for types, quality, and features

## Installation

### From Marketplace (Recommended)

```bash
# Add the marketplace
claude plugin:add-marketplace OmarAbdo/claude-netro-workflow

# Install netro
claude plugin:install netro@netro-marketplace

# Enable in settings
claude config:set enabledPlugins.netro@netro-marketplace true
```

Or via `/plugin` commands in Claude:
```
/plugin:add-marketplace OmarAbdo/claude-netro-workflow
/plugin:install netro@netro-marketplace
```

### Manual Installation

If marketplace installation doesn't work, follow these steps:

1. Add marketplace to `~/.claude/plugins/known_marketplaces.json`:
```json
{
  "netro-marketplace": {
    "source": {
      "source": "github",
      "repo": "OmarAbdo/claude-netro-workflow"
    },
    "installLocation": "~/.claude/plugins/marketplaces/netro-marketplace",
    "lastUpdated": "2026-01-24T12:00:00.000Z"
  }
}
```

2. Clone to marketplaces directory:
```bash
git clone https://github.com/OmarAbdo/claude-netro-workflow.git ~/.claude/plugins/marketplaces/netro-marketplace
```

3. Copy to cache:
```bash
mkdir -p ~/.claude/plugins/cache/netro-marketplace/netro/1.0.0
cp -r ~/.claude/plugins/marketplaces/netro-marketplace/plugins/netro/* ~/.claude/plugins/cache/netro-marketplace/netro/1.0.0/
```

4. Add to `~/.claude/plugins/installed_plugins.json`:
```json
{
  "netro@netro-marketplace": [{
    "scope": "user",
    "installPath": "~/.claude/plugins/cache/netro-marketplace/netro/1.0.0",
    "version": "1.0.0",
    "installedAt": "2026-01-24T12:00:00.000Z",
    "lastUpdated": "2026-01-24T12:00:00.000Z"
  }]
}
```

5. Enable in `~/.claude/settings.json`:
```json
{
  "enabledPlugins": {
    "netro@netro-marketplace": true
  }
}
```

6. Restart Claude Code

## Key Features

### 1. Memory Persistence

Survive context windows and session restarts:

```
/save-context          # Save current work state
/restore-context       # Restore previous state
```

**What's persisted:**
- Current task description
- Progress (completed/remaining todos)
- Key files read/modified
- Decisions made
- Resume instructions

**Auto-save triggers:**
- Before context compaction (PreCompact hook)
- Before session end (Stop hook)
- After major task completion

### 2. Continuous Execution

Work until tasks are complete without stopping:

```
/continuous on         # Enable continuous mode
/continuous off        # Disable
/continuous status     # Check current status
```

**When enabled, Claude:**
- Does NOT stop after individual tasks
- Auto-continues through the todo list
- Only pauses for user questions or critical errors
- Saves state regularly for crash recovery

### 3. Plugin Bundling

Netro bundles and coordinates these plugins:

```
/netro-enable [level]  # Activate bundled plugins
```

**Core Plugins (TDD, Review, Git):**
- `tdd-workflows` - Test-driven development
- `comprehensive-review` - Multi-agent code review
- `git-pr-workflows` - PR creation and management

**Extended Plugins:**
- `full-stack-orchestration` - Deployment, performance, security
- `error-diagnostics` - Debugging and error analysis
- `security-scanning` - SAST and vulnerability detection
- `code-refactoring` - Legacy modernization

**Integrations:**
- `linear` - Issue tracking
- `serena` - Semantic code analysis

### 4. Completion Enforcement

Strict hooks that verify work is done:

- **Stop Hook**: Blocks early stops, requires verification
- **TodoWrite Hook**: Ensures granular, actionable todos
- **PreCompact Hook**: Saves state before context compaction

## Commands

| Command | Description |
|---------|-------------|
| `/init-project` | Initialize project with Netro workflow |
| `/feature <name> <apps>` | Create cross-app feature with Linear |
| `/continuous on/off` | Toggle continuous execution |
| `/save-context` | Save current work state |
| `/restore-context` | Restore previous state |
| `/netro-enable` | Activate all bundled plugins |

## Skills

| Skill | Description |
|-------|-------------|
| `/health-check` | Full codebase health scan |
| `/scan-types` | Type consistency analysis |
| `/scan-features` | Feature alignment detection |
| `/scan-quality` | Code quality issues |

## Agents

- **code-reviewer**: Proactive code review for quality, security, performance
- **health-check**: Orchestrates comprehensive codebase scans

## Hooks

| Hook | Purpose |
|------|---------|
| SessionStart | Restore memory, detect Linear issues, check continuous mode |
| Stop | Save memory, check continuous mode, verify completion |
| PreCompact | Save state before context compaction |
| PreToolUse (TodoWrite) | Ensure granular task tracking |
| PostToolUse (Bash) | Capture large outputs to files |

## Rules

Universal rules included:
- `completion-requirements.md` - What "100%" and "ALL" mean
- `code-quality.md` - Type safety, file sizes, patterns
- `monorepo-architecture.md` - Package boundaries, imports
- `safe-testing.md` - Patterns to prevent context overflow

## Directory Structure

```
netro/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest with bundled plugins
├── commands/
│   ├── init-project.md          # /init-project
│   ├── feature.md               # /feature
│   ├── continuous.md            # /continuous
│   ├── save-context.md          # /save-context
│   ├── restore-context.md       # /restore-context
│   └── netro-enable.md          # /netro-enable
├── agents/
│   ├── code-reviewer.md
│   └── health-check.md
├── skills/
│   ├── health-check/
│   ├── scan-types/
│   ├── scan-features/
│   ├── scan-quality/
│   ├── feature-workflow/
│   ├── memory-persistence/
│   └── continuous-execution/
├── hooks/
│   ├── hooks.json
│   └── scripts/
│       └── capture-large-output.py
├── rules/
│   ├── completion-requirements.md
│   ├── code-quality.md
│   ├── monorepo-architecture.md
│   └── safe-testing.md
├── templates/
│   ├── CLAUDE.monorepo.md
│   ├── CLAUDE.single-app.md
│   └── progress.json
├── memory/                       # Plugin-level memory storage
├── .mcp.json
└── README.md
```

## Quick Start

### 1. Enable Plugin and Bundle

```bash
# In settings.json, add:
"netro": true
```

Then in Claude:
```
/netro-enable all
```

### 2. Initialize a Project

```
cd /path/to/project
claude
> /init-project
```

### 3. Start Working Continuously

```
> /continuous on
> Implement user authentication for all apps
```

### 4. Resume After Break

```
> /restore-context
```

## Workflow Examples

### Example 1: Cross-App Feature

```
> /feature user-auth mobile web server
> /continuous on

# Claude will:
# 1. Create Linear issues for tracking
# 2. Implement shared types first
# 3. Add shared logic
# 4. Implement in each app
# 5. Run tests after each step
# 6. Update Linear labels as apps complete
# 7. Stop only when all apps done
```

### Example 2: Codebase Audit

```
> /health-check
> Fix all critical issues found

# Claude will:
# 1. Scan for all issues
# 2. Create todos for each fix
# 3. Work through fixes continuously
# 4. Re-run health check to verify
```

### Example 3: Long Task Recovery

```
# Session 1
> Refactor the payment module
> /save-context "Finished types, starting logic"

# Session 2 (later)
> /restore-context
# Claude resumes from where you left off
```

## Environment Variables

```json
{
  "env": {
    "BASH_MAX_OUTPUT_LENGTH": "4000",
    "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": "70",
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "20000",
    "BASH_DEFAULT_TIMEOUT_MS": "180000"
  }
}
```

## MCP Servers

**Required:**
- `linear` - Issue tracking for /feature command

**Recommended:**
- `serena` - Semantic code analysis (enhances /scan-types)

## Troubleshooting

### Plugin not loading
1. Check settings.json has `"netro": true`
2. Restart Claude Code
3. Run `/netro-enable` to verify bundled plugins

### Memory not restoring
1. Check `.claude/memory/` directory exists
2. Run `/restore-context` manually
3. Check session-state.json for errors

### Continuous mode not working
1. Verify `.claude/continuous-mode.json` exists
2. Check Stop hook is enabled
3. Ensure todos are properly set

### Context overflow
1. Use safe testing patterns (pipe to `tail`)
2. Check `~/.claude/output-logs/` for captured outputs
3. Run `/compact` if context is filling

## License

MIT
