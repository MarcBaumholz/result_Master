# Enhanced Field Analysis

**Generated:** 2025-09-19 08:44:38
**Fields:** shift, schedule, time, employee, work, planning, roster, assignment, shift_plan, work_schedule
**Collection:** stackone_shift_planning
**Context Topic:** shift_planning

## Analysis Results

### Field Analysis for Shift Planning API

#### **shift**
1. **Semantic Description**: Represents a scheduled work period for an employee, typically defined by start/end times and associated details. Used to organize and track employee working hours within a scheduling system.
2. **Synonyms**: Work shift, duty period, rotation
3. **Possible Datatypes**: object, string (enum: full_time, shifts, part_time), Reference
4. **Business Context**: Core component for workforce management, used in scheduling, payroll calculation, and attendance tracking. Determines employee availability and coverage requirements.
5. **API Mapping Hints**: Map to EmploymentScheduleTypeEnum for schedule types; use Reference type when linking to specific shift instances; include source_value for provider-specific data.

#### **schedule**
1. **Semantic Description**: Defines time-off policies and arrangements, including leave types, durations, and approval workflows. Manages employee absence planning and coverage.
2. **Synonyms**: Time-off plan, leave schedule, absence calendar
3. **Possible Datatypes**: object, string (TimeOffTypeEnum), policy configuration
4. **Business Context**: Essential for HR management, compliance tracking, and workforce planning. Used to manage paid time off, sick leave, and other absence types.
5. **API Mapping Hints**: Use TimeOff schema for time-off instances; map to TimeOffTypeEnum for classification; include policy metadata (name, description, type) for comprehensive management.

#### **time**
1. **Semantic Description**: Tracks actual worked hours through time entries, including clock-in/out times, breaks, and status updates. Provides precise recording of employee labor.
2. **Synonyms**: Time tracking, hours log, attendance record
3. **Possible Datatypes**: object, string (status enum: approved, unmapped_value), number (hours)
4. **Business Context**: Critical for payroll processing, compliance reporting, and productivity analysis. Ensures accurate compensation and labor law compliance.
5. **API Mapping Hints**: Use TimeEntries schema for detailed records; map status to TimeEntryStatusEnum; include ISO 8601 duration format for time_worked.

#### **employee**
1. **Semantic Description**: Represents an individual worker with employment details, including job information, compensation, and contract terms. Central entity in workforce management.
2. **Synonyms**: Staff member, worker, personnel
3. **Possible Datatypes**: object, string (ID), employment type enum
4. **Business Context**: Foundation for all HR operations, including onboarding, payroll, performance management, and compliance reporting.
5. **API Mapping Hints**: Use Employee schema with comprehensive employment data; map employment_type to appropriate enum values; include unified_custom_fields for extensibility.

#### **work**
1. **Semantic Description**: Defines work eligibility and employment terms, including contract types, work schedules, and compensation structures. Determines legal working conditions.
2. **Synonyms**: Employment terms, work arrangement, labor conditions
3. **Possible Datatypes**: object, string (enum values), configuration object
4. **Business Context**: Governs employee classification, legal compliance, and benefit eligibility. Used for contract management and regulatory reporting.
5. **API Mapping Hints**: Map to WorkEligibilityTypeEnum; use HrisCreateEmploymentRequestDto pattern for creation; include pay_currency and effective_date for financial tracking.

#### **planning**
1. **Semantic Description**: Facilitates workforce planning operations through API references and content management. Supports scheduling and resource allocation processes.
2. **Synonyms**: Resource planning, capacity planning, scheduling setup
3. **Possible Datatypes**: object, Reference, Content
4. **Business Context**: Used for strategic workforce allocation, shift optimization, and operational planning. Supports both immediate and long-term scheduling needs.
5. **API Mapping Hints**: Use Reference type for linking planning elements; include required header parameters (x-account-id) for authentication; map to appropriate endpoint parameters.

#### **roster**
1. **Semantic Description**: Manages team compositions and employee groupings for scheduling purposes. Organizes workers into functional units for shift assignment.
2. **Synonyms**: Team list, crew assignment, staff grouping
3. **Possible Datatypes**: object, TeamTypeEnum, Employee collection
4. **Business Context**: Essential for team-based scheduling, coverage planning, and department management. Supports both permanent and ad-hoc team formations.
5. **API Mapping Hints**: Use TeamTypeEnum for classification; map to Employee schema for member details; follow work_eligibility endpoint pattern for updates.

