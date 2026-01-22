---
paths: ["**/*"]
alwaysApply: true
---

# Completion Requirements (Universal)

## Context Window & Persistence

Your context window will be automatically compacted as it approaches its limit. This is NORMAL. Therefore:

- NEVER stop tasks early due to token budget concerns
- NEVER assume you can't complete a large task
- ALWAYS continue working until ALL requirements are met
- The system handles context management - you focus on completion

## What "Complete" Actually Means

When asked for absolute requirements:
- "100% test coverage" → Run coverage report, verify numbers = 100%
- "ALL types" → List all source files, verify each processed
- "ALL files" → Use glob to list files, process each, verify count
- "Full test suite" → Every function has tests, all pass

**Verification is MANDATORY**:
1. Run the verification command (test, coverage, lint)
2. Check the actual output numbers
3. Only claim complete when numbers match requirement
4. If partial, state what remains and continue

## Task Tracking Protocol

For any multi-step task:
1. Use TodoWrite to create granular tasks BEFORE starting
2. Update TodoWrite as each completes
3. NEVER mark parent complete until ALL sub-tasks done
4. Add verification tasks: "Verify X with Y command"

## Anti-Patterns (NEVER DO)

- "I've added tests for the main functions" (which ones?)
- "Coverage should now be higher" (what number?)
- "I've processed the important files" (all were requested)
- "The task is essentially complete" (essentially ≠ complete)

## Required Patterns (ALWAYS DO)

- "Coverage is now 87% (was 62%). Remaining: auth.ts (12 lines)"
- "Processed 47/52 files. Remaining: [list]"
- "All 23 tests passing. Coverage: 94%"
- Continue working without being asked
