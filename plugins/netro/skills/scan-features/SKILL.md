---
name: scan-features
description: Detect feature alignment issues across apps in a monorepo. Identifies features present in some apps but missing in others.
version: 1.0.0
---

# Feature Alignment Scanner

Analyze which features exist in which apps in a monorepo.

## When to Use

- Auditing a monorepo for consistency
- Planning cross-app feature development
- Identifying technical debt from unfinished features
- Before starting a new cross-app feature

## Process

### 1. Detect Apps

```bash
# List all apps in monorepo
ls -la apps/ 2>/dev/null || ls -la packages/ 2>/dev/null
```

### 2. Feature Detection Patterns

For each app, check for common features:

| Feature | Detection Pattern |
|---------|-------------------|
| Auth/Login | `auth/`, `login`, `useAuth`, `AuthProvider` |
| Payments | `stripe`, `payment`, `checkout`, `billing` |
| API Integration | `trpc`, `api/`, `fetch`, `axios` |
| State Management | `zustand`, `redux`, `store/`, `useStore` |
| Testing | `__tests__`, `.test.`, `.spec.`, `vitest`, `jest` |
| i18n | `i18n/`, `translations`, `useTranslation` |
| Analytics | `analytics`, `tracking`, `mixpanel`, `amplitude` |
| Push Notifications | `notification`, `push`, `firebase` |
| File Upload | `upload`, `file`, `storage`, `s3` |
| Search | `search`, `algolia`, `elasticsearch` |

### 3. Scan Commands

```bash
# Auth detection
echo "=== Auth ===" && \
for app in apps/*/; do \
  echo -n "$app: "; \
  (grep -rl "useAuth\|AuthProvider\|login" "$app" 2>/dev/null | head -1) && echo "YES" || echo "NO"; \
done

# Payments detection
echo "=== Payments ===" && \
for app in apps/*/; do \
  echo -n "$app: "; \
  (grep -rl "stripe\|payment\|checkout" "$app" 2>/dev/null | head -1) && echo "YES" || echo "NO"; \
done

# Testing detection
echo "=== Testing ===" && \
for app in apps/*/; do \
  echo -n "$app: "; \
  (find "$app" -name "*.test.ts" -o -name "*.spec.ts" 2>/dev/null | head -1) && echo "YES" || echo "NO"; \
done
```

### 4. Serena Mode (Semantic)

If Serena MCP is available:

```
# Find specific hooks/providers across codebase
serena.search_for_pattern({
  substring_pattern: "useAuth|AuthProvider|AuthContext",
  restrict_search_to_code_files: true
})

# Find class/function definitions
serena.find_symbol({
  name_path_pattern: "Auth*",
  substring_matching: true
})
```

## Output Format

### Feature Matrix

| Feature | mobile | web | admin | server | Status |
|---------|--------|-----|-------|--------|--------|
| Auth | YES | YES | NO | YES | Gap: admin |
| Payments | YES | NO | NO | YES | Gap: web, admin |
| Testing | YES | YES | NO | YES | Gap: admin |
| i18n | YES | NO | NO | N/A | Gap: web |

### Gap Analysis

1. **admin** missing 4 features: Auth, Payments, Testing, i18n
2. **web** missing 2 features: Payments, i18n

### Recommendations

1. **High Priority**: Add auth to admin (security requirement)
2. **Medium Priority**: Add testing to admin
3. **Low Priority**: Add i18n to web (if targeting international users)

## Integration with Linear

If Linear MCP is available, create tracking issues:

```
For each missing feature:
1. Check if issue already exists with label "needs-<app>"
2. If not, create issue:
   - Title: "[<app>] Add <feature>"
   - Labels: ["cross-app", "needs-<app>"]
   - Description: "Feature exists in [apps] but missing in <app>"
```

## Save Results

Save to `feature-alignment.json`:

```json
{
  "timestamp": "ISO-8601",
  "apps": ["mobile", "web", "admin", "server"],
  "features": {
    "auth": {
      "mobile": true,
      "web": true,
      "admin": false,
      "server": true
    }
  },
  "gaps": [
    { "feature": "auth", "missingIn": ["admin"], "priority": "high" }
  ]
}
```
