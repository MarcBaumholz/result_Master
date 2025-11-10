# 🚀 Phase 3 Implementation Guide

## 📚 Overview
This guide provides practical examples and step-by-step instructions for implementing Phase 3 Kotlin mapper code generation following the Phase 3 Coding Rules.

---

## 🎯 Quick Start

### 1. Prerequisites
- Phase 2 mapping report completed and verified
- API endpoints identified and validated
- Field mappings documented with confidence scores
- Human approval received for mapping decisions

### 2. Tool Usage Sequence
```bash
# Step 1: Generate Kotlin code
phase3_generate_mapper(
    mapping_report_path="/path/to/mapping_report.md",
    output_directory="/path/to/outputs/phase3"
)

# Step 2: Quality audit and TDD tests
phase3_quality_suite(
    kotlin_file_path="/path/to/generated_mapper.kt",
    mapping_report_path="/path/to/mapping_report.md"
)

# Step 3: TDD validation with Cursor LLM
phase4_tdd_validation(
    kotlin_file_path="/path/to/generated_mapper.kt",
    mapping_report_path="/path/to/mapping_report.md"
)
```

---

## 🏗️ Architecture Implementation

### Complete Example: Absence Management Mapper

```kotlin
package com.flip.integrations.absence

import io.micronaut.http.*
import io.micronaut.http.annotation.*
import io.micronaut.security.annotation.*
import io.micronaut.security.rules.SecurityRule
import jakarta.inject.Singleton
import org.slf4j.LoggerFactory
import io.micronaut.security.authentication.Authentication
import java.time.LocalDate
import java.time.format.DateTimeFormatter

/**
 * Verified Endpoint(s):
 * - POST /api/timeOffEntries
 * Fields: id, employeeId, startDate, endDate, status, type, reason, duration
 */
@Controller("/api/absence")
@Secured(SecurityRule.IS_AUTHENTICATED)
class AbsenceController(private val service: AbsenceService) {

    private val log = LoggerFactory.getLogger(AbsenceController::class.java)

    @Get("/me")
    fun getMyAbsences(auth: Authentication): HttpResponse<Any> {
        return try {
            val email = (auth.attributes["email"] as? String) ?: auth.name
            val result = service.getAbsencesByEmail(email)
            HttpResponse.ok(result)
        } catch (ex: Throwable) {
            log.error("Failed to fetch absences for user: {}", email, ex)
            HttpResponse.serverError()
        }
    }

    @Post("/submit")
    fun submitAbsence(
        auth: Authentication,
        @Body request: AbsenceRequest
    ): HttpResponse<Any> {
        return try {
            val email = (auth.attributes["email"] as? String) ?: auth.name
            val result = service.submitAbsence(email, request)
            HttpResponse.ok(result)
        } catch (ex: ValidationException) {
            log.warn("Validation failed for user: {}", email, ex)
            HttpResponse.badRequest(mapOf("error" to ex.message))
        } catch (ex: Throwable) {
            log.error("Failed to submit absence for user: {}", email, ex)
            HttpResponse.serverError()
        }
    }
}

@Singleton
class AbsenceService(private val workdayClient: WorkdayClient) {
    
    private val log = LoggerFactory.getLogger(AbsenceService::class.java)

    fun getAbsencesByEmail(email: String): List<AbsenceDTO> {
        return try {
            val workdayData = workdayClient.fetchAbsencesByEmail(email)
            workdayData.map { AbsenceMapper.mapToTarget(it) }
        } catch (ex: Throwable) {
            log.error("Failed to fetch absences for email: {}", email, ex)
            throw RuntimeException("Failed to fetch absences")
        }
    }

    fun submitAbsence(email: String, request: AbsenceRequest): AbsenceSubmissionResult {
        return try {
            val workdayRequest = AbsenceMapper.mapToWorkdayRequest(request, email)
            val result = workdayClient.submitAbsence(workdayRequest)
            AbsenceSubmissionResult.success(result.id)
        } catch (ex: Throwable) {
            log.error("Failed to submit absence for email: {}", email, ex)
            throw RuntimeException("Failed to submit absence")
        }
    }
}

object AbsenceMapper {
    
    fun mapToTarget(source: WorkdayAbsenceData): AbsenceDTO = AbsenceDTO(
        // Direct mappings
        id = source.id,
        employeeId = source.employeeId,
        
        // Null-safe mappings with defaults
        startDate = source.startDate?.toLocalDate(),
        endDate = source.endDate?.toLocalDate(),
        reason = source.reason ?: "No reason provided",
        
        // Enum mappings with fallback
        status = when (source.status) {
            "approved" -> AbsenceStatus.APPROVED
            "pending" -> AbsenceStatus.PENDING
            "rejected" -> AbsenceStatus.REJECTED
            else -> AbsenceStatus.UNKNOWN
        },
        
        type = when (source.type) {
            "vacation" -> AbsenceType.VACATION
            "sick" -> AbsenceType.SICK_LEAVE
            "personal" -> AbsenceType.PERSONAL
            else -> AbsenceType.OTHER
        },
        
        // Complex logic
        duration = calculateDuration(source.startDate, source.endDate),
        fullName = "${source.firstName} ${source.lastName}".trim(),
        
        // Unmapped fields
        approvalDate = TODO("Calculate based on status and business rules"),
        approverEmail = TODO("Fetch from approval workflow")
    )
    
    fun mapToWorkdayRequest(request: AbsenceRequest, email: String): WorkdayAbsenceRequest {
        return WorkdayAbsenceRequest(
            employeeEmail = email,
            startDate = request.startDate,
            endDate = request.endDate,
            type = request.type.toWorkdayType(),
            reason = request.reason ?: "",
            // Unmapped fields
            approverId = TODO("Determine approver based on employee hierarchy")
        )
    }
    
    private fun calculateDuration(startDate: String?, endDate: String?): Int {
        if (startDate == null || endDate == null) return 0
        return try {
            val start = startDate.toLocalDate()
            val end = endDate.toLocalDate()
            start.until(end).days + 1
        } catch (ex: Exception) {
            0
        }
    }
    
    private fun String.toLocalDate(): LocalDate {
        return LocalDate.parse(this, DateTimeFormatter.ISO_LOCAL_DATE)
    }
    
    private fun AbsenceType.toWorkdayType(): String {
        return when (this) {
            AbsenceType.VACATION -> "vacation"
            AbsenceType.SICK_LEAVE -> "sick"
            AbsenceType.PERSONAL -> "personal"
            AbsenceType.OTHER -> "other"
        }
    }
}

// Data classes
data class AbsenceDTO(
    val id: String,
    val employeeId: String,
    val startDate: LocalDate?,
    val endDate: LocalDate?,
    val status: AbsenceStatus,
    val type: AbsenceType,
    val reason: String,
    val duration: Int,
    val fullName: String,
    val approvalDate: LocalDate?,
    val approverEmail: String?
)

data class AbsenceRequest(
    val startDate: LocalDate,
    val endDate: LocalDate,
    val type: AbsenceType,
    val reason: String?
)

data class AbsenceSubmissionResult(
    val success: Boolean,
    val id: String?,
    val error: String?
) {
    companion object {
        fun success(id: String) = AbsenceSubmissionResult(true, id, null)
        fun error(message: String) = AbsenceSubmissionResult(false, null, message)
    }
}

// Enums
enum class AbsenceStatus { APPROVED, PENDING, REJECTED, UNKNOWN }
enum class AbsenceType { VACATION, SICK_LEAVE, PERSONAL, OTHER }

// External service interfaces
interface WorkdayClient {
    fun fetchAbsencesByEmail(email: String): List<WorkdayAbsenceData>
    fun submitAbsence(request: WorkdayAbsenceRequest): WorkdayAbsenceResponse
}

// External data classes (mocked for example)
data class WorkdayAbsenceData(
    val id: String,
    val employeeId: String,
    val startDate: String?,
    val endDate: String?,
    val status: String?,
    val type: String?,
    val reason: String?,
    val firstName: String?,
    val lastName: String?
)

data class WorkdayAbsenceRequest(
    val employeeEmail: String,
    val startDate: LocalDate,
    val endDate: LocalDate,
    val type: String,
    val reason: String,
    val approverId: String?
)

data class WorkdayAbsenceResponse(
    val id: String,
    val status: String
)
```

