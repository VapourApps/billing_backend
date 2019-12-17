import hashlib
import base64
from collections import OrderedDict
from random import randrange


class Halk:

	def __init__(self, store_key, client_id, is_testing=False, **kwargs):

		param_options = [
			{'name': 'oid', 'is_required': True},
			{'name': 'amount', 'is_required': True, 'max_length': 500},
			{'name': 'okUrl', 'is_required': True},
			{'name': 'failUrl', 'is_required': True},
			{'name': 'currencyVal', 'is_required': True, 'max_length': 32},			
			{'name': 'storetype', 'is_required': True},
			{'name': 'lang', 'is_required': True},
			{'name': 'taksit', 'is_required': True},
			{'name': 'islemtipi', 'is_required': True},
			{'name': 'refreshtime', 'is_required':True}	
		]

		self.params = OrderedDict()

		for param in param_options:
			if param['is_required']:
				try:
					kwargs[param['name']]
					self.params[param['name']] = str(kwargs[param['name']])

				except KeyError:
					raise Exception('{} is a required parameter. You need to supply a value for it'.format(param))

			else:
				self.params[param['name']] = str(kwargs.get(param['name'], ''))

			if param.get('max_length'):
				self.params[param['name']] = self.params[param['name']][:param.get('max_length')]


		

		self.store_key = store_key
		self.client_id = client_id

		self.params['clientId'] = self.client_id
		self.params['rnd'] = str(randrange(999999999999))

		if is_testing:
			self.url = "https://entegrasyon.asseco-see.com.tr/fim/est3Dgate"
		else:
			self.url = "https://entegrasyon.asseco-see.com.tr/fim/est3Dgate"

		self.generate_checksum()

	def generate_checksum(self, params=None):

		hash_str = self.client_id
		
		hash_str += self.params['oid']
		hash_str += self.params['amount']
		hash_str += self.params['okUrl']
		hash_str += self.params['failUrl']
		hash_str += self.params['islemtipi']
		hash_str += self.params['taksit']
		hash_str += self.params['rnd']
		hash_str += self.store_key

		hash_value = hashlib.sha1(hash_str.encode('utf-8')).hexdigest()

		hash_value = base64.b64encode(hash_value.decode("hex"))

		self.params['hash'] = hash_value

	def validate_post_data(self, post_data):

		hashparams = post_data['HASHPARAMS']

		hashparamsval = post_data["HASHPARAMSVAL"]
		hashparam = post_data["HASH"]
		paramsval = ""

		for paramname in hashparams.split(':'):

			param_value = post_data.get(paramname, '')
			if paramname == 'clientid':
				param_value = self.client_id

			paramsval += param_value

		hashval = paramsval + self.store_key
		hashed = hashlib.sha1(hashval.encode('utf-8')).hexdigest()
		hashed = base64.b64encode(hashed.decode("hex"))

		if paramsval != hashparamsval or hashparam != hashed:
			return False

		return True
