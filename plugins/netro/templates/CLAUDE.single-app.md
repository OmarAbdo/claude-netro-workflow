# {{PROJECT_NAME}} - AI Agent Guide

## Overview

This is a single TypeScript application.

**Stack:** {{stack}}

## Project Structure

```
/src           - Application source code
/tests         - Test files
/public        - Static assets (if applicable)
```

## Development Standards

### Code Quality Rules

1. **No `any` types** - use `unknown` with type guards
2. **Files under 500 lines** - split large files
3. **Functions under 50 lines** - extract helpers
4. **No console.log** - use proper logging

### Testing Requirements

- Unit tests for business logic
- Integration tests for API routes
- E2E tests for critical flows

### Code Style

- ESLint + Prettier enforced
- Conventional commits (feat:, fix:, etc.)
- Semantic variable names

## Development Workflow

### Writing Code

1. **Write tests first** (TDD)
2. **Implement feature**
3. **Run quality checks**
4. **Create PR**

### Quality Commands

```
/health-check    # Full codebase scan
/scan-quality    # Code quality issues
/scan-types      # Type consistency
```

## Quick Reference

| What | Where |
|------|-------|
| Types | `src/types/` |
| Utils | `src/utils/` |
| Tests | `tests/` or `__tests__/` |

## Commit Message Format

```
type(scope): description

Types: feat, fix, docs, style, refactor, test, chore
```

## What NOT to Do

❌ Use `any` types
❌ Write files > 500 lines
❌ Skip tests for business logic
❌ Commit console.logs

## What TO Do

✅ Run /health-check regularly
✅ Write tests first
✅ Use meaningful names
✅ Handle errors properly
