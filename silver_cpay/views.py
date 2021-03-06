# -*- coding: utf-8 -*-
import json
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


def generate_default_serializer_data(request, extra_context):
        serializer_data = {}
        serializer_data['redirect_ok_url'] = request.POST.get('redirect_ok_url', request.build_absolute_uri(reverse('pay-ok')))
        serializer_data['redirect_fail_url'] = request.POST.get('redirect_fail_url', request.build_absolute_uri(reverse('pay-fail')))
        serializer_data['invoice_ids'] = request.POST.get('invoice_ids', extra_context['invoice'].series)

        return serializer_data

def generate_cpay_parameters(request, extra_context = {}):
        # NOTE: This is kind of a temporary fix to go along the temporary fix in silver_extensions.views.py
        # That view was originally supposed to work with a POST request, but we wanted to extend it to work from a mobile app
        # That app uses flutter which evidently doesn't support making POST requests and wrapping them
        # So hopefully one day this won't exist, but in the meantime, it works by adding some data to an empty POST dict and creates the serializer with said default data. 

        serializer_data = request.POST or generate_default_serializer_data(request, extra_context)
        serializer = Payment_Request_Validation_Serializer(data=serializer_data)
        serializer.is_valid()
        
#        serializer.payrequest.build_absolute_uri(reverse('pay-confirm')),
        serializer.sanitazie_post_data()

        invoices = Invoice.objects.filter(series__in=serializer.invoice_ids)
        proformas = Proforma.objects.filter(series__in=serializer.proforma_ids)

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

        if cpay_settings.CPAY_IS_CREATE_PAYMENT_METHOD_AUTOMATICALLY:
                customer = Customer.objects.get(id=customer_ids.pop())
                try:
                        customer.paymentmethod_set.get(payment_processor='cpay')
                except PaymentMethod.DoesNotExist:
                        PaymentMethod.objects.create(
                                customer=customer,
                                payment_processor='cpay',
                                verified=True
                        )

        payment_request = Payment_Request.objects.create(
                redirect_ok_url=serializer.redirect_ok_url,
                redirect_fail_url=serializer.redirect_fail_url
        )

        for invoice in invoices:
                payment_request.invoices.add(invoice)
        for proforma in proformas:
                payment_request.proformas.add(proforma)

        transaction_details = request.POST.get('transaction_details', str(cpay_settings.CPAY_MERCHANT_NAME))
        post_data = {
                'AmountToPay': str(total * 100),
                'AmountCurrency': 'MKD',
                'Details1': str(transaction_details),
                'Details2': payment_request.id,
                'PayToMerchant': str(cpay_settings.CPAY_MERCHANT_ID),
                'MerchantName': str(cpay_settings.CPAY_MERCHANT_NAME),
                'PaymentOKURL': request.build_absolute_uri(reverse('cpay-payment-success')),
                'PaymentFailURL': request.build_absolute_uri(reverse('cpay-payment-fail')),
        }

        cpay_obj = Cpay(password=cpay_settings.CPAY_PASSWORD, is_testing=cpay_settings.CPAY_IS_TESTING, **post_data)

        payment_request.data = json.dumps(dict(cpay_obj.params))
        payment_request.post_url = cpay_obj.url
        payment_request.save()

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

                cpay_obj = Cpay(password=cpay_settings.CPAY_PASSWORD, is_testing=cpay_settings.CPAY_IS_TESTING, **request.data)

                data = {}
                for key in request.data:
                        data[key] = request.data.get(key)

                data = json.dumps(data)

                notification = Notification.objects.create(payment_request=payment_request, status=status, data=data)

                if status == 'success':
                        invoices = payment_request.invoices.all().select_related('customer')
                        proformas = payment_request.proformas.all().select_related('customer')
                        total = 0
                        customer = None

                        for document in chain(invoices, proformas):
                                total += int(document.total)
                                customer = document.customer

                        if cpay_settings.CPAY_IS_CREATE_PAYMENT_METHOD_AUTOMATICALLY:
                                payment_method = None
                                try:
                                        payment_method = customer.paymentmethod_set.get(payment_processor='cpay')
                                except PaymentMethod.DoesNotExist:
                                        payment_method = PaymentMethod.objects.create(
                                                customer=customer,
                                                payment_processor='cpay',
                                                verified=True
                                        )


                        # if there is a mismatch between the amount from cpay, and the document total
                        # notify the admins and dont update the documents
                        # this is highly unlikely, but just in case
                        if int(total * 100) == int(request.data.get('AmountToPay')):
                                for invoice in invoices:
                                    if invoice.state != 'paid':
                                                invoice.pay()
                                for proforma in proformas:
                                        proforma.pay()
#                                        subscription.activate()
#                                        BillingLog = nesho()
#                                        BillingLog.save()

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
                response = generate_cpay_parameters(request, extra_context)
                data = response.get('data', {})
                error = response.get('error')
        except ValidationError as e:
                import traceback
                traceback.print_exc()
                error = e

        context = {
                'params': data.get('parameters'),
                'url': data.get('url'),
                'error': error
        }

        context.update(extra_context)

        return render(request, 'silver_cpay/pay_confirm.html', context)
