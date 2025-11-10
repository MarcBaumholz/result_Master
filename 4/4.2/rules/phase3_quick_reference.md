# 🚀 Phase 3 Quick Reference Card

## 📋 Essential Patterns

### Controller Template
```kotlin
@Controller("/api/resource")
@Secured(SecurityRule.IS_AUTHENTICATED)
class ResourceController(private val service: ResourceService) {
    
    private val log = LoggerFactory.getLogger(ResourceController::class.java)
    
    @Get("/me")
    fun getForMe(auth: Authentication): HttpResponse<Any> {
        return try {
            val email = (auth.attributes["email"] as? String) ?: auth.name
            val result = service.getResourcesByEmail(email)
            HttpResponse.ok(result)
        } catch (ex: Throwable) {
            log.error("Controller error", ex)
            HttpResponse.serverError()
        }
    }
}
```

### Service Template
```kotlin
@Singleton
class ResourceService(private val facadeClient: FacadeClient) {
    
    private val log = LoggerFactory.getLogger(ResourceService::class.java)
    
    fun getResourcesByEmail(email: String): Any {
        return try {
            val dto = facadeClient.fetchByEmail(email)
            Mapper.mapToTarget(dto)
        } catch (ex: Throwable) {
            log.error("Service error", ex)
            throw RuntimeException("Failed to fetch resources")
        }
    }
}
```

### Mapper Template
```kotlin
object Mapper {
    fun mapToTarget(source: SourceDTO): TargetDTO = TargetDTO(
        // Direct mappings
        id = source.id,
        email = source.email ?: "",
        
        // Type conversions
        startDate = source.startDate?.toLocalDate(),
        
        // Enum mappings
        status = when (source.status) {
            "active" -> Status.ACTIVE
            "inactive" -> Status.INACTIVE
            else -> Status.UNKNOWN
        },
        
        // Complex logic
        fullName = "${source.firstName} ${source.lastName}".trim(),
        
        // Unmapped fields
        endDate = TODO("Calculate based on business rules")
    )
}
```

---

## 🔑 Key Rules

### ✅ DO
- Use `@Secured(SecurityRule.IS_AUTHENTICATED)` on all endpoints
- Use `@Singleton` for services
- Use SLF4J logger throughout
- Use try/catch in Controller and Service
- Use null-safe operators (`?.`, `?:`)
- Use `when` expressions with `else` branch
- Use `TODO()` for unmapped fields
- Write TDD tests first

### ❌ DON'T
- Never use `!!` operator
- Never skip error handling
- Never skip security annotations
- Never skip logging
- Never skip null safety
- Never skip `else` branch in `when`
- Never skip testing

---

## 🧪 Testing Patterns

### Controller Test
```kotlin
@Test
fun `should return user resources successfully`() {
    // Given
    val email = "test@example.com"
    val auth = createMockAuth(email)
    
    // When
    val result = controller.getForMe(auth)
    
    // Then
    assertThat(result.status).isEqualTo(HttpStatus.OK)
}
```

### Mapper Test
```kotlin
@Test
fun `should map source to target successfully`() {
    // Given
    val source = SourceDTO(id = "123", email = "test@example.com")
    
    // When
    val result = Mapper.mapToTarget(source)
    
    // Then
    assertThat(result.id).isEqualTo("123")
    assertThat(result.email).isEqualTo("test@example.com")
}
```

---

## 🔧 Common Solutions

### Date Handling
```kotlin
private fun String.toLocalDate(): LocalDate? {
    return try {
        LocalDate.parse(this, DateTimeFormatter.ISO_LOCAL_DATE)
    } catch (ex: Exception) {
        null
    }
}
```

### Enum Mapping
```kotlin
private fun String.toStatus(): Status {
    return when (this.lowercase()) {
        "active" -> Status.ACTIVE
        "inactive" -> Status.INACTIVE
        else -> Status.UNKNOWN
    }
}
```

### String Operations
```kotlin
private fun buildFullName(firstName: String?, lastName: String?): String {
    return listOfNotNull(firstName, lastName)
        .joinToString(" ")
        .trim()
        .ifEmpty { "Unknown" }
}
```

---

## 📊 Quality Checklist

### Code Quality
- [ ] Controller/Service/Mapper architecture
- [ ] All endpoints secured
- [ ] SLF4J logging throughout
- [ ] Error handling in all layers
- [ ] Null-safe operations
- [ ] Enum mappings with `else` branch
- [ ] Unmapped fields marked with `TODO()`

### Testing
- [ ] TDD tests written and passing
- [ ] Happy path scenarios tested
- [ ] Error scenarios tested
- [ ] Null safety tested
- [ ] Security constraints tested

### Documentation
- [ ] Header comment with verified endpoints
- [ ] Mapped fields documented
- [ ] Unmapped fields explained
- [ ] Public methods documented

---

## 🚨 Common Issues & Fixes

### Issue: Null Pointer Exception
```kotlin
// ❌ Problem
val email = source.email!!

// ✅ Solution
val email = source.email ?: "unknown@example.com"
```

### Issue: Missing Error Handling
```kotlin
// ❌ Problem
fun getData(): String = service.fetchData()

// ✅ Solution
fun getData(): HttpResponse<String> = try {
    val data = service.fetchData()
    HttpResponse.ok(data)
} catch (ex: Throwable) {
    log.error("Failed to fetch data", ex)
    HttpResponse.serverError()
}
```

### Issue: Unsafe Enum Mapping
```kotlin
// ❌ Problem
val status = Status.valueOf(source.status)

// ✅ Solution
val status = when (source.status) {
    "active" -> Status.ACTIVE
    "inactive" -> Status.INACTIVE
    else -> Status.UNKNOWN
}
```

---

## 🔄 MCP Tool Usage

### Generate Code
```json
{
  "tool": "phase3_generate_mapper",
  "arguments": {
    "mapping_report_path": "/path/to/mapping_report.md",
    "output_directory": "/path/to/outputs/phase3"
  }
}
```

### Quality Audit
```json
{
  "tool": "phase3_quality_suite",
  "arguments": {
    "kotlin_file_path": "/path/to/generated_mapper.kt",
    "mapping_report_path": "/path/to/mapping_report.md"
  }
}
```

### TDD Validation
```json
{
  "tool": "phase4_tdd_validation",
  "arguments": {
    "kotlin_file_path": "/path/to/generated_mapper.kt",
    "mapping_report_path": "/path/to/mapping_report.md"
  }
}
```

---

## 📈 Success Metrics

### Code Quality
- **Test Coverage**: ≥95% for mappers
- **Cyclomatic Complexity**: ≤10 per method
- **File Size**: ≤200 lines per file
- **Null Safety**: 0 `!!` operators
- **Security**: 100% endpoints secured

### Performance
- **Response Time**: ≤100ms for simple operations
- **Memory Usage**: ≤50MB per request
- **Error Rate**: ≤1% for production endpoints

---

## 🎯 Final Checklist

Before Phase 3 complete:
- [ ] All quality gates passed
- [ ] All tests passing
- [ ] Code review completed
- [ ] Security review completed
- [ ] Performance review completed
- [ ] Documentation updated

---

*Keep this reference handy during Phase 3 development!*