---

## 🧪 Testing Implementation

### Complete Test Suite Example

```kotlin
package com.flip.integrations.absence

import io.micronaut.test.extensions.junit5.annotation.MicronautTest
import io.micronaut.test.annotation.MockBean
import io.micronaut.http.HttpStatus
import io.micronaut.security.authentication.Authentication
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.TestInstance
import org.mockito.Mockito.*
import org.assertj.core.api.Assertions.*
import java.time.LocalDate

@MicronautTest
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class AbsenceControllerTest {
    
    @MockBean(WorkdayClient::class)
    lateinit var workdayClient: WorkdayClient
    
    @Inject
    lateinit var controller: AbsenceController
    
    private lateinit var mockAuth: Authentication
    
    @BeforeEach
    fun setup() {
        mockAuth = mock(Authentication::class.java)
        `when`(mockAuth.attributes).thenReturn(mapOf("email" to "test@example.com"))
    }
    
    @Test
    fun `should return user absences successfully`() {
        // Given
        val email = "test@example.com"
        val mockData = listOf(
            WorkdayAbsenceData(
                id = "abs_123",
                employeeId = "emp_456",
                startDate = "2024-01-15",
                endDate = "2024-01-17",
                status = "approved",
                type = "vacation",
                reason = "Family vacation",
                firstName = "John",
                lastName = "Doe"
            )
        )
        `when`(workdayClient.fetchAbsencesByEmail(email)).thenReturn(mockData)
        
        // When
        val result = controller.getMyAbsences(mockAuth)
        
        // Then
        assertThat(result.status).isEqualTo(HttpStatus.OK)
        assertThat(result.body).isNotNull()
    }
    
    @Test
    fun `should handle service errors gracefully`() {
        // Given
        val email = "test@example.com"
        `when`(workdayClient.fetchAbsencesByEmail(email))
            .thenThrow(RuntimeException("Service unavailable"))
        
        // When
        val result = controller.getMyAbsences(mockAuth)
        
        // Then
        assertThat(result.status).isEqualTo(HttpStatus.INTERNAL_SERVER_ERROR)
    }
    
    @Test
    fun `should submit absence successfully`() {
        // Given
        val email = "test@example.com"
        val request = AbsenceRequest(
            startDate = LocalDate.of(2024, 1, 15),
            endDate = LocalDate.of(2024, 1, 17),
            type = AbsenceType.VACATION,
            reason = "Family vacation"
        )
        val mockResponse = WorkdayAbsenceResponse("abs_123", "submitted")
        `when`(workdayClient.submitAbsence(any())).thenReturn(mockResponse)
        
        // When
        val result = controller.submitAbsence(mockAuth, request)
        
        // Then
        assertThat(result.status).isEqualTo(HttpStatus.OK)
        assertThat(result.body).isNotNull()
    }
}

@MicronautTest
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class AbsenceMapperTest {
    
    @Test
    fun `should map workday data to absence DTO successfully`() {
        // Given
        val source = WorkdayAbsenceData(
            id = "abs_123",
            employeeId = "emp_456",
            startDate = "2024-01-15",
            endDate = "2024-01-17",
            status = "approved",
            type = "vacation",
            reason = "Family vacation",
            firstName = "John",
            lastName = "Doe"
        )
        
        // When
        val result = AbsenceMapper.mapToTarget(source)
        
        // Then
        assertThat(result.id).isEqualTo("abs_123")
        assertThat(result.employeeId).isEqualTo("emp_456")
        assertThat(result.startDate).isEqualTo(LocalDate.of(2024, 1, 15))
        assertThat(result.endDate).isEqualTo(LocalDate.of(2024, 1, 17))
        assertThat(result.status).isEqualTo(AbsenceStatus.APPROVED)
        assertThat(result.type).isEqualTo(AbsenceType.VACATION)
        assertThat(result.reason).isEqualTo("Family vacation")
        assertThat(result.duration).isEqualTo(3)
        assertThat(result.fullName).isEqualTo("John Doe")
    }
    
    @Test
    fun `should handle null values safely`() {
        // Given
        val source = WorkdayAbsenceData(
            id = "abs_123",
            employeeId = "emp_456",
            startDate = null,
            endDate = null,
            status = null,
            type = null,
            reason = null,
            firstName = "John",
            lastName = null
        )
        
        // When
        val result = AbsenceMapper.mapToTarget(source)
        
        // Then
        assertThat(result.startDate).isNull()
        assertThat(result.endDate).isNull()
        assertThat(result.status).isEqualTo(AbsenceStatus.UNKNOWN)
        assertThat(result.type).isEqualTo(AbsenceType.OTHER)
        assertThat(result.reason).isEqualTo("No reason provided")
        assertThat(result.duration).isEqualTo(0)
        assertThat(result.fullName).isEqualTo("John")
    }
    
    @Test
    fun `should handle unknown enum values`() {
        // Given
        val source = WorkdayAbsenceData(
            id = "abs_123",
            employeeId = "emp_456",
            startDate = "2024-01-15",
            endDate = "2024-01-17",
            status = "unknown_status",
            type = "unknown_type",
            reason = "Test reason",
            firstName = "John",
            lastName = "Doe"
        )
        
        // When
        val result = AbsenceMapper.mapToTarget(source)
        
        // Then
        assertThat(result.status).isEqualTo(AbsenceStatus.UNKNOWN)
        assertThat(result.type).isEqualTo(AbsenceType.OTHER)
    }
}
```

