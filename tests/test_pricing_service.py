import unittest
from unittest.mock import Mock

from src.models import CartItem, Order
from src.pricing import PricingService, PricingError

class TestPricingService(unittest.TestCase):
	def test1(self):
		p = PricingService()
		items = [
			CartItem("A", 1000, 2),  # $20.00
			CartItem("B", 500, 1),   # $5.00
		]
		subtotal = p.subtotal_cents(items)
		self.assertEqual(subtotal, 2500)
	
	def test2(self):
		p = PricingService()
		items = [
			CartItem("A", 1000, 2),  # $20.00
			CartItem("B", 500, 1),   # $5.00
		]
		subtotal = p.subtotal_cents(items)
		net_subtotal = p.apply_coupon(subtotal, "SAVE10")
		self.assertEqual(net_subtotal, 2250)

	def test3(self):
		p = PricingService()
		items = [
			CartItem("A", 1000, 2),
			CartItem("B", 500, 1),
		]
		subtotal = p.subtotal_cents(items)
		net_subtotal = p.apply_coupon(subtotal, "CLP2000")
		self.assertEqual(net_subtotal, 500)

	def test4(self):
		p = PricingService()
		items = [CartItem("A", 1000, -2),
		]
		self.assertRaises(PricingError, p.subtotal_cents, items)
	
	def test5(self):
		p = PricingService()
		items = [CartItem("A", -1000, 2),
		]
		self.assertRaises(PricingError, p.subtotal_cents, items)

	def test6(self):
		p = PricingService()
		items = [
			CartItem("A", 1000, 2),
			CartItem("B", 500, 1),
		]
		subtotal = p.subtotal_cents(items)
		net_subtotal = p.apply_coupon(subtotal, '')
		self.assertEqual(net_subtotal, net_subtotal)

	def test7(self):
		p = PricingService()
		items = [
			CartItem("A", 1000, 2),
			CartItem("B", 500, 1),
		]
		subtotal = p.subtotal_cents(items)
		self.assertRaises(PricingError, p.apply_coupon, subtotal, 'Testing')

	def test8(self):
		p = PricingService()
		tax_cl = p.tax_cents(10000, 'CL')
		self.assertEqual(tax_cl, 1900)

	def test9(self):
		p = PricingService()
		tax_us = p.tax_cents(10000, 'US')
		self.assertEqual(tax_us, 0)

	def test10(self):
		p = PricingService()
		tax_eu = p.tax_cents(10000, 'EU')
		self.assertEqual(tax_eu, 2100)
	
	def test11(self):
		p = PricingService()
		self.assertRaises(PricingError, p.tax_cents, 5000, 'AU')

	def test12(self):
		p = PricingService()
		shipping_cl_1 = p.shipping_cents(25000, 'CL')
		self.assertEqual(shipping_cl_1, 0)
		
	def test13(self):
		p = PricingService()	
		shipping_cl_2 = p.shipping_cents(15000, 'CL')
		self.assertEqual(shipping_cl_2, 2500)
	
	def test14(self):
		p = PricingService()	
		shipping_us = p.shipping_cents(15000, 'US')
		self.assertEqual(shipping_us, 5000)

	def test15(self):
		p = PricingService()	
		shipping_eu = p.shipping_cents(15000, 'EU')
		self.assertEqual(shipping_eu, 5000)

	def test16(self):
		p = PricingService()	
		self.assertRaises(PricingError, p.shipping_cents, 15000, 'AU')
	
	def test17(self):
		p = PricingService()	
		items = [
			CartItem("A", 1000, 2),
			CartItem("B", 500, 1),
		]
		sub = p.subtotal_cents(items)
		net = p.apply_coupon(sub, "SAVE10")
		tax = p.tax_cents(net, "CL")
		shipping = p.shipping_cents(net, "CL")
		total = net + tax + shipping
		self.assertEqual(p.total_cents(items, "SAVE10", "CL"), total)
