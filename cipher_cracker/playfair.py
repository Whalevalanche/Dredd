"""
A plain text attack for PlayFair Cipher. Given plain text and corresponding
cipher, find the key of the PlayFair Cipher.

@author: Derek S. Prijatelj, Sean McShane
"""

import sys
from collections import OrderedDict
import numpy as np
import re
import math

def encrypt(key, txt, letter_overlap = ('E','F')):
    """
    Encrypts the code using Playfair cipher with the given key. doubles
    insertion and single's addition letter is 'Q'

    @param key: String of 25 unique letters
    @param txt: String of plain text  to encrypt
    @param letter_overlap: tuple of two characters. The first is to be replaced
    by the second in the plain text, to account for the playfair cipher's pair
    letter overlap. E to F, to mask the most common letter with its least common
    nearest neighbor in the ordered alphabet.
    """
    key = key.upper()
    txt = txt.upper().replace(letter_overlap[0], letter_overlap[1])
    key_unique = ''.join(OrderedDict.fromkeys(key).keys())
    key_matrix = []
    if len(key_unique) < 25:
        # TODO Not provided with the full key, thus need to guess or use known
        # letter_overlap
        key_unique += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        key_unique = ''.join(OrderedDict.fromkeys(key_unique).keys())
    elif len(key_unique) > 25:
        raise Exception("Given Key is greater than 25 unique characters")
    else:
        # The key is fully provided
        key_matrix = np.reshape(np.array(list(key_unique)), [5,5])
    if len(key_matrix) == 0:
        return '';
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
  '''
    key_matrix = np.zeros((5,5), dtype = np.str)
    regex = re.compile('[^a-zA-Z]');

    plain_text = regex.sub('', plain_text);
    plain_text = insert_letter(plain_text);
    cipher_text = regex.sub('', cipher_text);

    plain_text = plain_text.lower();
    cipher_text = cipher_text.lower();

    digraph_dict = OrderedDict([]);

    print 'PLAIN TEXT: ' + plain_text
    print 'CIPHER TEXT: ' + cipher_text

    #string length must be even
    for i in range(len(plain_text)):
    	if i % 2 != 0:
    		continue;
    	digraph_dict[plain_text[i:i+2]] = cipher_text[i:i+2];

    reocc_list = find_reoccurrences(digraph_dict);
    for trigraph in reocc_list:
        for key in digraph_dict:
            #trigraph must appear horizontally with digraph below
            if trigraph[1] == key[0] and trigraph[0] == digraph_dict[key][0]:
                key_matrix = add_to_matrix("trigraph h", key_matrix, reocc_list,
                    trigraph, key[1] + digraph_dict[key][1]);
            if trigraph[1] == key[0] and trigraph[2] == digraph_dict[key][0]:
                key_matrix = add_to_matrix("trigraph h", key_matrix, reocc_list,
                    trigraph, digraph_dict[key][1] + key[1]);
            if trigraph[2] == key[1] and trigraph[0] == digraph_dict[key][1]:
                key_matrix = add_to_matrix("trigraph h", key_matrix, reocc_list,
                    trigraph, key[0] + ' ' + digraph_dict[key][0]);
            if trigraph[2] == key[1] and trigraph[1] == digraph_dict[key][1]:
                key_matrix = add_to_matrix("trigraph h", key_matrix, reocc_list,
                    trigraph, key[0] + digraph_dict[key][0]);

    for key in digraph_dict:
        for j in range(2):
            row, col = np.where(key_matrix == key[j]);
            if len(col) == 1:
                for i in range(5):
                    if key_matrix[i, col[0]] == digraph_dict[key][0]:
                        row2, col2 = np.where(key_matrix == key[j%1]);
                        if len(row2) == 1:
                            if j == 0:
                                key_matrix = add_to_matrix('special matching digraph',
                                key_matrix,None, digraph_dict[key][1], None, [i, col2[0]]);
                            else:
                                key_matrix = add_to_matrix('special matching digraph',
                                key_matrix,None, digraph_dict[key][1], None, [row[0], col2[0]]);
                        else:
                            key_matrix = add_to_matrix("matching digraph", key_matrix,
                            None, digraph_dict[key][1] + key[1], None, [i, row[0]]);
                    if key_matrix[i, col[0]] == digraph_dict[key][1]:
                        key_matrix = add_to_matrix("matching digraph", key_matrix,
                            None, digraph_dict[key][0] + key[1], None, [i, row[0]]);


    key = hail_mary(key_matrix, plain_text, cipher_text);
    print 'SECRET KEY: ' + key;


"""
find what letters this letter in plain/cipher maps to in cipher/plain
returns:
    mappings[0] = what letter encrypts to
    mappings[1] = what letter decrypts to
"""
def find_ind_mappings(letter, plain_text, cipher_text):
    mappings = [[], []];
    inds = [pos for pos, char in enumerate(plain_text) if char == letter]
    for ind in inds:
        mappings[0].append(cipher_text[ind]);
    mappings[0] = list(set(mappings[0]));
    inds = [pos for pos, char in enumerate(cipher_text) if char == letter]
    for ind in inds:
        mappings[1].append(plain_text[ind]);
    mappings[1] = list(set(mappings[1]));

    return mappings;

#find digraphs that share letters in plain/cipher, i.e. : to => op
def find_reoccurrences(digraph_dict):
    reoccurrences = [];
    for key in digraph_dict:
	    if key[0].lower() ==  digraph_dict[key][1].lower():
		    reoccurrences.append(key[1] + key[0] + digraph_dict[key][0]);
	    elif key[1].lower() ==  digraph_dict[key][0].lower():
		    reoccurrences.append(key + digraph_dict[key][1]);
    return reoccurrences;

def add_to_matrix(indicator, key_matrix, trigraph_list, str1, str2, meta=None):
   # print key_matrix, str1, str2
    if indicator == "trigraph h":
        for trigraph in trigraph_list:
            if len(str2) == 2:
                if str2 in trigraph or (str2[0] == trigraph[0] and str2[1] == trigraph[2]):
                    str2 = trigraph;
                    break;
            elif len(str2) == 3:
                if str2[0] == trigraph[0] and str2[2] == trigraph[2]:
                    str2 = trigraph;
                    break;
        row = next_empty_row(key_matrix);
        col = next_empty_col(key_matrix,row);
        if not row == -1 and not col == -1:
            if not in_matrix(key_matrix, str1):
                for c in str1:
                    key_matrix[row,col] = c;
                    col += 1;
                col = col - len(str1);
            if not in_matrix(key_matrix, str2):
                row = next_empty_row(key_matrix);
                for c in str2:
                    key_matrix[row,col] = c;
                    col += 1;
    elif indicator == 'matching digraph':
        flag = True;
        for i in range(2):
            row, col = np.where(key_matrix == str1[i]);
            if len(row) == 1:
                row2, col2 = np.where(key_matrix == str1[i%2]);
                if not len(row2) == 1:
                    flag = False;
                    if key_matrix[meta[0], col[0]] == '' or key_matrix[meta[0], col[0]] == ' ':
                        key_matrix[meta[0], col[0]] = str1[i%2];
                    else:
                        new_col = next_empty_col(key_matrix, meta[0]);
                        if not new_col == -1:
                            key_matrix[meta[0], new_col] = key_matrix[meta[0], col[0]];
                            key_matrix[meta[0], col[0]] = str1[i%2];
        if flag:
            row, col = np.where(key_matrix == str1[0]);
            row2, col2 = np.where(key_matrix == str1[1]);

            new_col = next_empty_col(key_matrix, meta[0]);
            new_col2 = next_empty_col(key_matrix, meta[1]);

            if new_col < new_col2:
                new_col = new_col2;

            if not col == -1 and len(row) == 0 and len(row2) == 0:
                key_matrix[meta[1], new_col] = str1[0];
                key_matrix[meta[0], new_col] = str1[1];
                global added_digraphs;
                added_digraphs.append(str1);
    elif indicator == 'special matching digraph':
        row, col = np.where(key_matrix == str1);
        if len(row) == 0:
            if key_matrix[meta[0], meta[1]] == '' or key_matrix[meta[0], meta[1]] == ' ':
                key_matrix[meta[0], meta[1]] = str1;
            else:
                new_col = next_empty_col(key_matrix, meta[0], meta[1]);
                if not new_col == -1:
                    key_matrix[meta[0], new_col] = key_matrix[meta[0], meta[1]];
                    key_matrix[meta[0], meta[1]] = str1;
                    for digraph in added_digraphs:
                        if key_matrix[meta[0], new_col] in digraph:
                            move_char = digraph[digraph.index(key_matrix[meta[0], new_col]) % 1];
                            row, col = np.where(key_matrix == move_char);
                            if key_matrix[row[0], new_col] == '' or key_matrix[row[0], new_col] == ' ':
                                key_matrix[row[0], new_col] = move_char;
                                key_matrix[row[0], col[0]] = '';
                            else:
                                new_col2 = next_empty_col(key_matrix, row[0]);
                                if not new_col2 == -1:
                                    key_matrix[row[0], new_col2] = key_matrix[row[0], meta[1]];
                                    key_matrix[row[0], new_col] = move_char;
    return key_matrix;

def next_empty_row(key_matrix):
    for row in range(5):
        if key_matrix[row,0] == '' or key_matrix[row,0] == ' ':
            return row;
    return -1;

def next_empty_col(key_matrix, row, start_at = 0):
    for col in range(start_at,5):
        if key_matrix[row,col] == '' or key_matrix[row,col] == ' ':
            return col;
    return -1;

def in_matrix(key_matrix, string):
    row,col = np.where(key_matrix == string[0]);
    if len(row) == 1:
        return True;
        string = string[1:];
        for c in string:
            try:
                if key_matrix[row, col + 1] == c:
                    col += 1;
                elif key_matrix[row + 1, col] == c:
                    row += 1;
                else:
                    return False;
            except:
                print 'out of bounds';
    else:
        return False;
    return True;

def hail_mary(key_matrix, plaintext, ciphertext):
    alpha = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    unknowns = []
    for row in range(5):
        for col in range(5):
            if key_matrix[row,col] == '' or key_matrix[row,col] == ' ':
                unknowns.append([row,col]);

    key = '';
    for el in np.nditer(key_matrix):
        if str(el) == '' or str(el) == ' ':
            el = '?'
        key += str(el);
    for c in key:
        try:
            if alpha.index(c) >= 0:
                alpha.remove(c);
        except ValueError:
            continue;
    idx = 0;
    idx2 = 1;
    cnt_idx = 1;
    for j in range(math.factorial(len(alpha))):
        for unknown in unknowns:
            if idx >= len(alpha):
                break;
            key_matrix[unknown[0], unknown[1]] = alpha[idx];

            #fill rest of matrix
            for i in range(len(alpha) - 1):
                if idx2 >= len(alpha) - 1 or cnt_idx >= len(alpha) - 1:
                    idx2 = 0;
                    cnt_idx = 0;
                if alpha[i] == alpha[idx]:
                    continue;
                else:
                    key_matrix[unknowns[cnt_idx][0], unknowns[cnt_idx][1]] = alpha[idx2];
                    idx2 += 1;
                    cnt_idx +=1;

            key = create_key(key_matrix);
            if idx == 0:
                b_key = key;

            try:
                if encrypt(key, plaintext).lower() == ciphertext.lower():
                    return key;

            except KeyError as e:
                continue;

            else:
                for row in range(5):
                    np.roll(key_matrix, 1);
                    key = create_key(key_matrix);
                    if encrypt(key, plaintext).lower() == ciphertext.lower():
                        return key;
                    for col in range(5):
                        key_matrix[:, [row, col]] = key_matrix[:, [col,row]];
                        key = create_key(key_matrix);
                        if encrypt(key, plaintext).lower() == ciphertext.lower():
                            return key;
            idx += 1;
            idx2 = idx + 1;
            cnt_idx = idx2;

    return b_key;

def create_key(key_matrix):
    key = '';
    for el in np.nditer(key_matrix):
        key += str(el);
    return key;
added_digraphs = [];

plaintext_file = open('plain.txt');
plaintext = plaintext_file.read();

ciphertext_file = open('cipher.txt');
ciphertext = ciphertext_file.read();

crack(plaintext, ciphertext);


def insert_letter(txt, letter='Q'):
    """
    Inserts the specified letter (default = 'Q')
    """
    idx = []
    offset = 0
    for i, c in enumerate(txt):
        if i == 0:
            continue
        if txt[i-1] == c and (i+offset)%2 != 0:
            idx += [i]
            offset += 1

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
    encryption = encrypt(key, txt, ('Z', 'Y'))
    expected = "MJJCUXFCPYQR"
    print(txt)
    print(encryption)
    print(encryption == expected, "\n")


    txt = "abcdefghijklmnopqrstuvwxyz"
    encryption = encrypt(key, txt, ('Z', 'Y'))
    expected = "bcdeajhijflmnoktrstpvwxyvtvt".upper()
    print(txt)
    print(encryption)
    print(encryption == expected, "\n")

    txt = "afkpuyyythmns"
    encryption = encrypt(key, txt, ('Z', 'Y'))
    expected = "fkpuvuvteymrsx".upper()
    print(txt)
    print(encryption)
    print(encryption == expected)

    txt = "yyyy"
    encryption = encrypt(key, txt, ('Z', 'Y'))
    expected = "vtvtvtvt".upper()
    print(txt)
    print(encryption)
    print(encryption == expected, "\n")

    txt2 = "zzzz"
    encryption2 = encrypt(key, txt2, ('Z', 'Y'))
    print(txt2)
    print(encryption2)
    print(encryption2 == expected, "\n")

if __name__ == "__main__":
    main(sys.argv)
