import json, requests
from django.db import models

from rest_hooks.models import AbstractHook

#This is the very specific case where we have a subscription hook which creates a vm
#We should definitely try and get this to be a general case but for the moment I guess not
#This gets called if the webhook procced on subscription.added.new_vm. Then, if the subscription.metadata contains a "vm_data" field, it generates proper vm_data payload. 
def subscription_vm_handler(payload):
    #vm_data = {u'username': u'root', u'network': u'default', u'image': u'debian-9.5.6-20181013-openstack-amd64.qcow2', u'storage': u'500', u'provider_name': u'libvirt', u'size': u'va-small'}

    vm_data = payload.get('vm_data', {})
    return vm_data




specific_cases = {
    'subscription.added.new_vm' : subscription_vm_handler, 
}


class VAHook(AbstractHook):
    headers = models.CharField(max_length = 200, default = '{}')
    method = models.CharField(max_length = 6, default = 'get')


def rest_hook_handler(target, payload, instance, hook):
    print ("I have ", target, payload, instance, hook)

    hook = VAHook.objects.filter(target = hook.target)[0]

    #We currently use extra_data to support creating VMs when creating subscrtiptions for a handful of specific cases.
    #We should probably find a generic way to add custom extra data, but for the moment, this will have to do. 
    #We use a global dict with specific cases for this. Hopefully this never grows out of control. 
    if payload['event'] in specific_cases: 
        extra_data_method = specific_cases[payload_data]
        extra_data = extra_data_method(payload)

        payload.update(extra_data)

    kwargs = {
        'headers' : json.loads(hook.headers) or {'Content-type' : "application/json"}, 
        'data' : payload, 
        
    }
    data = getattr(requests, hook.method.lower())(target, verify = False, **kwargs)
    print (data.json())
    return data


#This was a test to see if the custom hook firing works but for some reason it doesn't. Oh well, I managed to hack together a solution. 
def find_and_fire_hook(event_name, instance, **kwargs):
    open('/tmp/nesho', 'w').write('wtf is this')
    print ('Firing hook')
    filters = {
        'event': event_name,
    }

    hooks = VAHook.objects.filter(**filters)
    for hook in hooks:
        hook.deliver_hook(instance)


