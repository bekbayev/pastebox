from unittest import TestCase

from ..utils import make_random_string


class MakeRandomStringTest(TestCase):
    def test_positive_integer_length(self) -> None:
        """
        Length with a positive integer, returns a string of a given
        length.
        """
        for string_length in range(10):
            random_string = make_random_string(string_length)
            self.assertEquals(len(random_string), string_length)

    def test_negative_integer_length(self) -> None:
        """
        Length with a negative integer, returns an empty string.
        """
        for string_length in range(-10, 0):
            random_string = make_random_string(string_length)
            self.assertEquals(random_string, "")

    def test_chars_argument(self) -> None:
        """
        The returned string consists only of the given chars.
        """
        custom_chars = "Python+Django=🚀"
        random_string = make_random_string(chars=custom_chars, length=42)
        for char in random_string:
            self.assertNotIn(char, "ЯбЛокО🍎")
            self.assertIn(char, custom_chars)
