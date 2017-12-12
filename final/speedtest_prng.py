"""
Speed test of Blub Blub Shub a CSPNRG versus Linear Congruential Genrator as a
classic PNRG example. Both are used to generate a a random 32bit number.

@author: Derek S. Prijatelj
"""

from sys import argv
import fractions
from timeit import default_timer as timer
from Crypto.Util import number

# lcg to be tested against
def lcg(m, a, c, seed):
    """
    Linear Congruential Generator, mimics that of Java's java.util.Random,
    POSIX rand48, and glibc rand48. Outputs the 32 most significant bits
    """
    while True:
        seed = (a * seed + c) % m
        yield seed >> (seed.bit_length() - 32)

# functions for Blum Blum Shub

def parity_of(val):
    """
    Returns a parity bit. 0 if even, -1 if odd.
    """
    parity = 0
    while val:
        parity = ~parity
        val = val & (val - 1)
    return parity

def bbs(p, q, seed):
    """
    Blum Blum Shub CSPNRG
    """
    while True:
        seed = (seed ** 2) % (p*q)
        yield parity_of(seed)

def test_lcg(m=2**48, a=25214903917, c=11, seed=19):
    # Ensure the assertions are met for the LCG
    assert 0 < m and 0 < a < m and 0 <= c < m and 0 <= seed < m
    lcg_prng = lcg(m, a, c, seed)

    # run 1000 tests, timing each, store in a csv: time, random_num
    with open("lcg.csv", 'w') as output:
        for i in range(1000):
            # timer start
            start = timer()
            result = next(lcg_prng)
            # Stop timer and record
            duration = timer() - start
            output.write(str(duration) + "," + str(result) + "\n")

def test_bbs(p, q, seed=19):
    # Ensure the assertions are met for the BBS
    assert seed % p != 0 and seed % q != 0
    assert p % 4 == 3 and q % 4 == 3
    #assert fractions.gcd(phi(p),phi(q)) < 5
    bbs_csprng = bbs(p, q, seed)

    # run 1000 tests, timing each, store in a csv: time, random_num
    with open("bbs.csv", 'w') as output:
        for i in range(1000):
            # timer start
            result = 0
            start = timer()
            for i in range(32):
                bit = next(bbs_csprng)
                result = (result << 1) | 1 if bit else result << 1
            # Stop timer and record
            duration = timer() - start
            output.write(str(duration) + "," + str(result) + "\n")

def find_pq_seed(prime_size=2048, seed_size=32, cycle_length=2048):
    p = number.getPrime(prime_size)
    while p % 4 != 3:
        p = number.getPrime(prime_size)
    print("p found: ", p)

    q = number.getPrime(prime_size)
    while q % 4 != 3:
        q = number.getPrime(prime_size)
    print("q found: ", q)

    seed = number.getPrime(seed_size)
    while seed == 1:
        seed = number.getPrime(seed_size)
    print("seed found: ", seed)

    """ To ensure a longer cycle than M, M is still long so skipping for now.
    while (p*q) / fractions.gcd(phi(p-1),phi(q-1)) < 2 ** cycle_length \
            or q % 4 != 3:
        q = number.getPrime(prime_size)
        assert q < p*q > p
        print(q)
    """
    return p, q, seed


def main(argv):
    test_lcg()
    p, q, seed = find_pq_seed(2048, 8, 2048)
    test_bbs(p, q, seed)
    #print(find_pq_seed(int(argv[1]), int(argv[2]), int(argv[3])))

if __name__ == "__main__":
    main(argv)
