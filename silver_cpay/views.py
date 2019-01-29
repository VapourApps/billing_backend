# -*- coding: utf-8 -*-
from itertools import chain

from rest_framework.views import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.serializers import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.mail import mail_admins

from silver.models import Invoice, Proforma, BillingDocumentBase, PaymentMethod, Customer

from silver_cpay.cpay import Cpay
from silver_cpay import app_settings as cpay_settings
from silver_cpay.models import Payment_Request, Notification
from silver_cpay.serializers import Payment_Request_Validation_Serializer, Payment_Request_Serializer, Notification_Serializer


def generate_cpay_parameters(request):

	serializer = Payment_Request_Validation_Serializer(data=request.POST)
	serializer.is_valid()
	serializer.sanitazie_post_data()

	invoices = Invoice.objects.filter(id__in=serializer.invoice_ids)
	proformas = Proforma.objects.filter(id__in=serializer.proforma_ids)

	if len(invoices) == 0 and len(proformas) == 0:
		return {
			'status': status.HTTP_400_BAD_REQUEST,
			'error': 'No invoices or proformas selected'
		}

	customer_ids = set()

	total = 0

	for document in chain(invoices, proformas):
		if document.state != BillingDocumentBase.STATES.ISSUED:
			return {
				'status': status.HTTP_400_BAD_REQUEST,
				'error': '{} {} is not in ISSUED state. '
					'You can pay only based on issued documents'.format(type(document).__name__, document.id)
			}

		# to do: currency conversion support
		# for the time being only MKD is allowed
		if document.currency != 'MKD':
			return {
				'status': status.HTTP_400_BAD_REQUEST,
				'error': '{} {} is issued in {} currency. '
					'Cpay allows payment only in the following currenies: {}'.format(
						type(document).__name__, document.id, document.currency, ','.join(cpay_settings.CPAY_ALLOWED_CURENCIES)
					)
			}

		total += int(document.total)
		customer_ids.update([document.customer_id])

	if total <= 0:
		return {
			'error': 'Can not generate payment parameters for invoices that have a combined total of 0.',
			'status': status.HTTP_400_BAD_REQUEST
		}

	if len(customer_ids) > 1:
		return {
			'error': 'Can not generate payment parameters for invoices '
				'and proformas belogning to multiple customers',
			'status': status.HTTP_400_BAD_REQUEST
		}

	payment_request = Payment_Request.objects.create(
		redirect_ok_url=serializer.redirect_ok_url,
		redirect_fail_url=serializer.redirect_fail_url
	)

	for invoice in invoices:
		payment_request.invoices.add(invoice)
	for proforma in proformas:
		payment_request.proformas.add(proforma)

	customer = Customer.objects.get(id=customer_ids.pop())
	try:
		customer.paymentmethod_set.get(payment_processor='cpay')
	except PaymentMethod.DoesNotExist:
		PaymentMethod.objects.create(
			customer=customer,
			payment_processor='cpay',
			verified=True
		)

	post_data = {
		'AmountToPay': str(total * 100),
		'AmountCurrency': 'MKD',
		'Details1': payment_request.id,
		'Details2': payment_request.id,
		'PayToMerchant': str(cpay_settings.CPAY_MERCHANT_ID),
		'MerchantName': str(cpay_settings.CPAY_MERCHANT_NAME),
		'PaymentOKURL': request.build_absolute_uri(reverse('cpay-payment-success')),
		'PaymentFailURL': request.build_absolute_uri(reverse('cpay-payment-fail')),
	}

	cpay_obj = Cpay(password=cpay_settings.CPAY_PASSWORD, is_testing=False, **post_data)

	return {'data': {'parameters': cpay_obj.params, 'url': cpay_obj.url}, 'status': status.HTTP_200_OK}


