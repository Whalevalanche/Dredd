"""
Helper functions to cracking the playfair cipher in a plain text attack.
"""

def find_ind_mappings(letter, plain_text, cipher_text):
    """
    find what letters this letter in plain/cipher maps to in cipher/plain
    returns:
        mappings[0] = what letter encrypts to
        mappings[1] = what letter decrypts to
    """
    mappings = [[], []];
    inds = [pos for pos, char in enumerate(plain_text) if char == letter]
    for ind in inds:
        mappings[0].append(cipher_text[ind]);
    mappings[0] = list(set(mappings[0]));
    inds = [pos for pos, char in enumerate(cipher_text) if char == letter]
    for ind in inds:
        mappings[1].append(plain_text[ind]);
    mappings[1] = list(set(mappings[1]));

def find_shared_rowcol(digraph_dict):
    """
    Finds eash letter's shared row OR column in the unknown key matrix. The
    total letters in each row & col should never excede 8. TODO assert this.

    @param digraph_dict: key: plain_digraphs to cipher_digraphs

    @return: dict of letter to list of letters that are in the same row OR
        column. Note, the list will never have more than 8 characters
    """
    shared_rowcol = {}

    # set of unique letters that occur in cipher text
    #TODO May want to allow to look at the unique letters in both plain & cipher
    plain_unique_letters = set("".join(digraph_dict.values()))

    for letter in plain_unique_letters:
        for plain_di, cipher_di in \
                [(k,v) for k, v in digraph_dict.items() if letter in k
                                                           or letter in v]:
            # if letter in key, store key's respective char
            if plain_di[0] == letter:
                if letter in shared_rowcol:
                    shared_rowcol[letter].add(cipher_di[0])
                else:
                    shared_rowcol[letter] = set(cipher_di[0])
            elif plain_di[1] == letter:
                if letter in shared_rowcol:
                    shared_rowcol[letter].add(cipher_di[1])
                else:
                    shared_rowcol[letter] = set(cipher_di[1])

            # if letter in value, store key's respective char
            if cipher_di[0] == letter:
                if letter in shared_rowcol:
                    shared_rowcol[letter].add(plain_di[0])
                else:
                    shared_rowcol[letter] = set(plain_di[0])
            elif cipher_di[1] == letter:
                if letter in shared_rowcol:
                    shared_rowcol[letter].add(plain_di[1])
                else:
                    shared_rowcol[letter] = set(plain_di[1])

    return shared_rowcol

def find_rows_and_cols(digraph_dict, shared_rowcol=None):
    """
    Find for each letter, the two sets of other letters that share the same
    row and column, as well as one more set of letters that does not share
    either a row or column with the letter.

    """
    shared_row = {}
    shared_col = {}

    unshared_rowcol = {}



    return shared_row, shared_col, unshared_rowcol

def main():
    pie = {}
    pie["ab"] = "dc"
    pie["ac"] = "ca"
    pie["zy"] = "fg"
    pie["QX"] = "ba"

    shared = find_shared_rowcol(pie)
    print(shared)

if __name__ == "__main__":
    main()
