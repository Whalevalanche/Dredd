"""
A plain text attack for PlayFair Cipher. Given plain text and corresponding
cipher, find the key of the PlayFair Cipher.

@author: Derek S. Prijatelj
"""

import sys
from collections import OrderedDict
import numpy as np

def encrypt(key, txt, letter_overlap = None):
    """
    Encrypts the code using Playfair cipher with the given key. doubles
    insertion and single's addition letter is 'Q'

    @param key: String of 25 unique letters
    """
    key = key.upper()
    txt = txt.upper()
    key_unique = ''.join(OrderedDict.fromkeys(key).keys())

    if len(key_unique) < 25:
        # TODO Not provided with the full key, thus need to guess or use known
        # letter_overlap
        key_unique += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key_unique = ''.join(OrderedDict.fromkeys(key_unique).keys())
    elif len(key_unique) > 25:
        raise Exception("Given Key is greater than 25 unique characters")
    else:
        # The key is fully provided
        # pick which alpha ordered letters to overlap: most freq = "st" or "ef"
        #   most common digraph OR most common letter w/ its most common digraph
        key_matrix = np.reshape(np.array(list(key_unique)), [5,5])

    # get set of digraphs from plain text
    #string length must be even
    txt_digraph = Set()

    # modify plain text to include 'Q' in between doubles and at end if odd
    txt = convert_dubs(txt)
    if len(txt % 2 != 0:
        txt += 'Q'

    for i in range(len(txt)):
        if i % 2 != 0:
            continue;
        txt_digraph.add(txt[i:i+2]]);

    # for each unique digraph, get new mapping (create dict)


    #convert string based on dict

    return encryption

def decrypt():
    """
    Decrypts the provided cipher with the given key.
    """

def insert_letter(txt, letter = 'Q'):
    idx = []
    for i, c in enumerate(txt):
        if i == 0:
            continue
        if txt[i-1] == c:
            idx += [i]

    offset = 0
    for i in idx:
        txt = txt[:i+offset] + letter + txt[i+offset:]
        offset += 1

    if len(txt) % 2 != 0:
        txt += letter

    return txt

def main(args):
    """
    Given text file containing plain text and cipher, separated by new lines.
    """

if __name__ == "__main__":
    main(sys.args)
