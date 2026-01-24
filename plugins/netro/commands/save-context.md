---
name: save-context
description: Save current work state to memory for later resumption
arguments:
  - name: description
    description: Optional description of what to remember
    required: false
---

# Save Current Context

Saves the current work state to persistent memory so it can be restored later.

## What Gets Saved

1. **Current Task** - What we're working on
2. **Progress** - Completed, in-progress, and remaining items from TodoWrite
3. **Key Files** - Files that were read/modified this session
4. **Decisions** - Important choices made during this session
5. **Resume Instructions** - How to continue this work

## Process

### 1. Gather Current State

```bash
# Get current branch and any Linear issue
git branch --show-current 2>/dev/null
```

### 2. Extract Progress from TodoWrite

Read the current todo list and categorize items:
- Completed items
- In-progress items
- Pending items

### 3. Identify Key Files

Files that were:
- Read multiple times
- Modified (via Edit/Write)
- Mentioned in conversation

### 4. Generate Resume Instructions

Based on:
- Current in-progress task
- Most recent actions
- Any blockers or questions

### 5. Save to Memory Files

**Save session-state.json:**
```json
{
  "version": "1.0",
  "lastUpdated": "2024-01-15T10:30:00Z",
  "description": "[user provided or auto-generated]",
  "currentTask": {
    "description": "...",
    "startedAt": "...",
    "linearIssue": "MYT-123",
    "branch": "feature/..."
  },
  "progress": {
    "completed": [],
    "inProgress": "...",
    "remaining": []
  },
  "context": {
    "keyFiles": [],
    "keyDecisions": [],
    "blockers": []
  },
  "resumeInstructions": "..."
}
```

**Save task-context.md (human-readable):**
```markdown
# Session Context - [timestamp]

## Description
[description]

## Current Task
...

## Progress
- [x] Done items
- [ ] Remaining items

## Key Files
- file1.ts - reason
- file2.ts - reason

## Resume Instructions
...
```

### 6. Confirm Save

Output:
```
✅ Context saved to .claude/memory/

Saved:
- Task: [current task]
- Progress: X completed, Y remaining
- Key files: N files tracked
- Resume instructions included

To restore later: /restore-context
```

## Usage Examples

```
# Quick save
/save-context

# Save with description
/save-context "Finished auth types, starting validation"

# Save before taking a break
/save-context "Pausing - need to research OAuth flow"
```

## Auto-Save

This command is automatically called:
- Before context compaction
- When Stop hook detects significant progress
- Every 10 tool calls (lightweight version)
