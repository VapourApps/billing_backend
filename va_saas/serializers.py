from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
import django.contrib.auth
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        print ('Validated data is : ', validated_data)

        instance = self.Meta.model(**validated_data)
        instance.is_active = False
        if password is not None:
            instance.set_password(password)
        instance.save()
        
        mail_subject = 'Activate your ~VA~ account.'
        instance_uid = urlsafe_base64_encode(force_bytes(instance.pk))
        instance_token = account_activation_token.make_token(instance)
        message = render_to_string('signup.html', {
            'user': instance,
            'domain': settings.VA_DOMAIN,
            'uid': instance_uid,
            'token': instance_token,
        })
        print ('Sending ', message)
        print ('UID is ', instance_uid)
        print ('Token is ', instance_token)
        to_email = validated_data.get('email')
        email = EmailMessage(
                    mail_subject, message, to=[to_email]
        )
        email.send()
        print ('Sent!')
        return instance

    class Meta:
        model = User
        fields = ('token', 'username', 'password', 'first_name', 'last_name', 'email', 'id')
