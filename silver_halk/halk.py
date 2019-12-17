import hashlib
import base64
from collections import OrderedDict


class Halk:

	def __init__(self, is_testing=False, **kwargs):

		param_options = [
			{'name': 'clientId', 'is_required': True, 'max_length': 500},
			{'name': 'oid', 'is_required': True},
			{'name': 'amount', 'is_required': True, 'max_length': 500},
			{'name': 'okUrl', 'is_required': True},
			{'name': 'failUrl', 'is_required': True},
			{'name': 'currencyVal', 'is_required': True, 'max_length': 32},
			{'name': 'storekey', 'is_required': True, 'max_length': 10},
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

		self.params['rnd'] = '1555504777'

		if is_testing:
			self.url = "https://entegrasyon.asseco-see.com.tr/fim/est3Dgate"
		else:
			self.url = "https://entegrasyon.asseco-see.com.tr/fim/est3Dgate"

		self.generate_checksum()

	def generate_checksum(self, params=None):

		hash_str = ""
		hash_str += self.params['clientId']
		hash_str += self.params['oid']
		hash_str += self.params['amount']
		hash_str += self.params['okUrl']
		hash_str += self.params['failUrl']
		hash_str += self.params['islemtipi']
		hash_str += self.params['taksit']
		hash_str += self.params['rnd']
		hash_str += self.params['storekey']

		hash_value = hashlib.sha1(hash_str.encode('utf-8')).hexdigest()

		hash_value = base64.b64encode(hash_value.decode("hex"))

		self.params['hash'] = hash_value


	

	def validate_post_data(self, post_data):

		storekey = post_data['storekey']

		hashparams = post_data['HASHPARAMS']

		hashparamsval = post_data["HASHPARAMSVAL"]
		hashparam = post_data["HASH"]
		paramsval = ""

		for paramname in hashparams.split(':'):
			paramsval += post_data.get(paramname, '')

		hashval = paramsval + storekey
		hashed = hashlib.sha1(hashval.encode('utf-8')).hexdigest()
		hashed = base64.b64encode(hashed.decode("hex"))

		if paramsval != hashparamsval or hashparam != hashed:
			return False

		return True
