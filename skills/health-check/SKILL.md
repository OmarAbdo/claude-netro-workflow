---
name: health-check
description: Run comprehensive codebase health scan. Detects feature alignment, code quality, test gaps, type issues, and design violations. Use when auditing any codebase.
version: 1.0.0
---

# Full Codebase Health Check

Run this when you inherit a project or want to audit current state.

## Process

1. **Detect project type**: monorepo (apps/), single app, or package
2. **Run feature alignment scan** (if monorepo)
3. **Run code quality scan**
4. **Run type consistency scan**
5. **Run test coverage analysis**
6. **Run design token check** (if applicable)
7. **Aggregate into single report**

## Commands to Run

```bash
# 1. Project structure
find . -maxdepth 2 -type d \( -name "apps" -o -name "packages" -o -name "src" \) 2>/dev/null | head -10

# 2. Large files (>500 lines)
find . -name "*.ts" -o -name "*.tsx" -o -name "*.js" | grep -v node_modules | xargs wc -l 2>/dev/null | sort -rn | head -20

# 3. Any type usages
grep -rn "\bany\b" --include="*.ts" --include="*.tsx" . 2>/dev/null | grep -v node_modules | wc -l

# 4. TODO/FIXME comments
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.ts" --include="*.tsx" . 2>/dev/null | grep -v node_modules | head -30

# 5. Console.log statements
grep -rn "console.log" --include="*.ts" --include="*.tsx" . 2>/dev/null | grep -v node_modules | wc -l

# 6. Hardcoded colors
grep -rn "#[0-9a-fA-F]\{3,6\}\b" --include="*.ts" --include="*.tsx" --include="*.css" . 2>/dev/null | grep -v node_modules | head -20

# 7. Test file count vs source file count
echo "Source files:" && find . -name "*.ts" -o -name "*.tsx" | grep -v node_modules | grep -v test | grep -v spec | wc -l
echo "Test files:" && find . -name "*.test.ts" -o -name "*.spec.ts" -o -name "*.test.tsx" | grep -v node_modules | wc -l
```

## Serena Mode (Semantic Analysis)

If Serena MCP is available, use semantic analysis for more accurate results:

```
# Get symbol overview for type analysis
serena.get_symbols_overview({ relative_path: "src/types.ts" })

# Find all type definitions
serena.find_symbol({ name_path_pattern: "interface", depth: 0 })

# Find any usages semantically
serena.search_for_pattern({ substring_pattern: "\\bany\\b", restrict_search_to_code_files: true })
```

## Output Format

Generate a report with:

### Summary
- Overall health score (0-100)
- Issue counts by severity (critical, high, medium, low)

### Detailed Findings

1. **Feature Alignment** (monorepos only)
   - Features present in some apps but not others
   - Recommendations for alignment

2. **Code Quality**
   - Top 10 largest files with line counts
   - TODO/FIXME count and locations
   - Console.log count

3. **Type Consistency**
   - `any` usage count and top locations
   - Missing type exports

4. **Test Coverage**
   - Test-to-source file ratio
   - Modules with no tests

5. **Design Tokens**
   - Hardcoded colors found
   - Hardcoded spacing values

### Top 5 Priorities

List the 5 most impactful fixes to improve codebase health.

## Save Report

Save results to `health-report.json` in the project root.

```json
{
  "timestamp": "ISO-8601",
  "projectPath": "...",
  "overallScore": 72,
  "summary": {
    "critical": 3,
    "high": 15,
    "medium": 30,
    "low": 50
  },
  "scans": {
    "featureAlignment": { "score": 80, "issues": [] },
    "codeQuality": { "score": 65, "issues": [] },
    "typeConsistency": { "score": 70, "issues": [] },
    "testCoverage": { "score": 60, "issues": [] }
  },
  "topPriorities": []
}
```
