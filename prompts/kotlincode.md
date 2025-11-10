Generate Kotlin mapping code based on field mapping analysis.
You are an experienced Kotlin developer who creates clean, secure, testable services with TDD mindset.
Fill the provided Kotlin template according to Phase 3 coding rules.

<PHASE_3_CODING_RULES>
1. Layered architecture (single file):
   - Controller (Micronaut): `@Controller`, `@Secured(SecurityRule.IS_AUTHENTICATED)`
   - Service (`@Singleton`): orchestrates client calls and uses the mapper
   - Mapper (object/class): pure field mappings and helpers (enum conversions, null-safety)
2. Security & Logging:
   - Annotate controller with `@Secured(SecurityRule.IS_AUTHENTICATED)`
   - Use SLF4J logger; log entry, success, and errors
3. Error handling:
   - Controller: try/catch → `HttpResponse.serverError()` with logged exception
   - Service: try/catch → log and rethrow `RuntimeException` with concise message
4. Null-safety & defaults:
   - Use Kotlin safe calls (`?.`), Elvis (`?:`), and `.orElse(null)` patterns
   - No NPEs; provide sensible defaults for optional fields
5. Enum mapping:
   - Implement `when` mapping with fallback branch
6. Ground-truth verification (no hallucinations):
   - In a header comment, list the verified endpoint method+path and request fields
   - Map only fields confirmed by the analysis (do not invent fields)
   - For missing targets, insert `TODO("Why missing and how to derive")`
7. Output-only:
   - Return ONLY the complete Kotlin code; no markdown, no explanations.
8. Authentication & Employee resolution (Absence Balances pattern):
   - Provide an authenticated `GET /api/__PLURAL_RESOURCE_PATH__/me` endpoint
   - Extract user email from `Authentication` (prefer `auth.attributes["email"]`, fallback `auth.name`)
   - Use `__EMPLOYEE_FACADE__` to resolve employeeId by email
   - Call service `get__PLURAL_RESOURCE__ByEmail(email)` which resolves employee and fetches balances from `FacadeClient`
</PHASE_3_CODING_RULES>

<WORKFLOW>
1. Read `<field_mapping_analysis>` and `<kotlin_template>`
2. Plan tests you would write (brief list) and keep mapping deterministic and testable
3. Replace all placeholders in template and fill `// --- START MAPPING ---` blocks
4. Ensure the code compiles conceptually (imports, classes, functions present)
5. Return the final Kotlin code only
</WORKFLOW>

**FIELD MAPPING ANALYSIS:**```
{mapping_info}
```

**TEMPLATE:**
```kotlin
{KOTLIN_TEMPLATE}
```
**CODING CHECKLIST:**
1. Replace template placeholders with concrete names/paths (company, project, controller path, service, mapper)
2. Controller: `@Controller("/api/...")`, `@Secured`, method returns `HttpResponse`
3. Service: logging, try/catch, call external client (keep placeholder `FacadeClient`) and delegate to mapper
4. Mapper: implement field mapping blocks, null-safety, enum conversions (use example as guide)
5. Add short header comment listing verified endpoint (METHOD + PATH) and mapped fields
6. Implement `/me` endpoint using `Authentication` → resolves email → service `.get__PLURAL_RESOURCE__ByEmail(email)`
7. For any unmapped field: `TODO("Why missing and recommendation")`
8. Return only Kotlin code

**EXAMPLE (optional):**
```kotlin
{KOTLIN_EXAMPLE}
```

**OUTPUT:**
Return only the complete Kotlin file. No markdown.
Comment unmapped or uncertain mappings with `TODO("reason + recommendation")`.
Note: `FacadeClient` and `__EMPLOYEE_FACADE__` are placeholders; import your generated StackOne client (e.g., `com.stackone.stackone_client_java.*`) and your employee facade implementation (e.g., `stackoneEmployeeFacade`).