---

## 🔧 Common Patterns & Solutions

### 1. Date Handling
```kotlin
// Safe date parsing
private fun String.toLocalDate(): LocalDate? {
    return try {
        LocalDate.parse(this, DateTimeFormatter.ISO_LOCAL_DATE)
    } catch (ex: Exception) {
        null
    }
}

// Date calculations
private fun calculateDuration(startDate: String?, endDate: String?): Int {
    if (startDate == null || endDate == null) return 0
    return try {
        val start = startDate.toLocalDate()
        val end = endDate.toLocalDate()
        if (start != null && end != null) {
            start.until(end).days + 1
        } else 0
    } catch (ex: Exception) {
        0
    }
}
```

### 2. Enum Mapping
```kotlin
// Safe enum mapping with fallback
private fun String.toAbsenceStatus(): AbsenceStatus {
    return when (this.lowercase()) {
        "approved" -> AbsenceStatus.APPROVED
        "pending" -> AbsenceStatus.PENDING
        "rejected" -> AbsenceStatus.REJECTED
        else -> AbsenceStatus.UNKNOWN
    }
}
```

### 3. String Operations
```kotlin
// Safe string concatenation
private fun buildFullName(firstName: String?, lastName: String?): String {
    return listOfNotNull(firstName, lastName)
        .joinToString(" ")
        .trim()
        .ifEmpty { "Unknown" }
}
```

