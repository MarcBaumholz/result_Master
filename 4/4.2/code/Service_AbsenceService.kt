package com.getflip.absences.stackone.services

import com.getflip.absences.stackone.clients.stackone.employees.StackOneEmployeesFacade
import com.getflip.absences.stackone.controllers.mappers.AbsenceCreationToCreateTimeOffRequest
import com.getflip.absences.stackone.hris.absence.management.models.AbsenceDuration
import com.getflip.absences.stackone.hris.absence.management.models.AbsenceDurationUnit
import com.getflip.absences.stackone.hris.absence.management.models.AbsenceStatus
import com.getflip.absences.stackone.hris.absence.management.models.AbsenceType
import com.getflip.absences.stackone.hris.absence.management.models.Absence
import com.getflip.absences.stackone.controllers.dto.AbsenceCreationRequest
import com.getflip.absences.stackone.hris.absence.management.models.AbsenceCreation
import com.getflip.absences.stackone.hris.absence.management.models.Absences
import com.stackone.stackone_client_java.models.components.TimeOff
import io.micronaut.serde.annotation.SerdeImport
import io.micronaut.security.authentication.Authentication
import jakarta.inject.Singleton
import org.slf4j.LoggerFactory

@SerdeImport(Absence::class)
@SerdeImport(Absences::class)
@SerdeImport(AbsenceCreation::class)
@SerdeImport(com.getflip.absences.stackone.hris.absence.management.models.AbsenceDuration::class)
@SerdeImport(com.getflip.absences.stackone.hris.absence.management.models.AbsenceType::class)
@SerdeImport(com.getflip.absences.stackone.hris.absence.management.models.AbsenceStatus::class)
@Singleton
class AbsenceService(
    private val employeesFacade: StackOneEmployeesFacade,
    private val toCreateMapper: AbsenceCreationToCreateTimeOffRequest,
) {
    private val logger = LoggerFactory.getLogger(AbsenceService::class.java)

    fun list(authentication: Authentication): Absences {
        val email = authentication.attributes["email"].toString()
        val employee = employeesFacade.getEmployeeByEmail(email)
            ?: error("No employee found for email: $email")

        val employeeId = employee.id().get()
        val timeOffs: List<TimeOff> = employeesFacade.getEmployeeAbsences(employeeId)
        val items = timeOffs.mapNotNull { null }
        logger.info("Fetched {} absences for {}", items.size, email)
        return Absences(absences = items, pagination = null)
    }

    fun create(authentication: Authentication, request: AbsenceCreationRequest): Absence {
        val email = authentication.attributes["email"].toString()
        val employee = employeesFacade.getEmployeeByEmail(email)
            ?: error("No employee found for email: $email")

        val employeeId = employee.id().get()
        val dto = toCreateMapper.map(request.toModel())
        val created = employeesFacade.createAbsence(employeeId, dto)
        logger.info("Created absence for {} with status {}", email, created.statusCode())
        return mapCreationToAbsence(request.toModel())
    }

    private fun mapCreationToAbsence(source: AbsenceCreation): Absence {
        val duration = AbsenceDuration(
            amount = source.amount ?: 0.0,
            unit = AbsenceDurationUnit.DAYS,
        )

        val mappedStatus = when (source.status?.value) {
            "REQUESTED" -> AbsenceStatus.Mapped.PENDING
            "APPROVED" -> AbsenceStatus.Mapped.APPROVED
            else -> AbsenceStatus.Mapped.UNKNOWN
        }
        val status = AbsenceStatus(
            raw = source.status?.value ?: "UNKNOWN",
            mapped = mappedStatus,
        )

        val type = AbsenceType(
            externalId = source.absenceTypeExternalId ?: "",
            name = "",
            unit = AbsenceDurationUnit.DAYS,
            halfDaysSupported = true,
            exactTimesSupported = false,
        )

        val now = java.time.OffsetDateTime.now()
        return Absence(
            externalId = "",
            startDate = source.startDate ?: error("start_date missing"),
            endDate = source.endDate ?: error("end_date missing"),
            startHalfDay = source.startHalfDay ?: false,
            endHalfDay = source.endHalfDay ?: false,
            duration = duration,
            status = status,
            isCancellable = false,
            isDeletable = false,
            type = type,
            createdAt = now,
            updatedAt = now,
            approverExternalId = null,
            startTime = null,
            endTime = null,
            requestorComment = source.employeeNote,
        )
    }
}


