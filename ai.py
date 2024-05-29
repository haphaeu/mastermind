"""
Work ongoing
this doesn't do anything yet rather than solving it brute-force.
"""
import itertools
import random
import tensorflow

from mastermind2 import (PEGS, prune, get_response)


ALL_GUESSES = set(itertools.product(PEGS, repeat=4))
def get_next_guess_ai():
    return ''.join(ALL_GUESSES.pop())
	
	
def mastermind(code='ycmb', verbose=False):
    """AI is the code breaker.
    """
    S = list(itertools.product(PEGS, repeat=4))
    T = S[:]
    guess = get_next_guess_ai()
    count = 0
    while True:
        count += 1
        resp = get_response(guess, code)
        blacks, whites = resp
        if verbose:
            print(f'[{count}] {guess=} -> {blacks=}, {whites=}', end='\r')
        if blacks == 4:
            print(f'The code is {guess}.')
            return count
        guess = get_next_guess_ai()
        assert guess is not None

if __name__ == '__main__':
    print(f'Solved in {mastermind()} guesses')
