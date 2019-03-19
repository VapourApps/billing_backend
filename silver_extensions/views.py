# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers
from silver import models as s
from va_saas.views import current_user

from . import models as se


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
    user = current_user(request)
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

def get_subscriptions(request):
    #This seems weird - user is not in fact the current user, but this seems to set request.user to the correct user. 
    #TODO get this to work in a sane manner, as this is really weird behaviour
    user = current_user(request)

    user_relationship = se.UserCustomerMapping.objects.filter(user_id = request.user.id).all()
    customers = [x.customer for x in user_relationship]
    subscriptions = [{
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
    } for customer in customers for subscription in customer.subscriptions.all()]

    result = {'success' : True, 'data' : subscriptions, 'message' : ''}

    return JsonResponse(result)
