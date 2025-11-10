# Enhanced Field Analysis

**Generated:** 2025-09-30 11:03:09
**Fields:** body.input.data.employee_id, body.input.data.status, body.input.data.start_date, body.input.data.end_date, body.input.data.start_half_day, body.input.data.end_half_day, body.input.data.absence_type_external_id, body.input.data.employee_note, body.input.data.amount, body.input.data.unit, headers.x-account-id
**Collection:** stackone_api_v2
**Context Topic:** Stackone HRIS time off integration for absence management

## Analysis Results

### Field Analysis for Stackone HRIS Time Off Integration

#### **body.input.data.employee_id**
1. **Semantic Description**: Uniquely identifies the employee for whom the time off request is being created. Essential for linking absence data to the correct individual in the HR system.
2. **Synonyms**: user_id, staff_id, personnel_id
3. **Possible Datatypes**: string, integer, UUID
4. **Business Context**: Used in employee management workflows to ensure time off allocations, approvals, and reporting are accurately assigned. Critical for payroll and compliance tracking.
5. **API Mapping Hints**: Map to `id` in path parameters for employee-specific endpoints (e.g., `/employees/{id}/time_off`). Ensure consistency with other employee-related API calls.

#### **body.input.data.status**
1. **Semantic Description**: Indicates the current state of the time off request (e.g., pending, approved, denied). Drives workflow transitions and notifications.
2. **Synonyms**: state, request_status, approval_status
3. **Possible Datatypes**: string, enum, integer (coded values)
4. **Business Context**: Key for approval workflows, reporting on absence trends, and integrating with calendar/notification systems. Affects payroll processing if linked to paid time off.
5. **API Mapping Hints**: Align with standard HTTP status codes (e.g., 201 for created) in responses. Use consistent values across `GET`/`POST` operations to avoid mismatches.

#### **body.input.data.start_date**
1. **Semantic Description**: Defines the beginning date of the time off period. Fundamental for calculating duration and validating against policies.
2. **Synonyms**: from_date, begin_date, absence_start
3. **Possible Datatypes**: string (ISO 8601 date), timestamp, date object
4. **Business Context**: Used in conflict detection (overlapping requests), accrual calculations, and calendar visibility. Impacts resource planning and coverage.
5. **API Mapping Hints**: Format as YYYY-MM-DD to match ISO standards. Validate against `end_date` to ensure logical ranges.

#### **body.input.data.end_date**
1. **Semantic Description**: Specifies the conclusion date of the time off period. Works with `start_date` to determine total absence duration.
2. **Synonyms**: to_date, end_date, absence_end
3. **Possible Datatypes**: string (ISO 8601 date), timestamp, date object
4. **Business Context**: Critical for duration calculations, policy enforcement (e.g., max consecutive days), and return-to-work scheduling.
5. **API Mapping Hints**: Ensure it is chronologically after `start_date`. Use same format as `start_date` for consistency.

#### **body.input.data.start_half_day**
1. **Semantic Description**: Flags whether the time off starts at a half-day (e.g., morning or afternoon). Refines accuracy for partial-day absences.
2. **Synonyms**: half_day_start, is_half_day_begin, partial_start
3. **Possible Datatypes**: boolean, string (e.g., "AM"/"PM"), integer (0/1)
4. **Business Context**: Allows precise tracking for partial absences, affecting accrual deductions and team coverage for half days.
5. **API Mapping Hints**: Map to boolean (true/false) or enum ("am", "pm") based on system support. Combine with `start_date` for full context.

#### **body.input.data.end_half_day**
1. **Semantic Description**: Indicates if the time off ends at a half-day. Complements `start_half_day` for partial-day precision.
2. **Synonyms**: half_day_end, is_half_day_finish, partial_end
3. **Possible Datatypes**: boolean, string (e.g., "AM"/"PM"), integer (0/1)
4. **Business Context**: Ensures accurate calculation of absence hours/days, especially for multi-day requests spanning partial days.
5. **API Mapping Hints**: Treat symmetrically with `start_half_day`. Use consistent data types across both fields.

#### **body.input.data.absence_type_external_id**
1. **Semantic Description**: External identifier for the absence category (e.g., vacation, sick leave). Links to predefined policy types.
2. **Synonyms**: leave_type_id, category_id, policy_code
3. **Possible Datatypes**: string, integer, UUID
4. **Business Context**: Determines policy rules (e.g., paid/unpaid, accrual rates), reporting categories, and compliance requirements (e.g., FMLA).
5. **API Mapping Hints**: Map to system-specific absence type codes. Ensure it matches values from `GET /time_off` responses to maintain consistency.

#### **body.input.data.employee_note**
1. **Semantic Description**: Optional comments from the employee providing context for the request (e.g., reason for leave). Supports approval decisions.
2. **Synonyms**: comments, reason, notes
3. **Possible Datatypes**: string, text
4. **Business Context**: Aids managers in evaluating requests, auditing, and employee communication. May be used in dispute resolution or pattern analysis.
5. **API Mapping Hints**: Truncate or sanitize long text to avoid API payload issues. Include in POST payloads for clarity.

