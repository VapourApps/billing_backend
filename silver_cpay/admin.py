# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from silver_cpay.models import Payment_Request, Notification

admin.site.register(Payment_Request)
admin.site.register(Notification)


# Register your models here.
