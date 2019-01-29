from rest_framework.serializers import ModelSerializer, ValidationError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError as django_default_validation_error

from .models import Payment_Request


class Payment_Request_Serializer(ModelSerializer):
	class Meta:
		model = Payment_Request
		fields = "__all__"

	def sanitazie_post_data(self):

		self.invoice_ids_str = self.data.get('invoice_ids')
		self.proforma_ids_str = self.data.get('proforma_ids')
		self.redirect_ok_url = self.data.get('redirect_ok_url')
		self.redirect_fail_url = self.data.get('redirect_fail_url')

		if self.invoice_ids_str in [None, ''] and self.proforma_ids_str in [None, '']:
			raise ValidationError(
				'Please supply a invoice_ids or proforma_ids parameter. Both can not be blank.'
			)

		self.invoice_ids = []
		if self.invoice_ids_str not in [None, '']:
			for invoice_id in self.invoice_ids_str.split(','):
				try:
					self.invoice_ids.append(int(invoice_id))
				except ValueError:
					raise ValidationError('Invalid invocie_ids supplied')

		self.proforma_ids = []
		if self.proforma_ids_str not in [None, '']:
			for proforma_id in self.proforma_ids_str.split(','):
				try:
					self.proforma_ids.append(int(proforma_id))
				except ValueError:
					raise ValidationError('Invalid proforma_ids supplied')

		if self.redirect_ok_url not in [None, '']:
			validate = URLValidator()
			try:
				validate(self.redirect_ok_url)
			except django_default_validation_error:
				raise ValidationError('Invalid redirect_ok_url supplied')

		if self.redirect_fail_url not in [None, '']:
			validate = URLValidator()
			try:
				validate(self.redirect_fail_url)
			except django_default_validation_error:
				raise ValidationError('Invalid redirect_fail_url supplied')
