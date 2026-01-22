---
paths: ["**/*.test.ts", "**/*.spec.ts", "**/__tests__/**"]
alwaysApply: true
---

# Safe Testing Patterns

## The Problem

E2E tests and large test suites can generate 50K+ characters of output.
This can cause "prompt too long" errors that crash the session.

## Safe Patterns

### Pattern 1: Output to File

```bash
pnpm test 2>&1 | tee /tmp/test-results.log | tail -50
```

### Pattern 2: Only Show Failures

```bash
pnpm test 2>&1 | grep -A 10 "FAIL\|Error\|✗"
```

### Pattern 3: Summary Reporter

```bash
pnpm vitest --reporter=verbose --run 2>&1 | tail -30
```

### Pattern 4: Run in Background

```bash
pnpm test:e2e > /tmp/e2e.log 2>&1 &
# Later check with: tail -100 /tmp/e2e.log
```

### Pattern 5: Limit Output

```bash
pnpm test 2>&1 | head -200
```

## NEVER DO

```bash
# ❌ Raw output floods context
pnpm test:e2e
npx playwright test

# ❌ Full verbose output
pnpm vitest --reporter=verbose
```

## ALWAYS DO

```bash
# ✅ Limited output
pnpm test 2>&1 | tail -50

# ✅ Saved to file
pnpm test > /tmp/test.log 2>&1 && tail -30 /tmp/test.log

# ✅ Filtered failures
pnpm test 2>&1 | grep -E "(PASS|FAIL|Error)" | tail -50
```

## Recovery

If context is filling up:
1. Run `/compact` immediately
2. Save important state to a file
3. Consider fresh session with `/clear`

## Test Output Guidelines

| Test Type | Max Output | Command Pattern |
|-----------|-----------|-----------------|
| Unit tests | 100 lines | `pnpm test \| tail -100` |
| Integration | 50 lines | `pnpm test:int \| tail -50` |
| E2E | 30 lines | `pnpm test:e2e \| tail -30` |
| Coverage | 50 lines | `pnpm coverage \| tail -50` |
