# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import PlanFeatures, StepField, UserCustomerMapping, MappingType, PlanStep

class PlanFeaturesAdmin(admin.ModelAdmin):
    model = PlanFeatures

class StepFieldAdmin(admin.ModelAdmin): 
    model = StepField

class MappingTypeAdmin(admin.ModelAdmin):
    model = MappingType

class UserCustomerMappingAdmin(admin.ModelAdmin):
    model = UserCustomerMapping

class PlanStepAdmin(admin.ModelAdmin):
    model = PlanStep

admin.site.register(PlanFeatures, PlanFeaturesAdmin)
admin.site.register(StepField, StepFieldAdmin)
admin.site.register(UserCustomerMapping, UserCustomerMappingAdmin)
admin.site.register(MappingType, MappingTypeAdmin)
admin.site.register(PlanStep, PlanStepAdmin)
