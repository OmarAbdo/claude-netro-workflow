# {{PROJECT_NAME}} - AI Agent Guide

## Overview

This is a TypeScript monorepo containing:
{{#each apps}}
- **{{name}}**: {{description}}
{{/each}}

## Repository Structure

```
/apps          - All applications
/packages      - Shared code (business logic, types)
/infrastructure - Deployment configurations
/docs          - Documentation
```

## Core Principles

### 1. Code Reuse is Mandatory

**Business logic MUST live in `packages/shared`**, not in individual apps.

```typescript
// ❌ BAD: Logic in app
// apps/mobile/hooks/use-feature.ts

// ✅ GOOD: Logic in shared package
// packages/shared/src/hooks/use-feature.ts
export { useFeature } from '@{{scope}}/shared';
```

### 2. Type Safety Across the Stack

All TypeScript types live in `packages/types`. Never duplicate.

```typescript
import type { User } from '@{{scope}}/types';
```

### 3. Design Consistency

Use design tokens for all styling. No hardcoded values.

## Development Workflow

### Starting a Cross-App Feature

```
/feature <name> <apps...>
```

This creates Linear issues and tracking for the feature.

### Code Quality

Run health checks regularly:
```
/health-check
/scan-types
/scan-quality
```

### TDD Workflow

1. Write tests first (use tdd-workflows plugin)
2. Implement to make tests pass
3. Review with code-reviewer agent
4. Create PR with git-pr-workflows

## Quick Reference

| Command | Description |
|---------|-------------|
| `/feature` | Create cross-app feature with Linear tracking |
| `/health-check` | Run comprehensive codebase scan |
| `/scan-types` | Check for type issues |
| `/init-project` | (Re)initialize workflow setup |

## What NOT to Do

❌ Duplicate business logic across apps
❌ Hardcode API URLs, colors, or spacing
❌ Create types in multiple places
❌ Commit secrets or console.logs

## What TO Do

✅ Extract shared logic to packages/shared
✅ Use semantic commit messages
✅ Write tests for business logic
✅ Run /health-check before major PRs
