---
name: restore-context
description: Restore previous work state from memory to continue where you left off
---

# Restore Previous Context

Loads saved work state from memory and restores the session context.

## What Gets Restored

1. **Task Description** - What we were working on
2. **Progress** - Restored to TodoWrite
3. **Key Files** - Listed for quick reference
4. **Decisions** - Important choices already made
5. **Resume Instructions** - Where to continue

## Process

### 1. Check for Saved State

```bash
# Check project-level memory
ls -la .claude/memory/session-state.json 2>/dev/null

# Check user-level memory
ls -la ~/.claude/plugins/netro/memory/ 2>/dev/null
```

### 2. Load Session State

Read `.claude/memory/session-state.json` and parse.

### 3. Display Context Summary

```
📂 Restoring Context
═══════════════════════════════════════

Task: [current task description]
Started: [timestamp]
Linear: MYT-123 (if linked)
Branch: feature/MYT-123-name

Progress:
  ✅ Completed: 5 items
  🔄 In Progress: 1 item
  ⏳ Remaining: 3 items

Key Files:
  - src/auth/login.ts (modified)
  - src/types/user.ts (read)
  - src/utils/validation.ts (read)

Key Decisions:
  1. Using Zod for validation
  2. JWT tokens with 24h expiry

Resume Instructions:
  Continue implementing the validateUser function
  in src/auth/login.ts. The types are ready.

═══════════════════════════════════════
```

### 4. Restore TodoWrite

Convert saved progress to TodoWrite format:
```
- Completed items → status: completed
- In-progress item → status: in_progress
- Remaining items → status: pending
```

### 5. Offer to Read Key Files

```
Would you like me to read the key files to restore full context?
- src/auth/login.ts
- src/types/user.ts
```

## Output Format

### If State Found

```
✅ Context restored from .claude/memory/

Task: Implement user authentication
Progress: 5/9 tasks completed
Last saved: 2 hours ago

Todos restored. Key files identified.
Ready to continue with: [resume instructions]
```

### If No State Found

```
ℹ️ No saved context found

Checked:
- .claude/memory/session-state.json (not found)
- ~/.claude/plugins/netro/memory/ (empty)

This might be a fresh session. Use /save-context to save your work.
```

### If State is Old (>24h)

```
⚠️ Found old context (saved 3 days ago)

Task: Implement user authentication
Last saved: 2024-01-12T10:30:00Z

This context may be outdated. Options:
1. Restore anyway: /restore-context --force
2. Start fresh and save new context
3. Review the saved state first
```

## Usage

```
# Standard restore
/restore-context

# Force restore old state
/restore-context --force

# Show state without restoring
/restore-context --preview
```

## Integration with Linear

If Linear MCP available and issue ID in state:
1. Fetch current issue status
2. Show any new comments
3. Update if status changed

## Integration with Serena

If Serena MCP available:
1. Check serena memories for additional context
2. Load any project-specific memories
