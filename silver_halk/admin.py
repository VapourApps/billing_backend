# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from silver_halk.models import Halk_Payment_Request
from silver_halk.models import Halk_Notification

admin.site.register(Halk_Payment_Request)
admin.site.register(Halk_Notification)


# Register your models here.
