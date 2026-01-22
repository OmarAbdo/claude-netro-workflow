---
name: init-project
description: Initialize a project with the Tafkeer workflow - creates .claude folder, rules, templates, and configures hooks
arguments:
  - name: type
    description: Project type (monorepo, single-app, package)
    required: false
    default: auto-detect
---

# Initialize Project with Tafkeer Workflow

This command sets up a new project with the complete Tafkeer development workflow.

## What It Does

1. **Detects project type** (monorepo, single-app, or package)
2. **Creates `.claude/` directory** with project-specific configuration
3. **Copies appropriate rules** for the project type
4. **Sets up CLAUDE.md** with project instructions
5. **Configures Linear integration** if available
6. **Runs initial health check** to baseline the codebase

## Usage

```
/init-project [type]
```

- `type` (optional): `monorepo`, `single-app`, or `package`
- If not specified, auto-detects based on directory structure

## Process

### Step 1: Detect Project Type

```bash
# Check for monorepo indicators
if [ -d "apps" ] || [ -d "packages" ]; then
  PROJECT_TYPE="monorepo"
elif [ -f "package.json" ]; then
  PROJECT_TYPE="single-app"
else
  PROJECT_TYPE="package"
fi
```

### Step 2: Create Directory Structure

```bash
mkdir -p .claude/rules
mkdir -p .claude/templates
```

### Step 3: Create Project CLAUDE.md

Generate CLAUDE.md based on project type:

**For Monorepo:**
```markdown
# [Project Name] - AI Agent Guide

## Overview
This is a TypeScript monorepo with the following apps:
- [List detected apps]

## Core Principles
1. Code reuse: Business logic in packages/shared
2. Type safety: Types in packages/types
3. Design consistency: Design tokens for styling

## Development Workflow
- Use TDD: Write tests first
- Use Linear: Track features with /feature command
- Use health checks: Run /health-check regularly

## Quick Commands
- `/feature <name> <apps...>` - Create cross-app feature
- `/health-check` - Run codebase health scan
- `/scan-types` - Check type consistency
```

**For Single App:**
```markdown
# [Project Name] - AI Agent Guide

## Overview
Single TypeScript application.

## Development Workflow
- Use TDD: Write tests first
- Keep files under 500 lines
- No `any` types

## Quick Commands
- `/health-check` - Run codebase health scan
- `/scan-quality` - Check code quality
```

### Step 4: Create Project Rules

**For Monorepo - .claude/rules/architecture.md:**
```markdown
---
paths: ["**/*.ts", "**/*.tsx"]
---
# Architecture Rules

## Package Structure
- Business logic → packages/shared
- Types → packages/types
- UI Components → individual apps

## Import Rules
- Apps import from shared packages, never from other apps
- Types always from @<scope>/types
```

**For All Projects - .claude/rules/code-quality.md:**
```markdown
---
paths: ["**/*.ts", "**/*.tsx"]
---
# Code Quality Rules

## Must Avoid
- `any` types (use `unknown` with type guards)
- Files > 500 lines
- Functions > 50 lines
- console.log in production code
- Hardcoded colors/spacing

## Must Have
- Return types on exported functions
- Tests for business logic
- Error handling for async operations
```

### Step 5: Create Progress Template

**.claude/templates/progress.json:**
```json
{
  "_comment": "Copy this when starting complex tasks",
  "task": "DESCRIBE THE TASK",
  "started_at": "TIMESTAMP",
  "status": "in_progress",
  "requirements": [
    {
      "id": 1,
      "description": "First requirement",
      "status": "pending",
      "verification": "How to verify"
    }
  ],
  "verification_results": {
    "tests_passing": null,
    "coverage_percent": null,
    "lint_clean": null
  }
}
```

### Step 6: Add to .gitignore

Ensure `.claude/` sensitive files are ignored:
```
# Claude Code
.claude/*.local.md
.claude/progress.json
.claude/output-logs/
```

### Step 7: Run Initial Health Check

Execute the health-check agent to baseline the codebase:
- Generate initial health-report.json
- Identify existing issues
- Establish baseline score

### Step 8: Linear Setup (if available)

If Linear MCP is connected:
1. Check if project labels exist
2. Create missing labels
3. Display Linear project link

## Output

After initialization, display:

```
✅ Project initialized with Tafkeer Workflow

Project Type: monorepo
Apps Detected: mobile, web, server

Created:
  .claude/CLAUDE.md
  .claude/rules/architecture.md
  .claude/rules/code-quality.md
  .claude/templates/progress.json
  Updated .gitignore

Initial Health Score: 72/100
- Critical issues: 3
- High issues: 15
- See health-report.json for details

Next Steps:
1. Review .claude/CLAUDE.md and customize
2. Address critical issues from health report
3. Start development with /feature or write code

Linear Status: Connected ✅
- Workspace: Mytestenvironment
- Labels: 14 configured
```

## Customization

After init, users should:
1. Update CLAUDE.md with project-specific details
2. Add custom rules for their stack
3. Configure Linear workspace if different
4. Set up additional MCP servers as needed
