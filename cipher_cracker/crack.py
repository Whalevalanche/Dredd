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
                key_matrix = add_to_matrix("trigraph h",key_matrix,trigraph, key);
            if trigraph[1] == key[0] and trigraph[2] == digraph_dict[key][0]:
                key_matrix = add_to_matrix(


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
    print mappings;

#find digraphs that share letters in plain/cipher, i.e. : to => op
def find_reoccurrences(digraph_dict):
	reoccurrences = [];
	for key in digraph_dict:
		if key[0:1].lower() ==  digraph_dict[key][1:].lower():
			reoccurrences.append(key[1:] + key[0:1] + digraph_dict[key][1:]);
		elif key[1:].lower() ==  digraph_dict[key][0:1].lower():
			reoccurrences.append(key + digraph_dict[key][1:]);

def add_to_matrix(indicator, key_matrix, str1, str2):
    #TODO check to see if either are already in grid
    #TODO check to see if str2 is part of a trigraph
    if indicator == "trigraph h":
        row = next_empty_row(key_matrix);
        col = next_empty_col(key_matrix,row);

        for c in str1:
            key_matrix[row][col] = c;
            col += 1;
        row = next_empty_row(key_matrix);;
        col = col - len(str1);
        for c in str2:
            key_matrix[row][col];
            col += 1;

crack('commander in chief fleet to naval headquarter',
        'BPLYKRLHFEKIDBNFVUVIVZHZOPKERVNDFVLXWFESFE');
