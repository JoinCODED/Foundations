from io import StringIO
import sys
import unittest
from mock import patch
from shop import (
    menu, 
    original_flavors,
    original_price,
    signature_price,
    cupcake_shop_name,
    signature_flavors,

    print_menu, 
    print_originals, 
    print_signatures,
    is_valid_order,
    get_order,
    accept_credit_card,
    get_total_price,
    print_order
)

class TestShopMethods(unittest.TestCase):

    def test_print_menu(self):
        capturedOutput = StringIO()                   # Create StringIO object
        sys.stdout = capturedOutput                   #  and redirect stdout.
        print_menu()                                  # Call unchanged function.
        sys.stdout = sys.__stdout__                   # Reset redirect.
        output = capturedOutput.getvalue()
        
        for item in menu:
            self.assertIn(item, output, msg="\n\nThe function 'print_menu()' should print all the items in the menu dictionary.")

    def test_print_originals(self):
        capturedOutput = StringIO()                   # Create StringIO object
        sys.stdout = capturedOutput                   #  and redirect stdout.
        print_originals()                             # Call unchanged function.
        sys.stdout = sys.__stdout__                   # Reset redirect.
        output = capturedOutput.getvalue()
        
        for item in original_flavors:
            self.assertIn(item, output, msg="\n\nThe function 'print_originals()' should print the entire list of original flavors.")

    def test_print_signatures(self):
        capturedOutput = StringIO()                   # Create StringIO object
        sys.stdout = capturedOutput                   #  and redirect stdout.
        print_signatures()                            # Call unchanged function.
        sys.stdout = sys.__stdout__                   # Reset redirect.
        output = capturedOutput.getvalue()
        
        for item in signature_flavors:
            self.assertIn(item, output, msg="\n\nThe function 'print_signatures()' should print the entire list of signature flavors.")
    
    def test_is_valid_order(self):
        errmsg = "\n\nThe function 'is_valid_order()' should return True if the order it received as an argument exists in the menu, signature flavors, or original flavors. It should return False otherwise."
        self.assertTrue(is_valid_order("tea"), msg=errmsg)
        self.assertTrue(is_valid_order("coffee"), msg=errmsg)
        self.assertTrue(is_valid_order("vanilla"), msg=errmsg)
        self.assertTrue(is_valid_order("caramel"), msg=errmsg)
        self.assertTrue(is_valid_order("chocolate"), msg=errmsg)
        self.assertTrue(is_valid_order("raspberry"), msg=errmsg)
        self.assertTrue(is_valid_order("strawberry"), msg=errmsg)
        self.assertTrue(is_valid_order("bottled water"), msg=errmsg)
        self.assertTrue(is_valid_order("original cupcake"), msg=errmsg)
        self.assertTrue(is_valid_order("signature cupcake"), msg=errmsg)

        self.assertFalse(is_valid_order("sdfsdfs"), msg=errmsg)
        self.assertFalse(is_valid_order("fmerlsiugnlrs "), msg=errmsg)
        self.assertFalse(is_valid_order("lndksj nfsla"), msg=errmsg)

    @patch('shop.get_order.input', create=True)
    def test_get_order(self, magic_mock_object):
        user_input = signature_flavors + original_flavors + list(menu.keys()) + ['garbage', 'noting', 'hello', "Exit"]
        expected_output = signature_flavors + original_flavors + list(menu.keys())
        order_list = []
        with patch('builtins.input', side_effect=user_input):
            order_list = get_order()

        for item in expected_output:
            self.assertIn(item, order_list, msg="\n\nThe function 'get_order()' should return a list of the correct orders the user has entered. Any incorrect orders the user enters should not be in the returned list of orders.")
    
    def test_accept_credit_card(self):
        self.assertTrue(accept_credit_card(5), msg="\n\nThe 'accept_credit_card()' function should only return True when the total price is greater than or equal to 5.")
        self.assertTrue(accept_credit_card(50), msg="\n\nThe 'accept_credit_card()' function should only return True when the total price is greater than or equal to 5.")
        self.assertTrue(accept_credit_card(500), msg="\n\nThe 'accept_credit_card()' function should only return True when the total price is greater than or equal to 5.")
        self.assertTrue(accept_credit_card(499), msg="\n\nThe 'accept_credit_card()' function should only return True when the total price is greater than or equal to 5.")
        self.assertFalse(accept_credit_card(4), msg="\n\nThe 'accept_credit_card()' function should only return True when the total price is greater than or equal to 5.")
        self.assertFalse(accept_credit_card(0), msg="\n\nThe 'accept_credit_card()' function should only return True when the total price is greater than or equal to 5.")
        self.assertFalse(accept_credit_card(-6), msg="\n\nThe 'accept_credit_card()' function should only return True when the total price is greater than or equal to 5.")

    def test_get_total_price(self):
        total_price = len(signature_flavors)*signature_price + len(original_flavors)*original_price + menu['coffee'] + menu['tea'] + menu['bottled water']
        order_list = signature_flavors + original_flavors + ['coffee', 'tea', 'bottled water', 'Exit']
        
        returned_price = get_total_price(order_list)
        
        self.assertEqual(returned_price, total_price, msg="\n\nThe 'get_total_price()' function should return the total price of the order.")
        
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_order(self, mock_stdout):
        total_price = len(signature_flavors)*signature_price + len(original_flavors)*original_price + menu['coffee'] + menu['tea'] + menu['bottled water']
        order_list = signature_flavors + original_flavors + ['coffee', 'tea', 'bottled water', 'Exit']
        output = ""
        
        print_order(order_list)
        output = mock_stdout.getvalue()
        
        for item in order_list:
            self.assertIn(item, output, msg="\n\nThe 'print_order()' function should display all the items the user has ordered.")
        
        self.assertIn(str(total_price), output, msg="\n\nThe 'print_order()' function should display the total price.")
        self.assertIn(cupcake_shop_name, output, msg="\n\nThe 'print_order()' function should display the cupcake shop name.")