### 4. Error Handling
```kotlin
// Service error handling
fun processData(data: String): Result<ProcessedData> {
    return try {
        val processed = processDataInternal(data)
        Result.success(processed)
    } catch (ex: ValidationException) {
        log.warn("Validation failed: {}", ex.message)
        Result.failure(ex)
    } catch (ex: ExternalServiceException) {
        log.error("External service failed", ex)
        Result.failure(ServiceException("External service unavailable", ex))
    } catch (ex: Exception) {
        log.error("Unexpected error", ex)
        Result.failure(ServiceException("Processing failed", ex))
    }
}
```

---

## 📊 Quality Verification

### Code Review Checklist
- [ ] **Architecture**: Controller/Service/Mapper pattern followed
- [ ] **Security**: All endpoints have `@Secured` annotation
- [ ] **Logging**: SLF4J logger used throughout
- [ ] **Error Handling**: Try/catch in all public methods
- [ ] **Null Safety**: No `!!` operators found
- [ ] **Enum Mapping**: All `when` expressions have `else` branch
- [ ] **Unmapped Fields**: All marked with `TODO()` and explanation
- [ ] **Testing**: TDD tests cover all scenarios
- [ ] **Documentation**: Header comment with verified endpoints

### Performance Checklist
- [ ] **Lazy Loading**: Expensive operations are lazy-loaded
- [ ] **Caching**: Frequently accessed data is cached
- [ ] **Memory**: No memory leaks in data structures
- [ ] **Response Time**: Simple operations complete in <100ms

