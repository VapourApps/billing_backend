# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from silver.models import Plan, Customer

class PlanFeatures(models.Model):
    plan_image = models.ImageField()
    plan_description = models.CharField(max_length = 200)
    plan = models.ForeignKey(Plan, on_delete = models.CASCADE, default = None)

    def __unicode__(self):
        return 'Feature for ' + self.plan.__str__()

    def __str__(self):
        return self.__unicode__()

    class Meta: 
        verbose_name_plural = 'Plan Features'


class PlanStep(models.Model):
    name = models.CharField(max_length = 20)
    belongs_to = models.ForeignKey(PlanFeatures, on_delete = models.CASCADE)

    def __unicode__(self):
        return self.name

    def __str__(self): 
        return self.__unicode__()

    class Meta: 
        verbose_name_plural = 'Plan Steps'

class StepField(models.Model):
    input_type = models.CharField(max_length = 20)
    value = models.CharField(max_length = 50, blank = True)
    name = models.CharField(max_length = 30)
    belongs_to = models.ForeignKey(PlanStep, on_delete = models.CASCADE)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta: 
        verbose_name_plural = 'Step Fields'


class MappingType(models.Model):
    name = models.CharField(max_length = 20)

    def __unicode__(self):
        return self.name

class UserCustomerMapping(models.Model):

    customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    relation_type = models.ForeignKey(MappingType, on_delete = models.CASCADE)

    def __unicode__(self):
        return 'Relation between %s and %s (%s)' % (self.customer.__unicode__(), self.user.__unicode__(), self.relation_type.name)
