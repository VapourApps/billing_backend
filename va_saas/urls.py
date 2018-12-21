from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from . import views

urlpatterns = [
    url(r'token-auth', views.obtain_jwt_token),
    url(r'get-user', views.current_user),
    url(r'change_user_password', views.change_user_password),
    url(r'users/', views.UserList.as_view()),
    url(r'^getCompanyPageLanding/$',views.get_company_page_landing,name='companyPageLanding'),
    url(r'^getCompanyPagePricing/$',views.get_company_page_pricing,name='companyPagePricing'),
    url(r'^getCompanyPageAbout/$',views.get_company_page_about,name='companyPageAbout'),
    url(r'^getCompanyPageAboutSteps/$',views.get_steps_for_company,name='companyPageAboutSteps'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^forgot_password', views.forgot_pass, name = 'forgot_password'),
    url(r'^add_customer', views.add_customer, name = 'add_customer'),
    url(r'^map_customer_to_user', views.map_customer_user, name = 'map_customer_user'),
    url(r'^get_features', views.get_features, name = 'get_features'),
    url(r'^get_invoices', views.get_invoices, name = 'get_invoices'),

]                                            
