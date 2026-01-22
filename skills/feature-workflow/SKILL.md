---
name: feature-workflow
description: Create cross-app features with Linear tracking. Creates parent issue, sub-issues per app, and applies appropriate labels.
version: 1.0.0
---

# Cross-App Feature Orchestration

Use this skill to start a feature that spans multiple apps in a monorepo.

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

### 1. Parse Arguments

- `feature-name`: kebab-case feature identifier (e.g., `user-auth`)
- `apps`: space-separated list of apps (mobile, web, admin, server)

### 2. Create Parent Issue

Using Linear MCP, create the parent issue:

```javascript
linear.createIssue({
  title: "[Feature] <feature-name>",
  team: "Mytestenvironment",  // Adjust to your team
  labels: ["cross-app"],
  description: <feature-template>
})
```

### 3. Create Sub-Issues per App

For each app specified, create a sub-issue with:
- Title: `[<app>] <feature-name>`
- Labels: `needs-<app>`
- Parent: Link to parent issue

```javascript
for (const app of apps) {
  linear.createIssue({
    title: `[${app}] ${featureName}`,
    team: "Mytestenvironment",
    labels: [`needs-${app}`],
    parentId: parentIssue.id,
    description: `Implementation of ${featureName} for ${app} app.`
  })
}
```

### 4. Feature Template

Generate this template for the parent issue:

```markdown
## Feature: <feature-name>

### Implementation Status
| App | Status | Issue | PR |
|-----|--------|-------|-----|
| <app> | needs-<app> | MYT-X | - |

### Shared Code Checklist
- [ ] Types defined in @tafkeer/types (or packages/types)
- [ ] Business logic in @tafkeer/shared (or packages/shared)
- [ ] Design tokens used (no hardcoded colors)
- [ ] Tests written for shared code

### Requirements
[Fill in feature requirements]

### Technical Notes
[Add implementation notes]
```

### 5. Create Git Branch

After creating issues:
```bash
git checkout -b feature/<issue-id>-<feature-name>
```

### 6. Output Summary

Show:
- Parent issue ID and URL
- Sub-issue IDs for each app
- Git branch name
- Next steps

## App-to-Label Mapping

| App | Label Prefix |
|-----|--------------|
| mobile | needs-mobile / done-mobile |
| web | needs-web / done-web |
| admin | needs-admin / done-admin |
| server | needs-server / done-server |

## Label Workflow

1. **Starting**: All apps have `needs-<app>` label
2. **In Progress**: Issue in "In Progress" state
3. **Completed**: Change `needs-<app>` to `done-<app>`
4. **All Done**: Close parent issue when all done

## Fallback (No Linear MCP)

If Linear is not connected, output manual instructions:
- Issue titles and labels to create
- Template to copy
- Branch naming convention

```markdown
## Manual Steps (Linear not connected)

1. Create parent issue:
   - Title: [Feature] <feature-name>
   - Labels: cross-app

2. Create sub-issues:
   - [mobile] <feature-name> - labels: needs-mobile
   - [web] <feature-name> - labels: needs-web
   ...

3. Create branch:
   git checkout -b feature/<feature-name>

4. Copy template to parent issue description
```

## Error Handling

- Invalid app name: Show valid options (mobile, web, admin, server)
- Linear not connected: Show manual steps
- Issue creation fails: Show error and retry suggestion

## Integration with Development Workflow

After feature creation:

1. **Start with shared code** in `packages/types` and `packages/shared`
2. **Use TDD workflow** - write tests first
3. **Update issue status** as you progress
4. **Change labels** from `needs-*` to `done-*` as each app completes
5. **Close parent** when all apps are done
