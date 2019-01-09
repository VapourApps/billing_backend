# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from silver.models import Plan
from webhooks import VAHook

class CompanyPage(models.Model):
    company_name = models.CharField(max_length = 100)

    def __unicode__(self):
        return self.company_name

class CompanyPageLanding(models.Model):
    company_page = models.ForeignKey(CompanyPage, on_delete = models.CASCADE, default = None)
    header_logo = models.URLField(max_length = 300)
    landing_header = models.CharField(max_length = 600)
    landing_text = models.CharField(max_length = 600)
    landing_image = models.URLField(max_length = 600)
    footer_logo = models.URLField(max_length = 600)
    footer_text = models.CharField(max_length = 600)

    footer_facebook = models.URLField(max_length = 600)
    footer_twitter = models.URLField(max_length = 600)
    footer_youtube = models.URLField(max_length = 600)
    footer_instagram = models.URLField(max_length = 600)

    def __unicode__(self):
        return 'Landing page for ' + self.company_page.company_name


class CompanyPageAbout(models.Model):
    company_page = models.ForeignKey(CompanyPage, on_delete = models.CASCADE, default = None)
    features_header = models.CharField(max_length = 500)
    features_text = models.CharField(max_length = 500)
    features_image = models.URLField(max_length = 500)

    def __unicode__(self):
        return 'About page for ' + self.company_page.company_name

class CompanyPageAboutSteps(models.Model):
    step_header = models.CharField(max_length = 500)
    step_details = models.CharField(max_length = 500)
    
    belongs_to_page = models.ForeignKey(CompanyPageAbout, on_delete = models.CASCADE, default = None)

    def __unicode__(self):
        return 'Steps for the ' + self.belongs_to_page.__unicode__()

class CompanyPageFeaturesList(models.Model):
    company_page = models.ForeignKey(CompanyPage, on_delete = models.CASCADE, default = None)

    def __unicode__(self):
        return 'Features for ' + self.company_page.company_name

class CompanyPageFeature(models.Model):
    feature_image = models.ImageField(max_length = 500)
    feature_header = models.CharField(max_length = 500)
    feature_details = models.CharField(max_length = 500)
    feature_header_short_len = 10

    belongs_to_list = models.ForeignKey(CompanyPageFeaturesList, on_delete = models.CASCADE, default = None)

    def shorten_header(self):
        if len(self.feature_header) > self.feature_header_short_len + 3:
            return self.feature_header[:self.feature_header_short_len] + '...'
        return self.feature_header

    def __unicode__(self):
        return 'Feature in ' + self.belongs_to_list.company_page.company_name + '(%s)' % self.shorten_header()

class CompanyPagePricing(models.Model):
    company_page = models.ForeignKey(CompanyPage, on_delete = models.CASCADE, default = None)
    pricing_header = models.CharField(max_length = 500)
    pricing_details = models.CharField(max_length = 500)

    def __unicode__(self):
        return 'Pricing for ' + self.company_page.company_name

class CompanyPageSignup(models.Model):
    company_page = models.ForeignKey(CompanyPage, on_delete = models.CASCADE, default = None)
    terms_text = models.CharField(max_length = 500)

    def __unicode__(self):
        return 'Signup page for ' + self.company_page.company_name

class CompanyPageLoggedIn(models.Model):
    company_page = models.ForeignKey(CompanyPage, on_delete = models.CASCADE, default = None)

    footer_text = models.CharField(max_length = 500)
    support_email = models.CharField(max_length = 500)

    def __unicode__(self):
        return 'Login page for ', self.company_page.company_name
