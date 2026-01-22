---
name: continuous
description: Enable or disable continuous execution mode - Claude works until all tasks complete without stopping
arguments:
  - name: action
    description: "on, off, or status"
    required: true
---

# Continuous Execution Mode

Control whether Claude continues working automatically until all tasks are complete.

## Usage

```
/continuous on       # Enable continuous mode
/continuous off      # Disable continuous mode
/continuous status   # Check current status
```

## What Happens When Enabled

1. **Claude does not stop** after completing individual tasks
2. **Auto-continues** through the entire todo list
3. **Saves state** regularly for crash recovery
4. **Only pauses** for:
   - Questions requiring user input
   - Ambiguous requirements
   - Critical errors

## Process

### /continuous on

1. Create `.claude/continuous-mode.json`:
```json
{
  "enabled": true,
  "startedAt": "[timestamp]",
  "maxIterations": 50,
  "timeoutHours": 2
}
```

2. Inform user:
```
✅ Continuous mode ENABLED

Claude will now work continuously until:
- All todos are complete
- Tests pass (if applicable)
- You say "stop" or "pause"

Safety limits:
- Max 50 iterations
- 2 hour timeout
- Pauses for questions

To disable: /continuous off
```

### /continuous off

1. Remove or update `.claude/continuous-mode.json`
2. Inform user:
```
⏸️ Continuous mode DISABLED

Claude will now stop after completing each major step
and wait for your next instruction.
```

### /continuous status

Check and display:
```
📊 Continuous Mode Status

Enabled: Yes/No
Started: [timestamp] (X hours ago)
Iterations: Y/50
Tasks completed: Z

Current task: [description]
Remaining: N items

To change: /continuous on|off
```

## Integration with Stop Hook

When continuous mode is on, the Stop hook:
1. Checks `.claude/continuous-mode.json`
2. Checks if todos remain incomplete
3. Returns `{"ok": false}` to continue working
4. Only returns `{"ok": true}` when truly done

## Safety Features

- **Iteration limit**: Stops after 50 iterations for review
- **Time limit**: Pauses after 2 hours for check-in
- **Error limit**: 3 consecutive errors trigger pause
- **Always interruptible**: Ctrl+C stops immediately

## When to Use

**Good for:**
- Multi-file refactoring
- Achieving test coverage targets
- Processing many similar items
- Implementing cross-app features
- Bug fixing until tests pass

**Not recommended for:**
- Exploratory tasks
- Learning/research tasks
- Tasks needing frequent feedback
- Sensitive operations
