---
name: continuous-execution
description: Enable continuous autonomous execution without stopping until tasks are complete. Integrates with memory persistence and completion enforcement.
version: 1.0.0
---

# Continuous Execution Mode

This skill enables Claude to work continuously without stopping until all tasks are complete, while still allowing pauses for user clarification.

## Operating Modes

### 1. Auto-Approve Mode (Built-in)

Claude Code has a built-in auto-approve mode:
- Press `Shift+Tab` to cycle through permission modes
- Modes: Ask → Auto-approve for session → Auto-approve always
- In auto-approve mode, Claude continues without permission prompts

### 2. Continuous Task Mode (This Skill)

When activated, Claude:
- Does NOT stop after completing individual steps
- Continues through the entire task list
- Only pauses for:
  - User questions that require input
  - Ambiguous requirements
  - Critical errors that need human decision
- Saves state regularly for recovery

## Activation

### Via Command
```
/continuous on
```

### Via Task Description
Include in your request:
- "Work continuously until done"
- "Complete all tasks without stopping"
- "Don't stop until finished"

### Via Hook Configuration
The Stop hook is configured to:
1. Check if continuous mode is active
2. Verify if tasks remain incomplete
3. Auto-continue if work remains

## Behavior Rules

### Continue Automatically When:
- TodoWrite has pending items
- Tests are failing after code changes
- Coverage target not met
- Files remain to be processed
- Linear issue still has `needs-*` labels

### Pause for User When:
- Ambiguous requirement detected
- Multiple valid approaches exist
- Destructive operation requested
- External resource access needed
- Critical decision point

### Stop Only When:
- All todos marked complete
- Verification passed (tests, lint, build)
- User explicitly says "stop" or "pause"
- Critical unrecoverable error

## Implementation

### Stop Hook Enhancement

The Stop hook checks continuous mode:

```json
{
  "Stop": [{
    "hooks": [{
      "type": "prompt",
      "prompt": "Check if continuous mode is active and work remains:\n\n1. Is continuous mode enabled? (check .claude/continuous-mode)\n2. Are there incomplete todos in TodoWrite?\n3. Are there failing tests after code changes?\n4. Are there remaining items in progress.json?\n\nIf continuous mode is ON and work remains:\n- Respond {\"ok\": false, \"reason\": \"Continuous mode: X tasks remaining\"}\n- This will auto-continue execution\n\nIf work is complete OR continuous mode is OFF:\n- Respond {\"ok\": true}",
      "timeout": 60
    }]
  }]
}
```

### State File

`.claude/continuous-mode.json`:
```json
{
  "enabled": true,
  "startedAt": "ISO-8601",
  "taskDescription": "Original task description",
  "completionCriteria": [
    "All todos complete",
    "Tests passing",
    "Coverage > 80%"
  ],
  "pauseReasons": [],
  "autoResumeAfter": ["user_response", "error_fixed"]
}
```

## Integration with Memory

Continuous mode works with memory persistence:

1. **Auto-save before each major step**
   - Progress saved to session-state.json
   - Resume instructions updated

2. **Recovery from crashes**
   - On restart, check continuous-mode.json
   - If enabled, offer to resume
   - Restore todos and continue

3. **Context compaction survival**
   - State saved before compaction
   - After compaction, restore and continue

## Usage Patterns

### Pattern 1: Full Task Completion
```
User: "Implement user auth for all apps. Work continuously."

Claude:
1. Creates comprehensive todo list
2. Starts with shared types
3. Implements shared logic
4. [Auto-continues to each app]
5. Runs tests after each app
6. [Auto-continues if tests fail - fixes]
7. Updates Linear issues
8. [Stops only when ALL apps done]
```

### Pattern 2: Test Until Pass
```
User: "Fix all failing tests. Don't stop until green."

Claude:
1. Runs tests, captures failures
2. Analyzes first failure
3. Implements fix
4. Runs tests again
5. [Auto-continues if still failing]
6. [Stops only when all green]
```

### Pattern 3: Coverage Target
```
User: "Get to 100% coverage on auth module."

Claude:
1. Runs coverage report
2. Identifies uncovered lines
3. Writes tests for first gap
4. Re-runs coverage
5. [Auto-continues if < 100%]
6. [Stops only at 100%]
```

## External Integration

### Continuous Claude (External Tool)

For true infinite execution, use the external Continuous Claude tool:
- GitHub: https://github.com/sayem314/continuous-claude
- Runs as separate process
- Auto-sends "continue" when Claude stops
- Can run overnight/unattended

Setup:
```bash
npx continuous-claude
# In another terminal:
claude --continuous
```

### CLI Loop Pattern

For custom continuous execution:
```bash
while true; do
  claude --print "Continue the task" | tee -a log.txt
  if grep -q "TASK_COMPLETE" log.txt; then
    break
  fi
  sleep 2
done
```

## Commands

### Enable Continuous Mode
```
/continuous on
```

### Disable Continuous Mode
```
/continuous off
```

### Check Status
```
/continuous status
```

### Set Completion Criteria
```
/continuous until "all tests pass and coverage > 90%"
```

## Safety Measures

1. **Max iterations**: Default 50 iterations before forced pause
2. **Time limit**: Default 2 hours before check-in
3. **Error threshold**: 3 consecutive errors triggers pause
4. **User interrupt**: Ctrl+C always works to stop

## Best Practices

1. **Clear completion criteria** - Define what "done" means upfront
2. **Granular todos** - Small tasks = visible progress
3. **Regular saves** - Memory persistence for recovery
4. **Test after changes** - Catch issues early
5. **Monitor logs** - Watch for loops or issues
