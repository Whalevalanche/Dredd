"""
A plain text attack for PlayFair Cipher. Given plain text and corresponding
cipher, find the key of the PlayFair Cipher.

@author: Derek S. Prijatelj
"""

import sys
from collections import OrderedDict
import numpy as np
import re

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
    txt_digraph = set()

    # modify plain text to include 'Q' in between doubles and at end if odd
    txt = insert_letter(txt)

    for i in range(len(txt)):
        if i % 2 != 0:
            continue;
        txt_digraph.add(txt[i:i+2]);

    # for each unique digraph, get new mapping (create dict)
    index = {}
    for c in key_unique:
        idx = np.where(key_matrix == c)
        index[c] = (idx[0][0], idx[1][0])

    txt_digraph_encrypt = {}
    for digraph in txt_digraph:
        c1 = index[digraph[0]]
        c2 = index[digraph[1]]

        if c1[0] == c2[0] and c1[1] != c2[1]:
            # if same row, shift right once
            if c1[1] >= 4:
                e1 = key_matrix[c1[0]][0]
            else:
                e1 = key_matrix[c1[0]][c1[1]+1]

            if c2[1] >= 4:
                e2 = key_matrix[c2[0]][0]
            else:
                e2 = key_matrix[c2[0]][c2[1]+1]

        elif c1[0] != c2[0] and c1[1] == c2[1]:
            # if same col, shift down once
            if c1[0] >= 4:
                e1 = key_matrix[0][c1[1]]
            else:
                e1 = key_matrix[c1[0]+1][c1[1]]

            if c2[0] >= 4:
                e2 = key_matrix[0][c2[1]]
            else:
                e2 = key_matrix[c2[0]+1][c2[1]]

        elif c1[0] == c2[0] and c1[1] == c2[1]:
            raise Exception("Error in txt_digraph, There should be no doubles!")
        else:
            e1 = key_matrix[c1[0]][c2[1]]
            e2 = key_matrix[c2[0]][c1[1]]

        txt_digraph_encrypt[digraph] = e1 + e2

    #convert string based on dict
    pattern = re.compile('|'.join(txt_digraph_encrypt.keys()))
    encryption = pattern.sub(lambda x: txt_digraph_encrypt[x.group()], txt)

    return encryption

def decrypt():
    """
    Decrypts the provided cipher with the given key.
    """

def insert_letter(txt, letter='Q'):
    """
    Inserts the specified letter (default = 'Q')
    """
    idx = []
    for i, c in enumerate(txt):
        if i == 0:
            continue
        if txt[i-1] == c and i%2 != 0:
            idx += [i]

    offset = 0
    for i in idx:
        txt = txt[:i+offset] + letter + txt[i+offset:]
        offset += 1

    #Note, does not check if the last letter is the same as the inserted letter
    if len(txt) % 2 != 0:
        txt += letter
    return txt

def main(args):
    """
    Given text file containing plain text and cipher, separated by new lines.
    """
    key = "ABCDEFGHIJKLMNOPQRSTUVWXY"
    txt = "OhHeyWhatUp"
    encryption = encrypt(key, txt)
    expected = "MJJCUXFCPYQR"

    print(encryption)
    print(encryption == expected)

if __name__ == "__main__":
    main(sys.argv)
