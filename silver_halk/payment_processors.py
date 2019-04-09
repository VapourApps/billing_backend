from silver.payment_processors import PaymentProcessorBase
from silver.payment_processors.mixins import TriggeredProcessorMixin

from silver.models.transactions.codes import FAIL_CODES, CANCEL_CODES, REFUND_CODES 


class HalkTriggeredBase(PaymentProcessorBase, TriggeredProcessorMixin):
	pass


class HalkTriggered(HalkTriggeredBase):
	template_slug = 'halk_processor'

	def is_payment_method_recurring(self, payment_method):
		return False

	def execute_transaction(self, transaction):
		pass

	def _update_transaction_status(self, transaction, transaction_result):
		pass
