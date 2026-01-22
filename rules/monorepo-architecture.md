---
paths: ["apps/**/*", "packages/**/*"]
---

# Monorepo Architecture Rules

## Package Boundaries

### Where Code Lives

| Code Type | Location | Example |
|-----------|----------|---------|
| Business Logic | `packages/shared` | API clients, auth utils |
| Types | `packages/types` | Interfaces, enums |
| UI Components | App-specific | `apps/web/components` |
| API Routes | `apps/server` | tRPC routers |

### Import Rules

```typescript
// ✅ CORRECT: Import from packages
import { useAuth } from '@scope/shared';
import type { User } from '@scope/types';

// ❌ WRONG: Import from other apps
import { useAuth } from '../../apps/mobile/hooks';

// ❌ WRONG: Relative imports across packages
import { User } from '../../../packages/types';
```

## Type Centralization

### All Types in packages/types

```typescript
// packages/types/src/user.ts
export interface User {
  id: string;
  email: string;
  name: string;
}

// packages/types/src/index.ts
export * from './user';
```

### Never Duplicate Types

```typescript
// ❌ WRONG: Type defined in app
// apps/mobile/types/user.ts
interface User { ... }

// ✅ CORRECT: Import from shared
// apps/mobile/screens/profile.tsx
import type { User } from '@scope/types';
```

## Shared Logic

### Business Logic in packages/shared

```typescript
// packages/shared/src/hooks/use-auth.ts
export function useAuth() {
  // All auth logic here
}

// apps/mobile/hooks/index.ts
export { useAuth } from '@scope/shared';
```

### What Goes Where

| Logic | packages/shared | App-specific |
|-------|-----------------|--------------|
| Auth/Session | ✅ | |
| API calls | ✅ | |
| Data formatting | ✅ | |
| Validation schemas | ✅ | |
| Platform UI | | ✅ |
| Navigation | | ✅ |
| Native features | | ✅ |

## Cross-App Feature Development

### Process

1. **Types First** - Define in `packages/types`
2. **Shared Logic** - Implement in `packages/shared`
3. **Write Tests** - Test shared code
4. **App Integration** - Use in each app
5. **Track Progress** - Use Linear labels

### Linear Labels

| Label | Meaning |
|-------|---------|
| `needs-mobile` | Feature needs mobile implementation |
| `done-mobile` | Mobile implementation complete |
| `cross-app` | Feature spans multiple apps |

## Design Tokens

### Use Design System

```typescript
// ✅ CORRECT
import { colors, spacing } from '@scope/design-tokens';
const style = { backgroundColor: colors.primary };

// ❌ WRONG
const style = { backgroundColor: '#9333EA' };
```

### Token Categories

- Colors: `colors.primary`, `colors.error`
- Spacing: `spacing.sm`, `spacing.md`
- Typography: `fonts.body`, `fonts.heading`
- Borders: `borders.radius`, `borders.width`
