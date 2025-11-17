package com.getflip.absences.stackone.controllers.mappers

import com.getflip.absences.stackone.hris.absence.management.models.AbsenceCreation
import com.stackone.stackone_client_java.models.components.HrisCreateTimeOffRequestDto
import jakarta.inject.Singleton
import java.time.format.DateTimeFormatter

@Singleton
class AbsenceCreationToCreateTimeOffRequest(
    private val typeMapper: TimeOffTypeEnumToAbsenceTypeMapper
) {
    fun map(source: AbsenceCreation): HrisCreateTimeOffRequestDto {
        val fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSS")
        val startIso = source.startDate?.atStartOfDay()?.format(fmt)
            ?: error("start_date is required")
        val endIso = source.endDate?.atStartOfDay()?.format(fmt)
            ?: error("end_date is required")

        val builder = HrisCreateTimeOffRequestDto.builder()
            .timeOffPolicyId(source.absenceTypeExternalId ?: error("absence_type_external_id is required"))
            .startDate(startIso)
            .endDate(endIso)

        // ✅ MAP TYPE FROM EMPLOYEE NOTE
        val mappedType = typeMapper.mapFromEmployeeNote(source.employeeNote)
        builder.type(mappedType)

        // ✅ BUILD PASSTHROUGH DATA WITH ALL FIELDS
        val passthroughData = mutableMapOf<String, Any>()
        
        // ✅ FIX: Map employee note to "comment" instead of "notes"
        source.employeeNote?.let { passthroughData["comment"] = it }
        
        // Add status
        source.status?.let { status ->
            val statusValue = when (status.value) {
                "REQUESTED" -> "pending"
                "APPROVED" -> "approved"
                else -> "pending"
            }
            passthroughData["status"] = statusValue
        }
        
        // ✅ ADD UNIT AND AMOUNT TO PASSTHROUGH
        source.unit?.let { passthroughData["unit"] = it }
        source.amount?.let { passthroughData["amount"] = it }
        
        // ✅ ADD HALF DAY INFO TO PASSTHROUGH (as workaround)
        //source.startHalfDay?.let { passthroughData["start_half_day"] = it }
        //source.endHalfDay?.let { passthroughData["end_half_day"] = it }
        
        // ❌ REMOVED - These lines were causing compilation errors due to private field access
        // passthroughData["mapped_type"] = mappedType.value?.name
        // passthroughData["mapped_source_value"] = mappedType.sourceValue?.toString()
        
        // Set passthrough data
        if (passthroughData.isNotEmpty()) {
            builder.passthrough(passthroughData)
        }

        return builder.build()
    }
}