#### **body.input.data.amount**
1. **Semantic Description**: Numeric value representing the quantity of time off, interpreted with `unit` (e.g., 2 days, 4 hours).
2. **Synonyms**: quantity, duration, value
3. **Possible Datatypes**: number, float, integer
4. **Business Context**: Core for deducting from balances, calculating pay, and enforcing policy limits (e.g., max days per year).
5. **API Mapping Hints**: Always pair with `unit` field. Validate against policy rules (e.g., negative values invalid).

#### **body.input.data.unit**
1. **Semantic Description**: Specifies the time unit for `amount` (e.g., "hours", "days"). Essential for interpreting the absence duration.
2. **Synonyms**: duration_unit, time_unit, measure
3. **Possible Datatypes**: string, enum
4. **Business Context**: Ensures correct accrual calculations and alignment with payroll systems (e.g., hourly vs. daily rates).
5. **API Mapping Hints**: Use consistent enum values (e.g., "hours", "days"). Default to "days" if not specified, but encourage explicit values.

#### **headers.x-account-id**
1. **Semantic Description**: Authentication header identifying the tenant or account context. Ensures data isolation and security.
2. **Synonyms**: tenant_id, account_code, client_id
3. **Possible Datatypes**: string, UUID
4. **Business Context**: Mandatory for multi-tenant systems to route requests to correct HRIS instances and enforce access controls.
5. **API Mapping Hints**: Include in every request header. Validate format (e.g., UUID) to avoid 400 errors. Map from integration settings.

## Context Sources

### body.input.data.employee_id Sources:
1. Score: 0.807 | Query: Stackone HRIS time off integration for absence management body.input.data.employee_id
2. Score: 0.796 | Query: Stackone HRIS time off integration for absence management body.input.data.employee_id
3. Score: 0.756 | Query: body.input.data.employee_id parameter definition

### body.input.data.status Sources:
1. Score: 0.768 | Query: Stackone HRIS time off integration for absence management body.input.data.status
2. Score: 0.762 | Query: Stackone HRIS time off integration for absence management body.input.data.status
3. Score: 0.652 | Query: body.input.data.status property schema type

### body.input.data.start_date Sources:
1. Score: 0.775 | Query: Stackone HRIS time off integration for absence management body.input.data.start_date
2. Score: 0.774 | Query: Stackone HRIS time off integration for absence management body.input.data.start_date
3. Score: 0.583 | Query: body.input.data.start_date property schema type

### body.input.data.end_date Sources:
1. Score: 0.774 | Query: Stackone HRIS time off integration for absence management body.input.data.end_date
2. Score: 0.761 | Query: Stackone HRIS time off integration for absence management body.input.data.end_date
3. Score: 0.578 | Query: body.input.data.end_date property schema type

### body.input.data.start_half_day Sources:
1. Score: 0.759 | Query: Stackone HRIS time off integration for absence management body.input.data.start_half_day
2. Score: 0.755 | Query: Stackone HRIS time off integration for absence management body.input.data.start_half_day
3. Score: 0.571 | Query: body.input.data.start_half_day property schema type

### body.input.data.end_half_day Sources:
1. Score: 0.764 | Query: Stackone HRIS time off integration for absence management body.input.data.end_half_day
2. Score: 0.757 | Query: Stackone HRIS time off integration for absence management body.input.data.end_half_day
3. Score: 0.580 | Query: body.input.data.end_half_day property schema type

### body.input.data.absence_type_external_id Sources:
1. Score: 0.764 | Query: Stackone HRIS time off integration for absence management body.input.data.absence_type_external_id
2. Score: 0.657 | Query: Stackone HRIS time off integration for absence management body.input.data.absence_type_external_id
3. Score: 0.569 | Query: body.input.data.absence_type_external_id parameter definition

### body.input.data.employee_note Sources:
1. Score: 0.777 | Query: Stackone HRIS time off integration for absence management body.input.data.employee_note
2. Score: 0.755 | Query: Stackone HRIS time off integration for absence management body.input.data.employee_note
3. Score: 0.650 | Query: body.input.data.employee_note parameter definition

### body.input.data.amount Sources:
1. Score: 0.731 | Query: Stackone HRIS time off integration for absence management body.input.data.amount
2. Score: 0.726 | Query: Stackone HRIS time off integration for absence management body.input.data.amount
3. Score: 0.528 | Query: body.input.data.amount property schema type

### body.input.data.unit Sources:
1. Score: 0.724 | Query: Stackone HRIS time off integration for absence management body.input.data.unit
2. Score: 0.723 | Query: Stackone HRIS time off integration for absence management body.input.data.unit
3. Score: 0.564 | Query: body.input.data.unit property schema type

### headers.x-account-id Sources:
1. Score: 0.761 | Query: Stackone HRIS time off integration for absence management headers.x-account-id
2. Score: 0.759 | Query: headers.x-account-id parameter definition
3. Score: 0.732 | Query: headers.x-account-id parameter definition

