---
name: memory-persistence
description: Persist work state, context, and progress across context windows and sessions. Auto-activates to save and restore work state.
version: 1.0.0
---

# Memory Persistence System

This skill enables Claude to maintain context and progress across:
- Context window compactions
- Session restarts
- Multi-session work on complex tasks

## Memory Locations

### Project-Level Memory
```
<project>/.claude/
├── memory/
│   ├── session-state.json    # Current session state
│   ├── task-context.md       # Human-readable task context
│   └── decisions.md          # Architectural decisions made
├── progress.json             # Task progress tracking
└── CLAUDE.local.md           # Session notes (gitignored)
```

### User-Level Memory
```
~/.claude/plugins/netro/memory/
├── cross-project.json        # State shared across projects
└── learned-patterns.md       # Patterns learned from user
```

## Session State Structure

### session-state.json
```json
{
  "version": "1.0",
  "lastUpdated": "ISO-8601",
  "currentTask": {
    "description": "What we're working on",
    "startedAt": "ISO-8601",
    "linearIssue": "MYT-123",
    "branch": "feature/MYT-123-task-name"
  },
  "progress": {
    "completed": ["task 1", "task 2"],
    "inProgress": "current task",
    "remaining": ["task 3", "task 4"]
  },
  "context": {
    "keyFiles": ["src/auth.ts", "src/types.ts"],
    "keyDecisions": ["Using Zod for validation", "JWT for auth"],
    "blockers": []
  },
  "resumeInstructions": "Continue with implementing the login endpoint..."
}
```

### task-context.md
```markdown
# Current Task Context

## Task
[Description of what we're working on]

## Progress
- [x] Completed item 1
- [x] Completed item 2
- [ ] In progress: current item
- [ ] Remaining item

## Key Decisions
1. Decision 1 and rationale
2. Decision 2 and rationale

## Important Files
- `src/auth.ts` - Main auth logic
- `src/types.ts` - Type definitions

## Resume Instructions
When resuming, start by...
```

## Auto-Save Triggers

Memory is automatically saved:
1. **Before context compaction** (PreCompact hook)
2. **Before session end** (Stop hook)
3. **After completing major tasks** (PostToolUse for Write/Edit)
4. **Periodically** (every 10 tool calls)

## Auto-Load Triggers

Memory is automatically loaded:
1. **Session start** (SessionStart hook)
2. **After context compaction** (first tool call after)
3. **Manual restore** (`/restore-context` command)

## Commands

### Save Current State
```
/save-context [description]
```
Manually saves current work state with optional description.

### Restore Previous State
```
/restore-context
```
Loads the most recent saved state and displays context.

### Show Memory Status
```
/memory-status
```
Shows what's currently persisted and when.

## Implementation

### Saving State (call before compaction/stop)

```python
# Save to project memory
state = {
    "lastUpdated": datetime.now().isoformat(),
    "currentTask": extract_current_task(),
    "progress": get_todo_state(),
    "context": gather_context(),
    "resumeInstructions": generate_resume_instructions()
}
save_to_file(".claude/memory/session-state.json", state)

# Also save human-readable version
save_task_context_md(".claude/memory/task-context.md")
```

### Loading State (call on session start)

```python
# Check for existing state
if exists(".claude/memory/session-state.json"):
    state = load_json(".claude/memory/session-state.json")

    # Restore context
    print(f"Resuming task: {state['currentTask']['description']}")
    print(f"Progress: {len(state['progress']['completed'])} done, {len(state['progress']['remaining'])} remaining")
    print(f"Resume: {state['resumeInstructions']}")

    # Restore todos
    restore_todos(state['progress'])
```

## Integration with Serena

If Serena MCP is available, use its memory tools:
```
serena.write_memory({
    memory_file_name: "session-state.md",
    content: formatted_state
})

serena.read_memory({
    memory_file_name: "session-state.md"
})
```

## Best Practices

1. **Always save before stopping** - Even for small tasks
2. **Include resume instructions** - Be specific about next steps
3. **Track key files** - So you know what to read on resume
4. **Document decisions** - Rationale may be lost otherwise
5. **Use Linear issues** - They persist even if memory fails

## Example Workflow

### Starting Work
```
SessionStart: Load .claude/memory/session-state.json
→ Display: "Resuming: Implement user auth. 3/7 tasks done."
→ Restore todos from progress
→ Read key files listed in context
```

### During Work
```
Every 10 tool calls: Auto-save state
After completing task: Update progress, save
Before compaction: Full state save with instructions
```

### Ending Work
```
Stop hook: Save final state
→ Generate resume instructions
→ List remaining tasks
→ Note any blockers
```

### Resuming Later
```
/restore-context
→ Read session-state.json
→ Display task context
→ Restore todo list
→ Ready to continue
```
