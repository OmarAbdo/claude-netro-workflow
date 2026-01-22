---
paths: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"]
---

# Code Quality Standards

## Type Safety

### Must Avoid
- `any` type - use `unknown` with type guards instead
- Type assertions (`as`) without justification
- Implicit any from missing annotations

### Must Have
- Return types on exported functions
- Proper generic constraints
- Strict TypeScript settings

```typescript
// ❌ BAD
function process(data: any) { ... }

// ✅ GOOD
function process(data: unknown): Result {
  if (isValidData(data)) { ... }
}
```

## File Size Limits

| Metric | Limit | Action |
|--------|-------|--------|
| File lines | 500 | Split into modules |
| Function lines | 50 | Extract helpers |
| Nesting depth | 4 | Refactor logic |

## Forbidden Patterns

### In Production Code
- `console.log()` - use proper logging
- `debugger` statements
- Commented-out code blocks
- `// @ts-ignore` without explanation

### In All Code
- Magic numbers (use named constants)
- Hardcoded strings (use constants/i18n)
- Deeply nested conditionals
- God objects/functions

## Required Patterns

### Error Handling
```typescript
// ✅ Always handle errors
try {
  await riskyOperation();
} catch (error) {
  logger.error('Operation failed', { error });
  throw new AppError('OPERATION_FAILED', error);
}
```

### Async/Await
```typescript
// ✅ Always await promises
const result = await fetchData();

// ❌ Don't ignore promises
fetchData(); // Missing await!
```

### Input Validation
```typescript
// ✅ Validate at boundaries
const parsed = userSchema.parse(input);
```

## Documentation

- JSDoc for exported functions
- README for modules
- Comments only for non-obvious logic
- No obvious comments ("increment i")
