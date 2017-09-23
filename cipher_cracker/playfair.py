"""
A plain text attack for PlayFair Cipher. Given plain text and corresponding
cipher, find the key of the PlayFair Cipher.

@author: Derek S. Prijatelj
"""

import sys
from collections import OrderedDict

def encrypt(key, txt, letter_overlap = None):
    """
    Encrypts the code using Playfair cipher with the given key.
    """
    key = key.upper()
    key_unique = ''.join(OrderedDict.fromkeys(key).keys())
    if len(key_unique) < 25:
        # TODO Not provided with the full key, thus need to guess or use known
        # letter_overlap

        # create playfair  5x5 table
        #key += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        alpha_key = ''.join(OrderedDict.fromkeys(key.upper()).keys())
    else if len(unique_key) > 25:
        raise Exception("Given Key is greater than 25 unique characters")

    if len(alpha_key) > 25:
        # There is single letter pair that overlaps
        # if letter_overlap = None, throw error or search for overlapping chars

        """
        TODO optimally, we should overlap, the alphabetical orderd pair, that
        is most common. To be assholes & if allowed, our key will use the most
        frequent digraph in all texts. Just trying to think how we
        """




    return encryption

def decrypt():
    """
    Decrypts the provided cipher with the given key.
    """

def crack(txt, cipher):
    """
    Given the plain text and the cipher, determines the key to the Playfair
    cipher. Does so by simulating the potential cipher matrix.
    """
    # TODO need to find appropriate algorithm to determine key based on digraphs

    # The key can be an assortment of 25 random and unique letters.

def main(args):
    """
    Given text file containing plain text and cipher, separated by new lines.
    """

if __name__ == "__main__":
    main(sys.args)
