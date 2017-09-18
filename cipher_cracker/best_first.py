"""
Pseudo A* implementation (f(n) = h(n) not f(n) = g(n) + h(n)).
"""

import sys
from queue import PriorityQueue as pq
import json
from collections import OrderedDict
from collections import Counter
import numpy as np
import nltk

# Global english digraph frequency
with open("digraph_data/digraphs.json") as filename:
    digraph_freq = json.load(filename, object_pairs_hook=OrderedDict)

with open("wordsEn.txt") as filename:
    english_words = Set(filename.read().splitlines)

def best_first(cipher_dg, dg_freq_map):
    frontier_pq, explored_set = init_state();

    counter = 0
    while not eval_exit_condition(counter):
        counter++

def init_state():

def score(cipher):
    total = 0;
    for word in english_words:
        total += cipher.count(word)
    return total

def get_unexplored_neighbors(x, explored_set, dg_freq_map):
    """
    returns set of all neighbors who are only one away in frequency from x,
    and are unexplored.
    """
    n = len(x)
    r = n # n P r
    for di in x:

    # May want to allow more leniency, because the digraph freq in sample will not exactly match that of this general freq.
    # ensure this is 1 step in frequency from original digraph...
    #if 1 <= (digraph_freq.index(dg_freq_map[di_mod]) - digraph_freq.index(di)) <= 1:
    #   tmp = dg_freq_map[di_mod]
    #   dg_freq_map[di_mod] = dg_freq_map[di]
    #   dg_freq_map[di] = tmp
    # TODO do not do an if statement, simply branch out to the correct dimod, if not already visited!
    #return

def eval_exit_condition(counter):
    return counter > 100200300

def main(args):
    # Combine cipher into one string, assuming existance of spaces
    cipher = ""
    for s in args:
        cipher += s

    # Format cipher into list of digraphs [n, 2] matrix
    cipher_dg = np.array()
    dub = ""
    bool digraph = False

    for c in cipher:
        if digraph:
            dub += c
            cipher_dg = np.append(cipher_dg, dub)
            dub = ""
            digraph = False
        else:
            dub += c
            digraph = True


    digraph_set, digraph_counts = np.unique(cipher_dg, return_counts=True)
    cipher_dg_count = Counter(zip(digraph_set, digraph_counts))

    digraph_freq = digraph_freq[:len(digraph_set)]
    digraph_freq = tuple(digraph_freq.keys())

    dg_freq_map = dict(zip(cipher_dg_count.most_common(len(digraph_set)),
                           digraph_freq))

    best_first(cipher_dg, dg_freq_map)

if __name__ == "__main__":
    main(sys.args)
