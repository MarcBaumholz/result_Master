package com.getflip.absences.stackone.controllers

import com.getflip.absences.stackone.hris.absence.management.models.Absence
import com.getflip.absences.stackone.controllers.dto.AbsenceCreationRequest
import com.getflip.absences.stackone.hris.absence.management.models.Absences
import com.getflip.absences.stackone.services.AbsenceService
import io.micronaut.http.MediaType
import io.micronaut.http.annotation.Body
import io.micronaut.http.annotation.Controller
import io.micronaut.http.annotation.Get
import io.micronaut.http.annotation.Post
import io.micronaut.http.annotation.Produces
import io.micronaut.security.authentication.Authentication
import io.micronaut.security.rules.SecurityRule
import io.micronaut.security.annotation.Secured

@Secured(SecurityRule.IS_AUTHENTICATED)
@Controller("/api/hris/v4/absences")
class AbsenceController(
    private val absenceService: AbsenceService,
) {
    @Get
    @Produces(MediaType.APPLICATION_JSON)
    fun list(authentication: Authentication): Absences =
        absenceService.list(authentication)

    @Post
    @Produces(MediaType.APPLICATION_JSON)
    fun create(authentication: Authentication, @Body request: AbsenceCreationRequest): Absence =
        absenceService.create(authentication, request)
}


