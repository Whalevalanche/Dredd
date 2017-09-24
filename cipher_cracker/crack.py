import re
import numpy as np
from playfair import insert_letter

def crack(plain_text, cipher_text):
    key_matrix = np.empty([5,5])

    regex = re.compile('[^a-zA-Z]');

    plain_text = regex.sub('', plain_text);
    plain_text = insert_letter(plain_text);
    cipher_text = regex.sub('', cipher_text);

    plain_text = plain_text.lower();
    cipher_text = cipher_text.lower();

    digraph_dict = {};

    print plain_text
    print cipher_text
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

    print key_matrix;
    #find_ind_mappings('e', plain_text, cipher_text);


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

#find digraphs that share letters in plain/cipher, i.e. : to => op
def find_reoccurrences(digraph_dict):
    reoccurrences = [];
    for key in digraph_dict:
	    if key[0:1].lower() ==  digraph_dict[key][1:].lower():
		    reoccurrences.append(key[1:] + key[0:1] + digraph_dict[key][1:]);
	    elif key[1:].lower() ==  digraph_dict[key][0:1].lower():
		    reoccurrences.append(key + digraph_dict[key][1:]);
    return reoccurrences;

def add_to_matrix(indicator, key_matrix, trigraph_list, str1, str2):
    #TODO check to see if either are already in grid
    if indicator == "trigraph h":
        for trigraph in trigraph_list:
            if str2 in trigraph:
                str2 = trigraph;
        row = next_empty_row(key_matrix);
        col = next_empty_col(key_matrix,row);
        if not row == -1 and not col == -1:
            for c in str1:
                key_matrix[row][col] = c;
                col += 1;
            row = next_empty_row(key_matrix);
            col = col - len(str1);
            for c in str2:
                key_matrix[row][col];
                col += 1;

def next_empty_row(key_matrix):
    for row in range(5):
        for col in range(5):
            if not type(key_matrix[row][col]).__name__ == 'numpy.float64':
                return row;
    return -1;

def next_empty_col(key_matrix, row):
    for col in range(5):
        if not type(key_matrix[row][col]).__name__ == 'numpy.float64':
            return col;
    return -1;

crack('EXAMPLEAQUICKBROWNFOXIUMPSOVERTHELAZYDOG',
      'CZBLLMABRQHDGETMXMILYHRPNULYBUSIAPEVDIMI');