#### **assignment**
1. **Semantic Description**: Allocates specific shifts or duties to employees, creating concrete work assignments. Connects workers to scheduled activities.
2. **Synonyms**: Duty allocation, shift assignment, task delegation
3. **Possible Datatypes**: object, Reference, TypeEnum
4. **Business Context**: Critical for operational execution, ensuring adequate coverage and proper task distribution. Used in daily scheduling and emergency planning.
5. **API Mapping Hints**: Use Reference type for assignment linking; map to appropriate TypeEnum for classification; include required path parameters for specific operations.

#### **shift_plan**
1. **Semantic Description**: Defines comprehensive shift patterns and scheduling templates for recurring work arrangements. Provides blueprint for shift organization.
2. **Synonyms**: Shift pattern, rotation schedule, template plan
3. **Possible Datatypes**: object, Reference, ContractTypeApiModel
4. **Business Context**: Used for standardized scheduling, pattern-based planning, and consistent shift management across periods.
5. **API Mapping Hints**: Map to EmploymentScheduleTypeEnum for schedule types; use ContractTypeApiModel for detailed contract terms; include source_value for provider compatibility.

#### **work_schedule**
1. **Semantic Description**: Defines regular working patterns and eligibility criteria for employees. Establishes standard working hours and conditions.
2. **Synonyms**: Regular schedule, working pattern, standard hours
3. **Possible Datatypes**: object, WorkEligibility, WorkEligibilityTypeEnum
4. **Business Context**: Foundation for consistent scheduling, overtime calculation, and compliance with working time regulations.
5. **API Mapping Hints**: Use TimeEntries schema for detailed scheduling; include hours_worked and break_duration for precise tracking; map status appropriately for approval workflows.

### General API Implementation Recommendations:
- Use enum types consistently for standardized values
- Include both remote_id and id fields for provider compatibility
- Implement created_at/updated_at timestamps for audit trails
- Use unified_custom_fields for extensible custom data
- Follow ISO 8601 format for all time-related data
- Include passthrough objects for provider-specific requirements

## Context Sources

### shift Sources:
1. Score: 0.663 | Query: shift property schema type
2. Score: 0.654 | Query: shift property schema type
3. Score: 0.490 | Query: shift attribute meaning usage

### schedule Sources:
1. Score: 0.690 | Query: schedule property schema type
2. Score: 0.684 | Query: schedule property schema type
3. Score: 0.552 | Query: schedule attribute meaning usage

### time Sources:
1. Score: 0.872 | Query: time property schema type
2. Score: 0.843 | Query: time property schema type
3. Score: 0.662 | Query: time field description validation

### employee Sources:
1. Score: 0.893 | Query: employee property schema type
2. Score: 0.794 | Query: employee property schema type
3. Score: 0.709 | Query: employee attribute meaning usage

### work Sources:
1. Score: 0.825 | Query: work property schema type
2. Score: 0.823 | Query: work property schema type
3. Score: 0.655 | Query: work attribute meaning usage

### planning Sources:
1. Score: 0.617 | Query: planning property schema type
2. Score: 0.602 | Query: planning property schema type
3. Score: 0.509 | Query: planning parameter definition

### roster Sources:
1. Score: 0.726 | Query: roster property schema type
2. Score: 0.653 | Query: roster property schema type
3. Score: 0.581 | Query: roster parameter definition

### assignment Sources:
1. Score: 0.679 | Query: assignment property schema type
2. Score: 0.671 | Query: assignment property schema type
3. Score: 0.485 | Query: assignment parameter definition

### shift_plan Sources:
1. Score: 0.603 | Query: shift_plan property schema type
2. Score: 0.579 | Query: shift_plan property schema type
3. Score: 0.550 | Query: shift_plan attribute meaning usage

### work_schedule Sources:
1. Score: 0.700 | Query: work_schedule property schema type
2. Score: 0.694 | Query: work_schedule property schema type
3. Score: 0.642 | Query: work_schedule attribute meaning usage

