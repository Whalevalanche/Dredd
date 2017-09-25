import re
import math
import numpy as np
from playfair import insert_letter
from playfair import encrypt
from collections import OrderedDict

def crack(plain_text, cipher_text):
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

