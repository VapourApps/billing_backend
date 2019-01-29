import logging

from silver.payment_processors import PaymentProcessorBase
from silver.payment_processors.mixins import TriggeredProcessorMixin


class CpayTriggeredBase(PaymentProcessorBase, TriggeredProcessorMixin):
	pass


class CpayTriggered(CpayTriggeredBase):
	def is_payment_method_recurring(self, payment_method):
		return False
