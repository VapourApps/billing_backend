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

		#$hash = base64_encode(pack('H*',sha1($hashstr)));

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
		print(hash_str.encode('utf-8'))
		print(hash_value)
		print(hash_value.decode("hex"))
		hash_value = base64.b64encode(hash_value.decode("hex"))

		self.params['hash'] = hash_value

		"""
		$hashstr = $clientId . $oid . $amount . $okUrl . $failUrl .$transactionType. $instalment .$rnd . $storekey;

		$hash = base64_encode(sha1($hashstr));
		$hash = base64_encode(pack('H*',sha1($hashstr)));
		"""

	def prepare_params(self, post_data):

		return_checksum_header = post_data['ReturnCheckSumHeader']
		header_fields = return_checksum_header[2:].split(',')
		header_fields = header_fields[:-1]
		params_to_check = OrderedDict()

		for field_name in header_fields:
			params_to_check[field_name] = post_data[field_name]

		self.params = params_to_check

	def validate_post_data(self, post_data):

		self.prepare_params(post_data)
		self.generate_checksum()

		if post_data['ReturnCheckSum'] == self.params['CheckSum'] \
			and post_data['ReturnCheckSumHeader'] == self.params['CheckSumHeader']:
			return True

		else:
			return False
