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
        return 'Feature for ' + self.plan.__unicode__()


class PlanSteps(models.Model):
    step_input_type = models.CharField(max_length = 20)
    step_value = models.CharField(max_length = 30, blank = True)
    step_name = models.CharField(max_length = 30)
    belongs_to = models.ForeignKey(PlanFeatures, on_delete = models.CASCADE)

    def __unicode__(self):
        return 'Step type %s for %s' % (self.step_input_type, self.belongs_to.plan.__unicode__())


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
