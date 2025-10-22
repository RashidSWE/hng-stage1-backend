import hashlib

def length(string: str) -> int:
    """
    Compute the length of a given string
    """
    return len(string)


def is_palindrome(string: str) -> bool:
    """
    Checks if a string is a palindrome or not

    returns:
        True - if is palindrome otherwise returns False
    """

    string = string.lower()
    return string == string[::-1]

def unique_characters(string: str) -> int:
    """
    returns count of distinct characters in a string
    """
    return len(set(string))

def word_count(string: str) -> int:
    """
    Returns number of words separated by space
    """
    # string = string.strip()

    # if not string:
    #     return 0

    # count = 1

    # for i in range(len(string)):
    #     if string[i] == " " and string[i - 1] !== " ":
    #         count += 1
    # return count

    words = string.split()
    return len(words)


def sha256_hash(string: str) -> int:
    """
    Returns SHA-256 hash of the string for unique identification
    """
    return hashlib.sha256(string.encode()).hexdigest()


def character_frequency_map(string: str) -> dict:
    """ Maps each character to it's occurrence count"""
    freq = {}

    for ch in string:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


