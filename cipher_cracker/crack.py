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
               # print '1 ' + key[1] + ' ' + digraph_dict[key][1]
            if trigraph[1] == key[0] and trigraph[2] == digraph_dict[key][0]:
                key_matrix = add_to_matrix("trigraph h", key_matrix, reocc_list,
                    trigraph, digraph_dict[key][1] + key[1]);
               # print '2 ' + digraph_dict[key][1] + ' ' + key[1]
            if trigraph[2] == key[1] and trigraph[0] == digraph_dict[key][1]:
                key_matrix = add_to_matrix("trigraph h", key_matrix, reocc_list,
                    trigraph, key[0] + ' ' + digraph_dict[key][0]);
               # print '3 ' + key[0] + ' ' + digraph_dict[key][0]
            if trigraph[2] == key[1] and trigraph[1] == digraph_dict[key][1]:
                key_matrix = add_to_matrix("trigraph h", key_matrix, reocc_list,
                    trigraph, key[0] + digraph_dict[key][0]);
               # print '4 ' + key[0] + ' ' + digraph_dict[key][0]

    for key in digraph_dict:
        for j in range(2):
            row, col = np.where(key_matrix == key[j]);
            if len(col) == 1:
                for i in range(5):
                    if key_matrix[i, col[0]] == digraph_dict[key][0]:
                        key_matrix = add_to_matrix("matching digraph", key_matrix,
                            None, digraph_dict[key][1] + key[1], None, [i, row[0]]);
                        print '1 ' + key + ' ' + digraph_dict[key];
                    if key_matrix[i, col[0]] == digraph_dict[key][1]:
                        key_matrix = add_to_matrix("matching digraph", key_matrix,
                            None, digraph_dict[key][0] + key[1], None, [i, row[0]]);
                        print '2 ' + key + ' ' + digraph_dict[key];
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
        print str1, meta;
        flag = True;
        for i in range(2):
            row, col = np.where(key_matrix == str1[i]);
            if len(row) == 1:
                row2, col2 = np.where(key_matrix == str1[i%2]);
                if not len(row2) == 1:
                    flag = False;
                    if key_matrix[meta[0], col] == '' or key_matrix[meta[0], col] == ' ':
                        key_matrix[meta[0], col] = str1[i%2];
                        print 'added 1'
                        print key_matrix;
                    else:
                        new_col = next_empty_col(key_matrix, meta[0]);
                        if not col == -1:
                            key_matrix[meta[0], new_col] = key_matrix[meta[0], col];
                            key_matrix[meta[0], col] = str1[i%2];
                            print 'added 2'
                            print key_matrix;
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
                print 'added 3'
                print key_matrix;

    return key_matrix;

def next_empty_row(key_matrix):
    for row in range(5):
        if key_matrix[row,0] == '' or key_matrix[row,0] == ' ':
            return row;
    return -1;

def next_empty_col(key_matrix, row):
    for col in range(5):
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
            #TODO
            except:
                print 'out of bounds';
    else:
        return False;
    return True;
crack('EXAMPLEAQUICKBROWNFOXIUMPSOVERTHELAZYDOG',
      'CZBLLMABRQHDGETMXMILYHRPNULYBUSIAPEVDIMI');
