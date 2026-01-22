---
name: feature
description: Create a cross-app feature with Linear tracking - creates parent issue, sub-issues per app, and git branch
arguments:
  - name: feature-name
    description: Kebab-case feature name (e.g., user-auth, dark-mode)
    required: true
  - name: apps
    description: Space-separated list of apps (mobile, web, admin, server)
    required: true
---

# Create Cross-App Feature

Creates a tracked feature across multiple apps with Linear integration.

## Usage

```
/feature <feature-name> <apps...>
```

**Examples:**
```
/feature user-auth mobile web server
/feature dark-mode mobile web
/feature payment-webhooks server admin
```

## Process

### 1. Validate Arguments

- Feature name must be kebab-case
- Apps must be valid: mobile, web, admin, server
- At least one app required

### 2. Create Linear Issues (if MCP available)

**Parent Issue:**
```
Title: [Feature] <feature-name>
Team: Mytestenvironment (or configured team)
Labels: cross-app
Description: Feature template (see below)
```

**Sub-Issues (one per app):**
```
Title: [<app>] <feature-name>
Team: Same as parent
Labels: needs-<app>
Parent: Link to parent issue
```

### 3. Generate Feature Template

```markdown
## Feature: <feature-name>

### Implementation Status
| App | Status | Issue | PR |
|-----|--------|-------|-----|
| mobile | needs-mobile | MYT-X | - |
| web | needs-web | MYT-Y | - |
| server | needs-server | MYT-Z | - |

### Shared Code Checklist
- [ ] Types defined in packages/types
- [ ] Business logic in packages/shared
- [ ] Design tokens used (no hardcoded colors)
- [ ] Tests written for shared code

### Requirements
[Fill in feature requirements]

### Technical Notes
[Add implementation notes]
```

### 4. Create Git Branch

```bash
git checkout -b feature/<parent-issue-id>-<feature-name>
```

### 5. Output Summary

Display:
- Parent issue ID and URL
- Sub-issue IDs with URLs
- Git branch name
- Next steps checklist

## Label Workflow

| Stage | Action |
|-------|--------|
| Created | All apps have `needs-<app>` |
| In Progress | Issue state changes |
| App Complete | Change `needs-<app>` to `done-<app>` |
| All Complete | Close parent issue |

## Fallback (No Linear)

If Linear MCP is not connected, output manual instructions:

```
## Manual Feature Setup

1. Create parent issue in Linear:
   Title: [Feature] <feature-name>
   Labels: cross-app

2. Create sub-issues:
   - [mobile] <feature-name> (labels: needs-mobile)
   - [web] <feature-name> (labels: needs-web)
   - [server] <feature-name> (labels: needs-server)

3. Create git branch:
   git checkout -b feature/<feature-name>

4. Copy this template to parent issue description:
   [template]
```

## Integration with TDD Workflow

After feature creation:
1. Start with shared types in `packages/types`
2. Write tests for shared logic
3. Implement in `packages/shared`
4. Then implement per-app UI

## Example Output

```
✅ Feature Created: user-auth

Parent Issue:
  MYT-15: [Feature] user-auth
  https://linear.app/mytestenvironment/issue/MYT-15

Sub-Issues:
  MYT-16: [mobile] user-auth (needs-mobile)
  MYT-17: [web] user-auth (needs-web)
  MYT-18: [server] user-auth (needs-server)

Git Branch:
  feature/MYT-15-user-auth

Next Steps:
1. Define types in packages/types/src/auth.ts
2. Write tests in packages/shared/__tests__/auth.test.ts
3. Implement logic in packages/shared/src/auth.ts
4. Update MYT-16 when starting mobile implementation
```
