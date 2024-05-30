"""
Work ongoing
this doesn't do anything yet rather than solving it brute-force.
"""
import itertools
import random
import tensorflow

from mastermind2 import PEGS, get_response

# All possible guesses, in the format 'rgbc':
ALL_GUESSES = set(itertools.product(PEGS, repeat=4))

# Stack of guesses and reponses of a round of the game.
# The responses are a tuple (blacks, whites).
GUESSES = []
RESPONSES = []


def get_next_guess_ai():
    """Here AI should consider all previous GUESSES and
    RESPONSES and come up with the next guess.
    """
    return ''.join(ALL_GUESSES.pop())
	
	
def mastermind(code='ycmb', verbose=False):
    """AI is the code breaker.
    """
    global GUESSES, RESPONSES
    
    S = list(itertools.product(PEGS, repeat=4))
    T = S[:]
    guess = get_next_guess_ai()
    count = 0
    while True:
        count += 1
        resp = get_response(guess, code)
        
        GUESSES.append(guess)
        RESPONSES.append(resp)
        
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
   
    with open('last_game.txt', 'w') as f:
        for i, (g, r) in enumerate(zip(GUESSES, RESPONSES)):
            f.write(f'{i}, {g}, {r}\n')
