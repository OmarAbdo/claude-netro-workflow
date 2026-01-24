---
name: scan-types
description: Find type inconsistencies - any usages, duplicate types, missing return types. Uses Serena MCP for semantic analysis if available.
version: 1.0.0
---

# Type Consistency Scanner

Find TypeScript type issues that can lead to runtime errors.

## Mode Selection

This skill can run in two modes:

1. **Serena Mode** (preferred): Uses semantic analysis via Serena MCP
2. **Grep Mode** (fallback): Uses text-based pattern matching

Check for Serena availability first. If Serena MCP is connected, use semantic mode for more accurate results.

---

## Serena Mode (Semantic Analysis)

When Serena MCP is available, use these operations:

### 1. Find All Type Definitions

```
serena.get_symbols_overview({ relative_path: "packages/types/src/" })
serena.find_symbol({ name_path_pattern: "*", include_kinds: [5, 11], depth: 0 })
# Kind 5 = Interface, Kind 11 = TypeAlias
```

This returns actual TypeScript types with:
- Symbol name
- File location
- Full type definition
- References count

### 2. Find `any` Type Usages

```
serena.search_for_pattern({
  substring_pattern: "\\bany\\b",
  restrict_search_to_code_files: true,
  context_lines_before: 1,
  context_lines_after: 1
})
```

More accurate than grep because it:
- Distinguishes `any` type from variable names containing "any"
- Finds implicit `any` from missing type annotations
- Identifies `any` in generic parameters

### 3. Find Duplicate Type Names

```
serena.find_symbol({ name_path_pattern: "User", depth: 0 })
# If returns multiple locations, types are duplicated
```

Semantic comparison can detect:
- Exact duplicates (same structure)
- Similar types (mostly same properties)
- Type aliases that resolve to same type

### 4. Find Unused Exports

```
serena.find_referencing_symbols({ name_path: "SomeType", relative_path: "src/types.ts" })
# If returns empty, type is unused
```

### 5. Find Missing Return Types

```
serena.find_symbol({
  name_path_pattern: "*",
  include_kinds: [12], # Function
  include_body: true
})
# Check if function signature includes return type
```

---

## Grep Mode (Fallback)

If Serena is unavailable, use text-based scanning:

### 1. Any Type Usages

```bash
# Count total
grep -rn "\bany\b" --include="*.ts" --include="*.tsx" . 2>/dev/null | grep -v node_modules | wc -l

# Show locations
grep -rn "\bany\b" --include="*.ts" --include="*.tsx" . 2>/dev/null | grep -v node_modules | head -30
```

### 2. Duplicate Type Definitions

```bash
# Find all type/interface definitions and check for duplicates
grep -rhn "^export \(interface\|type\) [A-Z][a-zA-Z]*" --include="*.ts" . 2>/dev/null | grep -v node_modules | sort -t: -k2 | uniq -d -f1
```

### 3. Missing Return Types

```bash
# Functions without explicit return types
grep -rn "function [a-zA-Z]*(" --include="*.ts" . 2>/dev/null | grep -v node_modules | grep -v "): " | head -20
```

### 4. Type Imports from Wrong Locations

```bash
# Check if importing types from apps instead of shared package
grep -rn "import.*from.*apps/" --include="*.ts" . 2>/dev/null | grep -v node_modules | head -20
```

### 5. Unknown Type Usage

```bash
grep -rn "\bunknown\b" --include="*.ts" --include="*.tsx" . 2>/dev/null | grep -v node_modules | wc -l
```

---

## Output Format

### Summary

| Issue | Count | Severity | Mode Used |
|-------|-------|----------|-----------|
| `any` usages | X | High | Serena/Grep |
| Duplicate types | X | Medium | Serena/Grep |
| Missing return types | X | Low | Serena/Grep |
| Wrong import locations | X | High | Grep |
| Unused exports | X | Medium | Serena only |

### Any Usages - Top 10 Files

| File | Count | Example Line |
|------|-------|--------------|
| src/api/client.ts | 15 | `function fetchData(data: any)` |
| ... | ... | ... |

### Duplicate Types Found

| Type Name | Locations | Identical? |
|-----------|-----------|------------|
| User | apps/mobile/types.ts, apps/web/types.ts | Yes |
| ... | ... | ... |

### Recommendations

1. **Centralize types**: Move to packages/types or @tafkeer/types
2. **Replace any with unknown**: Then narrow with type guards
3. **Add return types**: Especially to exported functions
4. **Fix import paths**: Import from @tafkeer/types not relative paths
5. **Remove unused exports**: Clean up dead code

---

## Comparison: Serena vs Grep

| Aspect | Serena | Grep |
|--------|--------|------|
| Accuracy | High (AST-based) | Medium (text patterns) |
| Speed | Slower (parses code) | Fast |
| Implicit any detection | Yes | No |
| Structural comparison | Yes | No |
| Unused export detection | Yes | No |
| Setup required | MCP connection | None |

**Recommendation**: Use Serena for thorough audits, Grep for quick checks.
