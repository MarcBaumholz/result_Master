You are a Kotlin reviewer. Audit this code against rules:
"Controller annotated with @Controller and @Secured(SecurityRule.IS_AUTHENTICATED)",
"Controller returns HttpResponse and handles errors with serverError()",
"Service annotated with @Singleton and logs errors; rethrows with concise message",
"Mapper uses null-safe operators and elvis defaults; no unsafe !!",
"Enum with when has else fallback",
"Header comment lists verified METHOD+PATH and mapped fields",

Code:
```kotlin
{code}
```

Return JSON:
{{
  "violations": [{{
    "rule": "string", 
    "finding": "string", 
    "lineHint": "string"
  }}],
  "suggestions": ["string"]
}}
"""

# Execute audit
response = get_llm_response(prompt, model=model, max_tokens=1500)
audit_data = json.loads(response)
```

#### Audit Rules
```python
AUDIT_RULES = [
    "Controller annotated with @Controller and @Secured(SecurityRule.IS_AUTHENTICATED)",
    "Controller returns HttpResponse and handles errors with serverError()",
    "Service annotated with @Singleton and logs errors; rethrows with concise message",
    "Mapper uses null-safe operators and elvis defaults; no unsafe !!",
    "Enum with when has else fallback",
    "Header comment lists verified METHOD+PATH and mapped fields"
]
```