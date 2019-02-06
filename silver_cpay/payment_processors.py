import logging

from silver.payment_processors import PaymentProcessorBase
from silver.payment_processors.mixins import TriggeredProcessorMixin

from silver.models.transactions.codes import FAIL_CODES, CANCEL_CODES, REFUND_CODES 


class CpayTriggeredBase(PaymentProcessorBase, TriggeredProcessorMixin):
	pass


class CpayTriggered(CpayTriggeredBase):
        template_slug = 'cpay_processor'

	def is_payment_method_recurring(self, payment_method):
		return False

        def execute_transaction(self, transaction):
                pass

        def _update_transaction_status(self, transaction, transaction_result):
                pass


