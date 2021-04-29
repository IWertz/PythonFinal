"""
Program: test_customer.py
Author: Isaiah Wertz
Last date modified: 04/28/2021

The purpose of this program is to unit test the customer class
"""

import unittest
from final.cutsomer import Customer


class MyTestCase(unittest.TestCase):

    def test_customer_create(self):
        # Arrange
        customer = Customer("Isaiah", "Wertz", 19.00)
        expected = "Isaiah"
        # Act
        actual = customer.fname
        # Assert
        self.assertEqual(expected, actual)

    def test_customer_add_cart(self):
        # Arrange
        customer = Customer("Isaiah", "Wertz", 19.00)
        customer.add_cart(.07, 2.00, .50)
        expected = .07
        # Act
        actual = customer.cart.tax
        # Assert
        self.assertEqual(expected, actual)

    def test_customer_add_item(self):
        # Arrange
        customer = Customer("Isaiah", "Wertz", 19.00)
        customer.add_cart(.07, 2.00, .50)
        customer.cart.add_item("Milk", 2.29)
        expected = 2.29
        # Act
        actual = customer.cart.items["Milk"]
        # Assert
        self.assertEqual(expected, actual)

    def test_customer_check_out(self):
        # Arrange
        customer = Customer("Isaiah", "Wertz", 19.00)
        customer.add_cart(.07, 2.00, .50)
        customer.cart.add_item("Milk", 2.29)
        customer.check_out()
        expected = 14.91
        # Act
        actual = customer.balance
        # Assert
        self.assertEqual(expected, actual)
