# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from django.core import serializers
from silver import models as s
from va_saas.views import current_user
from django.urls import reverse
from silver_cpay.views import generate_cpay_form

from . import models as se
from silver_cpay.models import Payment_Request
from silver.models import Invoice

def get_plans(request):
    enabled = request.GET.get('enabled', True)
    plans = s.Plan.objects.filter(enabled = enabled)
    if request.GET.get('private'):
        plans = plans.filter(private = request.GET['private'])

    plans = plans.all()

    result = []

    #This field is not serialized by default, and is not required, so to avoid a bit of hassle, I'm just ignoring it
    #There might be other fields. 
    ignore_fields = ['metered_features']

    for plan in plans: 
        plan_features = se.PlanFeatures.objects.filter(plan_id = plan.id).all()
        plan_result = model_to_dict(plan)
        plan_result['plan_provider'] = model_to_dict(plan.provider) 

        if plan_features:
            plan_feature = plan_features[0]
            feature = model_to_dict(plan_feature)
            feature = {
                'plan_image' : feature['plan_image'].url,
                'plan_description' : feature['plan_description'], 
                'plan_steps' : [
                    {'input_type' : step.step_input_type, 'input_name' : step.step_name, 'input_value': step.step_value}
                    for step in plan_feature.plansteps_set.all()]
            }
            feature['plan_image'] = plan_feature.plan_image.url

            plan_result['feature'] = feature
        plan_result = {x : plan_result[x] for x in plan_result if x not in ignore_fields}    
        result.append(plan_result)

    result = {'success' : True, 'data' : result, 'message' : ''}
    return JsonResponse(result)

@api_view(['GET'])
def get_customers(request):
    user = current_user(request._request)
    user_relationship = se.UserCustomerMapping.objects.filter(user_id = request.user.id).all()

    customers = [model_to_dict(x.customer) for x in user_relationship]
    result = {'sucess' : True, 'data' : customers, 'message' : ''}
    return JsonResponse(result)

@api_view(['POST'])
def edit_customer(request):
    customer_mail = request.POST['email']
    customer_data = request.POST['customer_data']
    customer = Customer.objects.filter(email = customer_mail)
    for key, value in customer_data.items():
        setattr(customer, key, value)
    customer.save()


def get_subscriptions_for_customer(customer):
    subs = [{
	'id': subscription.id,
	'customer_id': customer.id,
        'first_name' : customer.first_name, 
        'last_name' : customer.last_name,
        'address' : customer.address_1,
        'phone' : customer.phone,
        'description' : subscription.description, 
        'plan_name' : subscription.plan.name,
        'state' : subscription.state, 
        'start_date' : subscription.start_date, 
        'ended_at' : subscription.ended_at,
        'cancel_date' : subscription.cancel_date, 
        'trial_end' : subscription.trial_end, 
        'meta' : subscription.meta, 
        'company' : customer.company,
        'interval' : subscription.plan.interval,
        'interval_count' : subscription.plan.interval_count,
        'amount': subscription.plan.amount,
        'currency' : subscription.plan.currency,
#        'meters' : [x.to_dict() for x in subscription.meter_set.all()],
    } for subscription in customer.subscriptions.all()]
    return subs

def get_subscriptions(request):
    #This seems weird - user is not in fact the current user, but this seems to set request.user to the correct user. 
    #TODO get this to work in a sane manner, as this is really weird behaviour
    user = current_user(request)

    user_relationship = se.UserCustomerMapping.objects.filter(user_id = request.user.id).all()
    customers = [x.customer for x in user_relationship]
    subscriptions = [get_subscriptions_for_customer(customer) for customer in customers]

    result = {'success' : True, 'data' : subscriptions, 'message' : ''}

    return JsonResponse(result)


def cpay_payment_ok(request, cpay_request_id=None):
    # Your custom payment success web page
    cpay_request = Payment_Request.objects.get(id=cpay_request_id)
    return HttpResponse("Your payment success page. Payment request ID:{}".format(cpay_request.id))


def cpay_payment_fail(request, cpay_request_id=None):
    # Your custom payment faile web page
    cpay_request = Payment_Request.objects.get(id=cpay_request_id)
    return HttpResponse("Your payment fail page. Payment request ID: {}".format(cpay_request.id))

def pay_select(request, invoice_series = None):
    context = {}

    # NOTE: This is a kind of temporary / hackish solution to make the view work both with GET and POST variants. 
    # If the view is accessed via GET and without an invoice series, it goes to a form which asks for the series and then posts to the same view
    # Alternatively, if the invoice_series is set, then the POST step is skipped and instantly goes to the confirm page. 
    # This is done to more easily wrap the view in a mobile app, but has security concerns and we should get it working properly. 
    if request.POST or invoice_series:
        try: 
            invoice_series = invoice_series or request.POST.get('invoice_ids')
            int(invoice_series) #check if series is in a valid format
            if Invoice.objects.filter(series = invoice_series):
                print ('Returning pay_confirm')
                return pay_confirm(request, invoice_series)
            else:
                context['error'] = 'Не е пронајдена фактура !' #no invoice
        except ValueError: 
            context['error'] = 'Невалиден формат !' #invalid series

    return render(request, 'silver_extensions/pay_select.html', context)


def pay_confirm(request, invoice_series= None):
    # you custom code for payment confirmation goes here. 
    # This is the page that is shown before the redirec to Cpay

    # at the end call the generate_cpay_form from silver_cpay, to generate the cpay form
    # add the extra_context parameter for any additional template vars that you want

    invoice_series = invoice_series or request.POST.get('invoice_ids')
    invoice = Invoice.objects.filter(series = invoice_series).all()[0]
    print ('Returning cpay_form')
    return generate_cpay_form(request, extra_context={
        'invoice' : invoice,
    })