### Security Checklist
- [ ] **Authentication**: All endpoints require authentication
- [ ] **Authorization**: User can only access their own data
- [ ] **Input Validation**: All inputs are validated
- [ ] **Error Messages**: No sensitive data in error messages
- [ ] **Logging**: No sensitive data in logs

---

## 🚨 Troubleshooting

### Common Issues

#### 1. Null Pointer Exceptions
```kotlin
// ❌ Problem: Unsafe null handling
val email = source.email!!

// ✅ Solution: Safe null handling
val email = source.email ?: "unknown@example.com"
```

#### 2. Missing Error Handling
```kotlin
// ❌ Problem: No error handling
fun getData(): String = service.fetchData()

// ✅ Solution: Proper error handling
fun getData(): HttpResponse<String> = try {
    val data = service.fetchData()
    HttpResponse.ok(data)
} catch (ex: Throwable) {
    log.error("Failed to fetch data", ex)
    HttpResponse.serverError()
}
```

#### 3. Unsafe Enum Mapping
```kotlin
// ❌ Problem: Can throw exception
val status = Status.valueOf(source.status)

// ✅ Solution: Safe enum mapping
val status = when (source.status) {
    "active" -> Status.ACTIVE
    "inactive" -> Status.INACTIVE
    else -> Status.UNKNOWN
}
```

#### 4. Missing Security
```kotlin
// ❌ Problem: No security
@Get("/data")
fun getData(): String = "data"

// ✅ Solution: Proper security
@Get("/data")
@Secured(SecurityRule.IS_AUTHENTICATED)
fun getData(): HttpResponse<String> = HttpResponse.ok("data")
```

---

## 📈 Performance Optimization

### 1. Lazy Loading
```kotlin
class ExpensiveService {
    private val expensiveResource by lazy {
        createExpensiveResource()
    }
    
    fun getData(): String {
        return expensiveResource.process()
    }
}
```

### 2. Caching
```kotlin
@Singleton
class CachedService {
    private val cache = ConcurrentHashMap<String, Any>()
    
    fun getCachedData(key: String): Any {
        return cache.computeIfAbsent(key) { fetchData(key) }
    }
}
```

### 3. Memory Management
```kotlin
// Use appropriate data structures
private val smallMap = HashMap<String, String>()  // For small collections
private val largeMap = ConcurrentHashMap<String, Any>()  // For large collections
```

---

## 🔄 Integration with MCP Tools

### Phase 3 Workflow
```bash
# 1. Generate code
phase3_generate_mapper(
    mapping_report_path="/path/to/mapping_report.md",
    output_directory="/path/to/outputs/phase3"
)

# 2. Quality audit
phase3_quality_suite(
    kotlin_file_path="/path/to/generated_mapper.kt",
    mapping_report_path="/path/to/mapping_report.md"
)

# 3. TDD validation
phase4_tdd_validation(
    kotlin_file_path="/path/to/generated_mapper.kt",
    mapping_report_path="/path/to/mapping_report.md"
)
```

### Expected Outputs
- **Generated Code**: Complete Kotlin file with Controller/Service/Mapper
- **Quality Report**: JSON report with violations and suggestions
- **Test Suite**: Comprehensive TDD test file
- **Validation Report**: TDD validation results and prompts

---

## 🎯 Success Criteria

### Code Quality
- ✅ All tests passing (100% coverage for mappers)
- ✅ No security vulnerabilities
- ✅ No null pointer exceptions
- ✅ All endpoints properly secured
- ✅ Comprehensive error handling

### Performance
- ✅ Response time <100ms for simple operations
- ✅ Memory usage <50MB per request
- ✅ Error rate <1% in production

### Maintainability
- ✅ Code follows KISS principles
- ✅ Single responsibility per class
- ✅ Clear separation of concerns
- ✅ Comprehensive documentation
- ✅ Easy to test and modify

---

*This implementation guide ensures production-ready Kotlin code that follows all Phase 3 coding rules and provides excellent developer experience.*