# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import CompanyPage, CompanyPageLanding, CompanyPageAbout, CompanyPageAboutSteps, CompanyPageFeaturesList, CompanyPagePricing, CompanyPageSignup, CompanyPageLoggedIn, CompanyPageFeature

from .webhooks import VAHook

class CompanyPageAdmin(admin.ModelAdmin):
    model = CompanyPage

class CompanyPageLandingAdmin(admin.ModelAdmin):
    model = CompanyPageLanding
    fk_name = 'company_landing_page'
    list_filter = ('company_page__company_name', )
    list_display = ('company_page', )
#    list_display = [field.name for field in CompanyPageLanding._meta.get_fields()]

class CompanyPageAboutAdmin(admin.ModelAdmin):
    model = CompanyPageAbout
    fk_name = 'company_about_page'
    list_filter = ('company_page__company_name', )
    list_display = ('company_page', )

class CompanyPageAboutStepsAdmin(admin.ModelAdmin):
    model = CompanyPageAboutSteps
    fk_name = 'company_about_steps'
    list_filter = ('belongs_to_page__company_page__company_name', )
    list_display = ('belongs_to_page', )


class CompanyPageFeaturesAdmin(admin.ModelAdmin):
    model = CompanyPageFeature
    fk_name = 'company_page_features'
    list_filter = ('belongs_to_list__company_page__company_name', )
    list_display = ('belongs_to_list', 'feature_header', )


class CompanyPageFeaturesListAdmin(admin.ModelAdmin):
    model = CompanyPageFeaturesList
    fk_name = 'company_page_features_list'
    list_filter = ('company_page__company_name', )
    list_display = ('company_page', )


class CompanyPagePricingAdmin(admin.ModelAdmin):
    model = CompanyPagePricing
    fk_name = 'company_page_pricing'
    list_filter = ('company_page__company_name', )
    list_display = ('company_page', 'pricing_header', )


class CompanyPageSignupAdmin(admin.ModelAdmin):
    model = CompanyPageSignup
    fk_name = 'company_page_signup'
    list_filter = ('company_page__company_name', )
    list_display = ('company_page', )


class CompanyPageLoggedInAdmin(admin.ModelAdmin):
    model = CompanyPageLoggedIn
    fk_name = 'company_page_logged_in'
    list_filter = ('company_page__company_name', )
    list_display = ('company_page', 'support_email', )

class VAHookAdmin(admin.ModelAdmin):
    model = VAHook


admin.site.register(CompanyPage, CompanyPageAdmin)
admin.site.register(CompanyPageLanding, CompanyPageLandingAdmin)
admin.site.register(CompanyPageAbout, CompanyPageAboutAdmin)
admin.site.register(CompanyPageFeaturesList, CompanyPageFeaturesListAdmin)
admin.site.register(CompanyPageFeature, CompanyPageFeaturesAdmin)
admin.site.register(CompanyPagePricing, CompanyPagePricingAdmin)
admin.site.register(CompanyPageSignup, CompanyPageSignupAdmin)
admin.site.register(CompanyPageLoggedIn, CompanyPageLoggedInAdmin)
admin.site.register(CompanyPageAboutSteps, CompanyPageAboutStepsAdmin)
admin.site.register(VAHook, VAHookAdmin)
