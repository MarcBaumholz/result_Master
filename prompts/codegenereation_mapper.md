
### Step 3: Build Enhanced Prompt
```python
prompt = f"""
You are an expert Kotlin backend engineer.
Generate complete Controller/Service/Mapper implementation.

{CODING_RULES}

FIELD_MAPPING_ANALYSIS:
{mapping_info}

TEMPLATE_SCAFFOLD:
```kotlin
{template_text}
```

Instructions:
1. Replace placeholders and fill mapping blocks
2. Ensure imports and classes are consistent
3. Return only the complete Kotlin code file
"""
```

#### Phase 3 Coding Rules (embedded in prompt)
```
PHASE_3_CODING_RULES:
1) Architecture: Controller (@Controller + @Secured), Service (@Singleton), Mapper (object/class)
2) Security & Logging: Controller secured with SecurityRule.IS_AUTHENTICATED; SLF4J logger; log entry/errors
3) Error handling: try/catch in Controller and Service; HttpResponse.serverError on failure
4) Null-safety: prefer safe calls (?.) and elvis (?:); avoid NPEs; use defaults
5) Enum mapping: use when with else branch as fallback
6) Ground-truth: list verified METHOD+PATH and fields in header comment. Do NOT invent fields
7) Unmapped: add TODO("reason") where target cannot be derived
8) Output: return only Kotlin code (no markdown)
9) /me endpoint: resolve email from Authentication and call service
```