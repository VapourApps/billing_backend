# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import PlanFeatures, PlanSteps, UserCustomerMapping

class PlanFeaturesAdmin(admin.ModelAdmin):
    model = PlanFeatures

class PlanStepsAdmin(admin.ModelAdmin): 
    model = PlanSteps

class UserCustomerMappingAdmin(admin.ModelAdmin):
    model = UserCustomerMapping


admin.site.register(PlanFeatures, PlanFeaturesAdmin)
admin.site.register(PlanSteps, PlanStepsAdmin)
admin.site.register(UserCustomerMapping, UserCustomerMappingAdmin)

