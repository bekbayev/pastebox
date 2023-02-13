from random import choice
from string import ascii_letters, digits


def make_random_string(length: int, chars: str = None) -> str:
    """Return a string of random `chars` with a given `length`.

    If no chars are given, the value will be a string of digits and
    ASCII letters.
    A negative integer for length will return an empty string.
    """
    chars = chars or f"{ascii_letters}{digits}"
    return "".join(choice(chars) for _ in range(length))