class Cpay_View_Set(viewsets.ViewSet):
	authentication_classes = []
	permission_classes = (permissions.AllowAny,)
	pagination_class = PageNumberPagination
	pagination_class.page_size = 20

	def generate_parameters(self, request):
		response = generate_cpay_parameters(request)
		if response.get('error'):
			return JsonResponse({'error': response.get('error')}, status=response['status'])
		else:
			return JsonResponse(response.get('data'), status=response['status'])

	def process_notification(self, request, status):
		payment_request_id = int(request.data.get('Details2'))
		payment_request = Payment_Request.objects.get(id=payment_request_id)
		payment_request.status = status
		payment_request.save()

		cpay_obj = Cpay(password=cpay_settings.CPAY_PASSWORD, is_testing=False, **request.data)

		notification = Notification.objects.create(payment_request=payment_request, status=status)

		if status == 'success':
			invoices = payment_request.invoices.all().select_related('customer')
			proformas = payment_request.proformas.all().select_related('customer')
			total = 0
			customer = None

			for document in chain(invoices, proformas):
				total += int(document.total)
				customer = document.customer

			payment_method = None
			try:
				payment_method = customer.paymentmethod_set.get(payment_processor='cpay')
			except PaymentMethod.DoesNotExist:
				payment_method = PaymentMethod.objects.create(
					customer=customer,
					payment_processor='cpay',
					verified=True
				)

			"""
			transaction_data = {
				'amount': int(request.data.get('AmountToPay')) / 100,
				'currency': 'MKD',
				'payment_method_id': payment_method.id,
				'external_reference': request.data.get('cPayPaymentRef'),
				'state': 'settled'  # (options: 'initial', 'pending', 'settled', 'failed', 'canceled', 'refunded')
			}

			# if the payment was linked to a single invoice or proforma, add it in the transaction
			if len(invoices) == 1:
				transaction_data['invoice'] = invoices[0]
			elif len(proformas) == 1:
				transaction_data['proforma'] = proformas[0]

			print(transaction_data)

			Transaction.objects.create(**transaction_data)
			"""

			# if there is a mismatc between the amount from cpay, and the document total
			# notify the admins and dont update the documents
			# this is highly unlikely, but just in case
			if int(total * 100) == int(request.data.get('AmountToPay')):
				for invoice in invoices:
					invoice.pay()
				for proforma in proformas:
					proforma.pay()

			else:
				mail_admins(
					'Amount mismatch between Cpay Notification and Document total',
					'There has been and amount mismatch between the Cpay Notificion and Calculated Document Total.'
					'\nThe documents were not marked as paid\n'
					'Cpay Payment Request ID: {}\nCpay Notification ID: {}'.format(
						payment_request.id,
						notification.id
					),
					fail_silently=True,
				)

			redirect_url = payment_request.redirect_ok_url
		else:
			redirect_url = payment_request.redirect_fail_url

		if cpay_obj.validate_post_data(request.data):
			return HttpResponseRedirect(redirect_to="{}/{}".format(redirect_url, payment_request_id))

		else:
			notification.status = 'invalid_data'
			notification.save()
			return JsonResponse({'error': 'Invalid data'})

	def payment_success(self, request):
		return self.process_notification(request, 'success')

	def payment_fail(self, request):
		return self.process_notification(request, 'fail')

	"""
	def get_notifications(self, request):
		notifications = Notification.objects.all()
		serializer = Notification_Serializer(notifications, many=True)
		return JsonResponse(serializer.data, safe=False)

	def get_payment_requests(self, request):
		payment_requests = Payment_Request.objects.all()
		serializer = Payment_Request_Serializer(payment_requests, many=True)
		return Response(serializer.data)
	"""
	def get_payment_request(self, request, id):
		payment_request = Payment_Request.objects.get(id=id)
		serializer = Payment_Request_Serializer(payment_request)
		return JsonResponse(serializer.data)


def generate_cpay_form(request, extra_context={}):
	data = {}
	error = None

	try:
		response = generate_cpay_parameters(request)
		data = response.get('data', {})
		error = response.get('error')
	except ValidationError as e:
		error = e

	context = {
		'params': data.get('parameters'),
		'url': data.get('url'),
		'error': error
	}

	context.update(extra_context)

	return render(request, 'silver_cpay/pay_confirm.html', context)
