from django.db import models
from silver.models import Proforma, Invoice

class Payment_Request(models.Model):
	#proforma_ids = models.CharField(blank=True, null=True, max_length=5000)
	#invoice_ids = models.CharField(blank=True, null=True, max_length=5000)
	redirect_ok_url = models.CharField(blank=True, null=True, max_length=2083)
	redirect_fail_url = models.CharField(blank=True, null=True, max_length=2083)

	proformas = models.ManyToManyField(Proforma, related_name='proforma_payment_requests')
	invoices = models.ManyToManyField(Invoice, related_name='invoice_payment_requests')

	status_choices = (
		('generated', 'generated'),
		('success', 'success'),
		('fail', 'fail'),
	)

	status = models.CharField(blank=False, null=False, max_length=9, choices=status_choices,
		default='generated'
	)


class Notification(models.Model):
	payment_request = models.ForeignKey(Payment_Request)
	status_choices = (
		('success', 'success'),
		('fail', 'fail'),
		('invalid_data', 'invalid_data')
	)

	status = models.CharField(blank=False, null=False, max_length=9, choices=status_choices)

