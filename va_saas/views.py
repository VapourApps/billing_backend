# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import rest_framework_jwt.views as JWT



from .models import CompanyPageLanding, CompanyPagePricing, CompanyPageAbout, CompanyPage, CompanyPageFeature, CompanyPageFeaturesList
from .serializers import UserSerializer, UserSerializerWithToken
import requests, json

from silver.models import Customer, Invoice
from silver_extensions.models import UserCustomerMapping

def rest_hook_handler(target, payload, instance, hook):
    print ("I have ", target, payload, instance, hook)

    kwargs = {
        'headers' : json.loads(hook.headers) or {'Content-type' : "application/json"}, 
        'data' : payload, 
        
    }
    data = getattr(requests, hook.method)(target, **kwargs)
    print (data)


def obtain_jwt_token(response):
    print ('In my view')
    print ('Rseponse : ', response.POST)
    return JWT.obtain_jwt_token(response)

def check_activation_token(uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        return uid
    return False

@permission_classes((AllowAny, ))
@api_view(['GET'])
def activate(request, uidb64, token):
    uid = check_activation_token(uidb64, token)
    print ('UID is : ', uid)
    if uid:
        user = User.objects.get(pk=uid)
        print ('User is :', user)
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('https://billing.vapour-apps.com/')
    else:
        print ('Invalid!')
        return Response('Activation link is invalid!', status = 400)

@api_view(['POST'])
@permission_classes((AllowAny, ))
def forgot_pass(request):
    data = json.loads(request.body)
    user_email = data.get('email')
    user = User.objects.filter(username = user_email)
    if not user: 
        return Response("No user with email : " + str(user_email), status = 400)


    user = user[0]
    mail_subject = 'Change your *~VA~* account password.'

    random_pass = User.objects.make_random_password()

    user.set_password(random_pass)
    user.save()

    message = render_to_string('change_pass.html', {
        'user': user,
        'url': 'https://billing.vapour-apps.com/#/Login',
        'password' : random_pass, 
    })
    to_email = user_email
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.send()

    return Response('Sent mail to ' + str(user_email))


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
def add_customer(request):
    data = request.data
    relation_type = data.pop('relation_type')

    customer = customer(**data)
    customer.save()

    relation_type = UserCustomerMapping(customer = customer, user = request.user, relation_type = relation_type)
    relation_type.save()

    return Response('Success!')


def get_customer_for_user(request):
    mapping = UserCustomerMapping.objects.filter(user = request.user).all()[0]
    return mapping.customer


@api_view(['POST'])
def map_customer_user(request):

    data = request.data

    customer = Customer.objects.filter(id = data['customer_id']).all()[0]
    relation_type = data['relation_type']
    relation_type = UserCustomerMapping(customer = customer, user = request.user, relation_type = relation_type)
    relation_type.save()

    return Response('Success!') 


@api_view(['POST'])
def change_user_password(request):
    data = request.data
    if not all([x in data.keys() for x in ['username', 'old_password', 'new_password']]):
        return Response('Requires 3 POST arguments : username, old_password and new_password. ', status = 400)

    user = authenticate(username = data['username'], password = data['old_password'])
    if not user: 
        return Response('Could not authenticate user with supplied credentials. ', status = 401)
    user.set_password(data['new_password'])
    user.save()
    return Response('Success!')

class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    a =requests.get('http://billing-api.vapour-apps.com/admin')
    return HttpResponse("return this string")

#Helper function to reduce repeating code - simply gets the object with the specified id and model name. 
#This may already exist in django but using it at least as a quick fix until we have time to figure it out. 
def filter_get_request_data(request, model, to_dict = True):
    if request.GET:
        company = CompanyPage.objects.filter(company_name = request.GET['company_name'])
        data = model.objects.filter(company_page = company)
    else: 
        data= model.objects.all()

    if to_dict:
        data = model_to_dict(data[0])

    return data

def get_features(request):
    company_name = request.GET['company_name']

    data = CompanyPageFeature.objects.filter(belongs_to_list__company_page__company_name = company_name)
#    data = CompanyPageFeature.objects.filter(company_name = belongs_to_list.company_name)
    data = {
        "success" : True, 
        "message" : "", 
        "data" :  [{
            "feature_image" : x.feature_image.url, 
            "feature_details" : x.feature_details,
            "feature_header" : x.feature_header,
        } for x in data]
    }
    return HttpResponse(json.dumps(data))

def get_invoices(request):
    
    user = current_user(request)

    user_relationship = UserCustomerMapping.objects.filter(user_id = request.user.id).all()
    customers = [x.customer for x in user_relationship]
    invoices = []
    for customer in customers: 

        invoice = Invoice.objects.filter(customer = customer).all()
        if invoice:
            invoice = invoice[0]
            invoice = {
                x : str(getattr(invoice, x)) for x in ["kind", "related_document", "series", "number", "customer", "provider", "archived_customer", "archived_provider", "due_date", "issue_date", "paid_date", "cancel_date", "sales_tax_percent", "sales_tax_name", "currency", "transaction_currency", "transaction_xe_rate", "transaction_xe_date", "pdf", "state"]
            }
            invoices.append(invoice)

    data = {"success" : True, "message" : "", "data" : invoices}
    return HttpResponse(json.dumps(data))
   
def get_plans(request):
    pass


def get_company_page_landing(request):
    data = json.dumps(filter_get_request_data(request, CompanyPageLanding))
    return HttpResponse(data,content_type='application/json')

def get_company_page_pricing(request):
    data = json.dumps(filter_get_request_data(request, CompanyPagePricing))
    return HttpResponse(data,content_type='application/json')

def get_company_page_about(request):
    data = json.dumps(filter_get_request_data(request, CompanyPageAbout))
    return HttpResponse(data,content_type='application/json')

def get_steps_for_company(request):
    about_page = filter_get_request_data(request, CompanyPageAbout, to_dict = False)[0]
    steps = about_page.companypageaboutsteps_set.all()

    data = json.dumps({'steps' : [model_to_dict(x) for x in steps]})

    return HttpResponse(data,content_type='application/json')


