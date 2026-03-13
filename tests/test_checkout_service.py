import unittest
from unittest.mock import Mock

from src.models import CartItem, Order
from src.pricing import PricingService, PricingError
from src.checkout import CheckoutService, ChargeResult


class TestCheckoutService(unittest.TestCase):
    def test_checkout_ok(self):
        payments = Mock()
        email = Mock()
        fraud = Mock()
        repo = Mock()

        fraud.score.return_value = 10
        payments.charge.return_value = ChargeResult(ok=True, charge_id="ch_123")

        checkout = CheckoutService(
            payments=payments,
            email=email,
            fraud=fraud,
            repo=repo,
        )

        items = [CartItem("A", 10000, 2)]

        result = checkout.checkout(
            user_id="u1",
            items=items,
            payment_token="tok_visa",
            country="CL",
            coupon_code=None,
        )

        self.assertTrue(result.startswith("OK:"))

        fraud.score.assert_called_once()
        payments.charge.assert_called_once()
        repo.save.assert_called_once()
        email.send_receipt.assert_called_once()

class TestCheckoutServiceEmptyCart(unittest.TestCase):
	def test_checkout_empty_cart(self):
		payments = Mock()
		email = Mock()
		fraud = Mock()
		repo = Mock()

		checkout = CheckoutService(
			payments=payments,
			email=email,
			fraud=fraud,
			repo=repo,
		)

		items = [CartItem("A", 10000, -2)]

		result = checkout.checkout(
			user_id="u1",
			items=items,
			payment_token="tok_visa",
			country="CL",
			coupon_code=None,
		)

		self.assertRaises(PricingError)
    
class TestCheckoutServiceInvalidUser(unittest.TestCase):
	def test_checkout_invalid_user(self):
		payments = Mock()
		email = Mock()
		fraud = Mock()
		repo = Mock()

		fraud.score.return_value = 10
		payments.charge.return_value = ChargeResult(ok=True, charge_id="ch_123")

		checkout = CheckoutService(
			payments=payments,
			email=email,
			fraud=fraud,
			repo=repo,
		)

		items = [CartItem("A", 10000, 2)]

		result = checkout.checkout(
			user_id="",
			items=items,
			payment_token="tok_visa",
			country="CL",
			coupon_code=None,
		)

		self.assertEqual(result, "INVALID_USER")
	
	def test_checkout_invalid_user_whitespace(self):
		payments = Mock()
		email = Mock()
		fraud = Mock()
		repo = Mock()

		fraud.score.return_value = 10
		payments.charge.return_value = ChargeResult(ok=True, charge_id="ch_123")

		checkout = CheckoutService(
			payments=payments,
			email=email,
			fraud=fraud,
			repo=repo,
		)

		items = [CartItem("A", 10000, 2)]

		result = checkout.checkout(
			user_id="   ",
			items=items,
			payment_token="tok_visa",
			country="CL",
			coupon_code=None,
		)

		self.assertEqual(result, "INVALID_USER")
            
class TestCheckoutServiceElevatedFraudScore(unittest.TestCase):
	def test_checkout_high_fraud_score(self):
		payments = Mock()
		email = Mock()
		fraud = Mock()
		repo = Mock()

		fraud.score.return_value = 81

		checkout = CheckoutService(
			payments=payments,
			email=email,
			fraud=fraud,
			repo=repo,
		)

		items = [CartItem("A", 10000, 2)]

		result = checkout.checkout(
			user_id="u1",
			items=items,
			payment_token="tok_visa",
			country="CL",
			coupon_code=None,
		)

		self.assertEqual(result, "REJECTED_FRAUD")

class TestCheckoutServicePaymentFailure(unittest.TestCase):
	def test_checkout_payment_failure(self):
		payments = Mock()
		email = Mock()
		fraud = Mock()
		repo = Mock()

		fraud.score.return_value = 10
		payments.charge.return_value = ChargeResult(ok=False, reason="Contact bank")

		checkout = CheckoutService(
			payments=payments,
			email=email,
			fraud=fraud,
			repo=repo,
		)

		items = [CartItem("A", 10000, 2)]

		result = checkout.checkout(
			user_id="u1",
			items=items,
			payment_token="tok_visa",
			country="CL",
			coupon_code=None,
		)

		self.assertEqual(result, "PAYMENT_FAILED:Contact bank")

class TestCheckoutServiceInvalidCart(unittest.TestCase):
	def test_checkout_invalid_cart(self):
		payments = Mock()
		email = Mock()
		fraud = Mock()
		repo = Mock()

		checkout = CheckoutService(
			payments=payments,
			email=email,
			fraud=fraud,
			repo=repo,
		)

		items = [CartItem("A", -10000, 2)]

		result = checkout.checkout(
			user_id="u1",
			items=items,
			payment_token="tok_visa",
			country="CL",
			coupon_code=None,
		)

		self.assertTrue(result.startswith("INVALID_CART:"))
        
	
class TestCheckoutServiceValidPayment(unittest.TestCase):
	def test_checkout_valid_payment(self):
		payments = Mock()
		email = Mock()
		fraud = Mock()
		repo = Mock()

		fraud.score.return_value = 10
		payments.charge.return_value = ChargeResult(ok=True, charge_id="ch_123")

		checkout = CheckoutService(
			payments=payments,
			email=email,
			fraud=fraud,
			repo=repo,
		)

		items = [CartItem("A", 10000, 2)]

		result = checkout.checkout(
			user_id="u1",
			items=items,
			payment_token="tok_visa",
			country="CL",
			coupon_code=None,
		)

		self.assertTrue(result.startswith("OK:"))
        
