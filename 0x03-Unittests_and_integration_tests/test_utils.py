#!/usr/bin/env python3
"""Unit tests for utils.access_nested_map function."""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, MagicMock



class TestAccessNestedMap(unittest.TestCase):
    """Test cases for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test access_nested_map returns the expected value."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "a"),
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map, path, expected_msg):
        """Test access_nested_map raises KeyError with correct message."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(context.exception.args[0], expected_msg)

class TestGetJson(unittest.TestCase):
    """Test cases for utils.get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")  # patch requests.get in utils module
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test that get_json returns expected payload without real HTTP call."""
        # Create a mock response with .json() returning test_payload
        mock_response = MagicMock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function
        result = get_json(test_url) 

        # Assert .get was called once with test_url
        mock_get.assert_called_once_with(test_url)

        # Assert the returned data matches test_payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    def test_memoize(self):

        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
            
        obj= TestClass()

        with patch.object(TestClass, 'a_method', return_value=42) as mock_method:
            result1 = obj.a_method

            result2 =obj.a_property
            result3=obj.a_property

            self.assertEqual(result2, 42)
            self.assertEqual(result3, 42)

            mock_method.assert_called_once_with()



if __name__ == "__main__":
    unittest.main()
