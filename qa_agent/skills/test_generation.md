# Test Generation Skill (Deprecated - Split by Role)

This file was intentionally split into two separate skills.

Use these files instead:
- `qa_agent/skills/test_plan_generation.md`
- `qa_agent/skills/test_generation_from_plan.md`

## Role Split

1. **Planning role** (`test_plan_generation.md`)
   - Input: feature description
   - Output: plain-text test plan appended to `listOfTests.txt`
   - No pytest code generation

2. **Implementation role** (`test_generation_from_plan.md`)
   - Input: feature description
   - Reads: exact matching `FEATURE:` block from `listOfTests.txt`
   - Output: executable pytest tests under `generated_tests/`

## Mandatory Compatibility Rules

- Exact title match is required for plan lookup.
- Generated tests must only be created in `generated_tests/`.
- Do not modify `tests/`, `pages/`, or `utils/`.
- Reuse existing page objects, flows, fixtures, and repository patterns.
