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

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_menu(self, mock_print):
        # fail test messages
        error_message = "\n\nThe function 'print_menu()' should print all the items in the menu dictionary."

        # initializing test data
        print_menu()
        output = mock_print.getvalue()
        
        # performing test
        for item in menu:
            self.assertIn(item, output, msg=error_message)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_originals(self, mock_print):
        # fail test messages
        error_message = "\n\nThe function 'print_originals()' should print the entire list of original flavors."

        # initializing test data
        print_originals()
        output = mock_print.getvalue()
        
        # performing test
        for item in original_flavors:
            self.assertIn(item, output, msg=error_message)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_signatures(self, mock_print):
        # fail test messages
        error_message = "\n\nThe function 'print_signatures()' should print the entire list of signature flavors."

        # initializing test data
        print_signatures()
        output = mock_print.getvalue()
        
        # performing test
        for item in signature_flavors:
            self.assertIn(item, output, msg=error_message)
    
    def test_is_valid_order(self):
        # fail test messages
        error_message = "\n\nThe function 'is_valid_order()' should return True if the order it received as an argument exists in the menu, signature flavors, or original flavors. It should return False otherwise."
        
        # initializing test data
        order_list_valid = [
            "tea",
            "coffee",
            "vanilla",
            "caramel",
            "chocolate",
            "raspberry",
            "strawberry",
            "bottled water",
            "original cupcake",
            "signature cupcake",
        ]

        order_list_invalid = [
            "sdfsdfs",
            "fmerlsiugnlrs",
            "lndksj nfsla",
        ]
        
        # performing test
        for order in order_list_valid:
            self.assertTrue(is_valid_order(order), msg=error_message)
       
        for order in order_list_invalid:
            self.assertFalse(is_valid_order(order), msg=error_message)

    def test_get_order(self):
        # fail test messages
        error_message = "\n\nThe function 'get_order()' should return a list of the correct orders the user has entered. Any incorrect orders the user enters should not be in the returned list of orders."

        # initializing test data
        user_input = signature_flavors + original_flavors + list(menu.keys()) + ['garbage', 'noting', 'hello', "Exit"]
        expected_output = signature_flavors + original_flavors + list(menu.keys())
        order_list = []
        with patch('builtins.input', side_effect=user_input):
            order_list = get_order()

        # performing test
        for item in expected_output:
            self.assertIn(item, order_list, msg=error_message)
    
    def test_accept_credit_card(self):
        # fail test messages
        error_message = "\n\nThe 'accept_credit_card()' function should only return True when the total price is greater than or equal to 5."

        # initializing test data
        big_price_list = [
            5,
            50,
            500,
            499,
        ]
        small_price_list = [
            4,
            0,
            -6,
        ]

        # performing test
        for price in big_price_list:
            self.assertTrue(accept_credit_card(price), msg=error_message)
        
        for price in small_price_list:
            self.assertFalse(accept_credit_card(price), msg=error_message)
        

    def test_get_total_price(self):
        # fail test messages
        error_message = "\n\nThe 'get_total_price()' function should return the total price of the order."

        # initializing test data
        total_price = len(signature_flavors)*signature_price + len(original_flavors)*original_price + menu['coffee'] + menu['tea'] + menu['bottled water']
        order_list = signature_flavors + original_flavors + ['coffee', 'tea', 'bottled water', 'Exit']
        
        returned_price = get_total_price(order_list)
        
        # performing test
        self.assertEqual(returned_price, total_price, msg=error_message)
        
    @patch('sys.stdout', new_callable=StringIO)
    def test_print_order(self, mock_print):
        # fail test messages
        total_price_msg = "\n\nThe 'print_order()' function should display the total price."
        cupcake_name_msg = "\n\nThe 'print_order()' function should display the cupcake shop name."
        
        # initializing test data
        total_price = len(signature_flavors)*signature_price + len(original_flavors)*original_price + menu['coffee'] + menu['tea'] + menu['bottled water']
        order_list = signature_flavors + original_flavors + ['coffee', 'tea', 'bottled water', 'Exit']
        output = ""
        
        print_order(order_list)
        output = mock_print.getvalue()
        
        # performing test
        for item in order_list:
            self.assertIn(item, output, msg="\n\nThe 'print_order()' function should display all the items the user has ordered.")
        
        self.assertIn(str(total_price), output, msg=total_price_msg)
        self.assertIn(cupcake_shop_name, output, msg=cupcake_name_msg)
