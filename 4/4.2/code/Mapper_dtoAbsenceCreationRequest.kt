package com.getflip.absences.stackone.controllers.dto

import com.getflip.absences.stackone.hris.absence.management.models.AbsenceCreation
import io.micronaut.serde.annotation.Serdeable
import java.time.LocalDate

@Serdeable
data class AbsenceCreationRequest(
    val absence_type_external_id: String?,
    val start_date: LocalDate?,
    val end_date: LocalDate?,
    val start_half_day: Boolean?,
    val end_half_day: Boolean?,
    val status: String?,
    val employee_note: String?,
    val amount: Double?,  // ✅ ADD THIS
    val unit: String?,   // ✅ ADD THIS
) {
    fun toModel(): AbsenceCreation = AbsenceCreation(
        employeeExternalId = null,
        absenceTypeExternalId = absence_type_external_id,
        status = when (status) {
            "REQUESTED" -> AbsenceCreation.Status.REQUESTED
            "APPROVED" -> AbsenceCreation.Status.APPROVED
            else -> null
        },
        startDate = start_date,
        endDate = end_date,
        startHalfDay = start_half_day,
        endHalfDay = end_half_day,
        amount = amount,  // ✅ USE ACTUAL VALUE
        unit = unit?.let { AbsenceCreation.Unit.valueOf(it) },      // ✅ USE ACTUAL VALUE
        employeeNote = employee_note,
    )
}