import re
import numpy as np
from playfair import insert_letter

def crack(plain_text, cipher_text):
    key_matrix = np.zeros((5,5), dtype = np.str)
    print key_matrix
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
            #pass col num here as they must start at same
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

    return mappings;

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
    return key_matrix;

def next_empty_row(key_matrix):
    for row in range(5):
        if key_matrix[row,0] == '':
            return row;
    return -1;

def next_empty_col(key_matrix, row):
    for col in range(5):
        if key_matrix[row,col] == '':
            return col;
    return -1;

def in_matrix(key_matrix, string):
    row,col = np.where(key_matrix == string[0]);
    if len(row) == 1:
        string = string[1:];
        for c in string:
            try:
                if key_matrix[row, col + 1] == c:
                    col += 1;
                elif key_matrix[row + 1, col] == c:
                    row += 1;
                else:
                    return False;
            #TODO
            except:
                print 'out of bounds';
    else:
        return False;
    return True;
crack('EXAMPLEAQUICKBROWNFOXIUMPSOVERTHELAZYDOG',
      'CZBLLMABRQHDGETMXMILYHRPNULYBUSIAPEVDIMI');
