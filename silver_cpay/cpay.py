import hashlib
from collections import OrderedDict


class Cpay:

	def __init__(self, password, is_testing=False, **kwargs):

		param_options = [
			{'name': 'PaymentOKURL', 'is_required': True},
			{'name': 'PaymentFailURL', 'is_required': True},
			{'name': 'AmountToPay', 'is_required': True},
			{'name': 'AmountCurrency', 'is_required': True},
			{'name': 'PayToMerchant', 'is_required': True},
			{'name': 'Details1', 'is_required': True},
			{'name': 'Details2', 'is_required': True},
			{'name': 'MerchantName', 'is_required': True},
			{'name': 'OriginalAmount', 'is_required': False},
			{'name': 'OriginalCurrency', 'is_required': False},
			{'name': 'Fee', 'is_required': False},
			{'name': 'CRef', 'is_required': False},
			{'name': 'TransactionType', 'is_required': False},
			{'name': 'Installment', 'is_required': False},
			{'name': 'RPRef', 'is_required': False},
			{'name': 'FirstName', 'is_required': False},
			{'name': 'LastName', 'is_required': False},
			{'name': 'Address', 'is_required': False},
			{'name': 'City', 'is_required': False},
			{'name': 'Zip', 'is_required': False},
			{'name': 'Country', 'is_required': False},
			{'name': 'Telephone', 'is_required': False},
			{'name': 'Email', 'is_required': False},
			{'name': 'cPayPaymentRef', 'is_required': False},
		]

		self.params = OrderedDict()

		for param in param_options:
			if param['is_required']:
				try:
					kwargs[param['name']]
					self.params[param['name']] = kwargs[param['name']]
				except KeyError:
					raise Exception('{} is a required parameter. You need to supply a value for it'.format(param))

			else:
				self.params[param['name']] = kwargs.get(param['name'], '')

		self.password = password

		if is_testing:
			self.password = 'TEST_PASS'
			self.url = "https://www.cpay.com.mk/Client/page/default.aspx?xml_id=/mk-MK/.TestLoginToPay/"
		else:
			self.url = "https://80.77.147.45/client/Page/default.aspx?xml_id=/mk-MK/.loginToPay/.simple/"

		self.generate_checksum()

	def generate_checksum(self, params=None):

		if not params:
			params = self.params
		# this function is based on the casys documentation, appendix A

		header = ""
		input_string = ""

		values = ""
		value_count = ""

		param_length = 0

		for key, value in params.items():
			if value != '':
				header += str(key) + ','

				values += str(value)
				value_count += "{:03d}".format(len(str(value)))
				# print (value_count, str(value))

				param_length += 1

		header += value_count

		# the checksum header starts with the number of parameters
		header = "{:02d}".format(param_length) + header

		input_string = header + values + self.password

		# print (input_string)

		check_sum = hashlib.md5(input_string.encode('utf-8')).hexdigest().upper()

		self.params['CheckSum'] = check_sum
		self.params['CheckSumHeader'] = header

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
