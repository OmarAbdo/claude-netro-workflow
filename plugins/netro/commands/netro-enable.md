---
name: netro-enable
description: Activate all bundled plugins that are part of the Netro workflow (TDD, code review, git-pr, etc.) by modifying settings.json
arguments:
  - name: level
    description: "core, extended, or all"
    required: false
    default: all
---

# Enable Netro Plugin Bundle

This command ACTUALLY enables bundled plugins by modifying `~/.claude/settings.json`.

## REQUIRED EXECUTION STEPS

You MUST execute these steps in order:

### Step 1: Read Current Settings

```bash
cat ~/.claude/settings.json
```

Parse the JSON to identify currently enabled plugins in `enabledPlugins`.

### Step 2: Determine Plugins to Enable

Based on the `level` argument:

**Core plugins** (level: core, extended, or all):
- `tdd-workflows@claude-code-workflows`
- `comprehensive-review@claude-code-workflows`
- `git-pr-workflows@claude-code-workflows`

**Extended plugins** (level: extended or all):
- `full-stack-orchestration@claude-code-workflows`
- `error-diagnostics@claude-code-workflows`
- `security-scanning@claude-code-workflows`
- `code-refactoring@claude-code-workflows`

**Integration plugins** (level: all only):
- `linear@claude-plugins-official`
- `serena@claude-plugins-official`

### Step 3: Identify Missing Plugins

Compare the plugin list against `enabledPlugins` in settings.json.
Create a list of plugins that need to be added.

### Step 4: Modify settings.json

For each missing plugin, add it to the `enabledPlugins` object with value `true`.

Use the Edit tool to add the missing entries to `enabledPlugins` in `~/.claude/settings.json`.

Example - if `security-scanning@claude-code-workflows` is missing, add:
```json
"security-scanning@claude-code-workflows": true,
```

### Step 5: Verify Changes

Read settings.json again to confirm all requested plugins are now enabled.

### Step 6: Report Results

Display a summary:

```
Netro Plugin Bundle Enabled (level: [level])

Core Plugins:
  [status] tdd-workflows@claude-code-workflows
  [status] comprehensive-review@claude-code-workflows
  [status] git-pr-workflows@claude-code-workflows

Extended Plugins:
  [status] full-stack-orchestration@claude-code-workflows
  [status] error-diagnostics@claude-code-workflows
  [status] security-scanning@claude-code-workflows
  [status] code-refactoring@claude-code-workflows

Integrations:
  [status] linear@claude-plugins-official
  [status] serena@claude-plugins-official

[status] = "already enabled" or "enabled now" or "skipped (not in level)"

IMPORTANT: Restart Claude Code to load newly enabled plugins.
```

## Plugin Descriptions

### Core: tdd-workflows
- TDD orchestration (red-green-refactor)
- Test-first development enforcement
- Coverage tracking

### Core: comprehensive-review
- Multi-agent code review
- Security, performance, architecture review
- Automated quality checks

### Core: git-pr-workflows
- PR creation and management
- Conventional commits
- Branch management

### Extended: full-stack-orchestration
- Deployment engineering
- Performance optimization
- Security auditing
- Test automation

### Extended: error-diagnostics
- Debugging specialist
- Error pattern detection
- Root cause analysis

### Extended: security-scanning
- SAST (Static Analysis)
- Threat modeling
- Vulnerability detection

### Extended: code-refactoring
- Legacy modernization
- Technical debt reduction
- Code quality improvement

### Integration: linear
- Issue tracking
- Cross-app feature management
- Label-based workflow

### Integration: serena
- Semantic code analysis
- Symbol navigation
- Type analysis
