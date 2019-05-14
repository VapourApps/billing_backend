import json, requests, threading
from django.db import models

from rest_hooks.models import AbstractHook
from silver.models import Subscription

#This is the very specific case where we have a subscription hook which creates a vm
#We should definitely try and get this to be a general case but for the moment I guess not
#This gets called if the webhook procced on subscription.added.new_vm. Then, if the subscription.metadata contains a "default_data" field, it generates proper default_data payload. 
def subscription_vm_handler(hook, target, payload):

    default_data = {'server_name' : 'hook-test', u'username': u'root', u'network': u'eth0', u'image': u'va-master-img', u'storage': u'500', u'provider_name': u'lxc', u'size': u'va-small', 'subscription_id' : payload['pk'], 'role' : 'va-master'}
    print ('Payload', payload)
#    default_data = payload['fields']['meta']
#    default_data = json.loads(default_data)
#    novobox_name = default_data.get('novobox_name', '')
#    default_data = default_data.get('default_data', {})
#    default_data['server_name'] = novobox_name

    print ('Headers : ', hook.headers)
    headers = json.loads(hook.headers) or {'Content-type' : "application/json"}
    print ('Calling ', hook.method.lower(), ' on ', target,' with headers ', headers, ' and data ', default_data)

    subscription = Subscription.objects.get(pk = payload['pk'])

    if subscription_should_create_vm(subscription):
        print ('Starting creating task')
        vm_creation_task = threading.Thread(target = subscription_handle_vm_creation, args = [hook.method.lower(), target, headers, default_data])
        vm_creation_task.start()
#    print ('Starting (eventually) checking task')
#    vm_check_status = threading.Thread(target = subscription_vm_check_status, args = [target, headers])
    return default_data


def subscription_should_create_vm(subscription):
    print ('Sub state ', subscription.state, ' vm data ', subscription.meta)
    if subscription.state == 'active' and subscription.meta.get('default_data') and not subscription.meta.get('default_data', {}).get('status'):
        print ('Starting vm!')
        return True

def subscription_handle_vm_creation(method, target, headers, default_data):
    print ('In creation!, calling data')
    data = getattr(requests, method)(target, verify = False, headers = headers, data = json.dumps(default_data))
    print ('Finished!', data.text)


def subscription_vm_check_status(target, headers):
    pass

specific_cases = {
    'subscription.updated' : subscription_vm_handler, 
}


class VAHook(AbstractHook):
    headers = models.CharField(max_length = 200, default = '{}')
    method = models.CharField(max_length = 6, default = 'get')

    def __str__(self):
        return self.target

    def __unicode__(self):
        return self.__str__()


def rest_hook_handler(target, payload, instance, hook):
    print ("I have ", target, payload, instance, hook.__dict__, hook.target)
    
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
    filters = {
        'event': event_name,
    }

    hooks = VAHook.objects.filter(**filters)
    for hook in hooks:
        hook.deliver_hook(instance)


