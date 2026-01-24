---
name: scan-quality
description: Find code quality issues - large files, duplication, tech debt markers, console.log statements, deep nesting.
version: 1.0.0
---

# Code Quality Scanner

Identify code quality issues that affect maintainability and reliability.

## Checks Performed

1. **Large files** (>500 lines)
2. **Large functions** (>50 lines)
3. **TODO/FIXME comments** (tech debt markers)
4. **Console.log statements** (debug leftovers)
5. **Commented out code blocks**
6. **Deep nesting** (>4 levels)
7. **Magic numbers/strings**
8. **Duplicate code patterns**

## Commands

### Large Files

```bash
# Find files > 500 lines
find . -name "*.ts" -o -name "*.tsx" | grep -v node_modules | xargs wc -l 2>/dev/null | sort -rn | head -20 | awk '$1 > 500 {print}'
```

### TODO/FIXME Comments

```bash
# Count and list tech debt markers
echo "=== Tech Debt Markers ===" && \
grep -rn "TODO\|FIXME\|HACK\|XXX\|BUG\|TEMP" --include="*.ts" --include="*.tsx" . 2>/dev/null | \
grep -v node_modules | head -50

# Count by type
echo "TODO:" && grep -rn "TODO" --include="*.ts" . 2>/dev/null | grep -v node_modules | wc -l
echo "FIXME:" && grep -rn "FIXME" --include="*.ts" . 2>/dev/null | grep -v node_modules | wc -l
echo "HACK:" && grep -rn "HACK" --include="*.ts" . 2>/dev/null | grep -v node_modules | wc -l
```

### Console.log Statements

```bash
# Find console.log (should be removed in production code)
echo "=== Console Statements ===" && \
grep -rn "console\.\(log\|warn\|error\|debug\|info\)" --include="*.ts" --include="*.tsx" . 2>/dev/null | \
grep -v node_modules | grep -v ".test." | grep -v ".spec." | head -30
```

### Commented Out Code

```bash
# Find potential commented code blocks (// followed by code-like patterns)
grep -rn "^[[:space:]]*//.*[{};=()]" --include="*.ts" --include="*.tsx" . 2>/dev/null | \
grep -v node_modules | head -20
```

### Deep Nesting

```bash
# Find deeply nested code (rough detection via indentation)
grep -rn "^[[:space:]]\{16,\}" --include="*.ts" --include="*.tsx" . 2>/dev/null | \
grep -v node_modules | head -20
```

### Magic Numbers

```bash
# Find magic numbers (numbers that aren't 0, 1, or in obvious contexts)
grep -rn "[^a-zA-Z0-9_][2-9][0-9]\{2,\}[^a-zA-Z0-9_x]" --include="*.ts" --include="*.tsx" . 2>/dev/null | \
grep -v node_modules | grep -v "port\|timeout\|delay\|width\|height" | head -20
```

## Serena Mode

If Serena MCP is available for deeper analysis:

```
# Find large functions
serena.find_symbol({
  name_path_pattern: "*",
  include_kinds: [12], # Functions
  include_body: true
})
# Then analyze body length

# Find complex nesting
serena.search_for_pattern({
  substring_pattern: "if.*{[\\s\\S]*if.*{[\\s\\S]*if.*{",
  restrict_search_to_code_files: true,
  context_lines_before: 2,
  context_lines_after: 10
})
```

## Output Format

### Summary

| Category | Count | Severity |
|----------|-------|----------|
| Large files (>500 lines) | X | High |
| TODO/FIXME comments | X | Medium |
| Console.log statements | X | Medium |
| Deep nesting (>4 levels) | X | High |
| Commented out code | X | Low |

### Large Files (Top 10)

| File | Lines | Recommendation |
|------|-------|----------------|
| src/components/Dashboard.tsx | 850 | Split into smaller components |
| src/api/client.ts | 620 | Extract API helpers |

### Tech Debt Locations

| File | Line | Type | Comment |
|------|------|------|---------|
| src/auth/login.ts | 45 | TODO | "Add rate limiting" |
| src/api/client.ts | 120 | FIXME | "Handle network errors" |

### Console.log to Remove

| File | Line | Statement |
|------|------|-----------|
| src/debug.ts | 10 | console.log('debug data:', data) |

### Recommendations

1. **Immediate**: Remove 15 console.log statements before deployment
2. **This Sprint**: Split Dashboard.tsx into smaller components
3. **Backlog**: Address 23 TODO comments as separate tasks

## Scoring

Calculate quality score:

```
Base Score: 100

Deductions:
- Each file >500 lines: -2 points
- Each file >1000 lines: -5 points
- Each TODO/FIXME: -0.5 points
- Each console.log in non-test: -1 point
- Each deep nesting instance: -2 points

Final Score = max(0, Base - Deductions)
```

## Save Results

Save to `quality-report.json`:

```json
{
  "timestamp": "ISO-8601",
  "score": 72,
  "findings": {
    "largeFiles": [
      { "path": "src/Dashboard.tsx", "lines": 850 }
    ],
    "techDebt": [
      { "path": "src/auth.ts", "line": 45, "type": "TODO", "text": "..." }
    ],
    "consoleLogs": 15,
    "deepNesting": 3
  }
}
```
