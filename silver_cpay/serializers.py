from rest_framework.serializers import ModelSerializer, ValidationError, CharField, Serializer
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError as django_default_validation_error

from .models import Payment_Request, Notification


class Notification_Serializer(ModelSerializer):
	class Meta:
		model = Notification
		fields = "__all__"


class Payment_Request_Serializer(ModelSerializer):
	class Meta:
		model = Payment_Request
		fields = "__all__"


class Payment_Request_Validation_Serializer(Serializer):
	invoice_ids = CharField(max_length=5000)
	proforma_ids = CharField(max_length=5000)
	redirect_ok_url = CharField(max_length=2083, required=True)
	redirect_fail_url = CharField(max_length=2083, required=True)


	def sanitazie_post_data(self):

		self.invoice_ids_str = self.data.get('invoice_ids')
		self.proforma_ids_str = self.data.get('proforma_ids')

		try:
			self.redirect_ok_url = self.data['redirect_ok_url']
		except KeyError:
			raise ValidationError('Please supply a redirect_ok_url'	)

		try:
			self.redirect_fail_url = self.data['redirect_fail_url']
		except KeyError:
			raise ValidationError('Please supply a redirect_fail_url'	)

		self.redirect_fail_url = self.data['redirect_fail_url']

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
