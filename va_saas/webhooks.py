import json, requests, threading
from django.db import models

from rest_hooks.models import AbstractHook

#This is the very specific case where we have a subscription hook which creates a vm
#We should definitely try and get this to be a general case but for the moment I guess not
#This gets called if the webhook procced on subscription.added.new_vm. Then, if the subscription.metadata contains a "vm_data" field, it generates proper vm_data payload. 
def subscription_vm_handler(hook, target, payload):

    #vm_data = {u'username': u'root', u'network': u'default', u'image': u'debian-9.5.6-20181013-openstack-amd64.qcow2', u'storage': u'500', u'provider_name': u'libvirt', u'size': u'va-small'}
    print ('Payload', payload)
    vm_data = payload['fields']['meta']
    vm_data = json.loads(vm_data)
    novobox_name = vm_data.get('novobox_name', '')
    vm_data = vm_data.get('vm_data', {})
    vm_data['server_name'] = novobox_name

    headers = json.loads(hook.headers) or {'Content-type' : "application/json"}
    print ('Calling ', hook.method.lower(), ' on ', target,' with headers ', headers, ' and data ', vm_data)

    print ('Starting creating task')
    vm_creation_task = threading.Thread(target = subscription_handle_vm_creation, args = [hook.method.lower(), target, headers, vm_data])
    vm_creation_task.start()

    print ('Starting (eventually) checking task')
    vm_check_status = threading.Thread(target = subscription_vm_check_status, args = [target, headers])
    return vm_data


def subscription_handle_vm_creation(method, target, headers, vm_data):
    print ('In creation!, calling data')
    data = getattr(requests, method)(target, verify = False, headers = headers, data = json.dumps(vm_data))
    print ('Finished!', data)


def subscription_vm_check_status(target, headers):
    pass

specific_cases = {
    'subscription.added' : subscription_vm_handler, 
}


class VAHook(AbstractHook):
    headers = models.CharField(max_length = 200, default = '{}')
    method = models.CharField(max_length = 6, default = 'get')


def rest_hook_handler(target, payload, instance, hook):
    print ("I have ", target, payload, instance, hook)
    
    hook = VAHook.objects.filter(target = hook.target)[0]

    url_data = payload['data']
    print ('Pure data is : ', url_data)
    event = payload['hook']['event']

    #We currently use extra_data to support creating VMs when creating subscrtiptions for a handful of specific cases.
    #We should probably find a generic way to add custom extra data, but for the moment, this will have to do. 
    #We use a global dict with specific cases for this. Hopefully this never grows out of control. 
    if event in specific_cases: 
        specific_handler = specific_cases[event]
        return specific_handler(hook, target, url_data)

    headers = json.loads(hook.headers) or {'Content-type' : "application/json"}
    print ('Calling ', hook.method.lower(), ' on ', target,' with headers ', headers, ' and data ', url_data)
    data = getattr(requests, hook.method.lower())(target, verify = False, headers = headers, data = json.dumps(url_data))
    print (data.text)
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


