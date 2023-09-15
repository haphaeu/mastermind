"""

Solver for Mastermind code breaking game.

Implement Donald Knuth algorithm.

Author:
Rafael Rossi

License:
GNU-GPL 3

References:
https://en.wikipedia.org/wiki/Mastermind_(board_game)#Worst_case:_Five-guess_algorithm
https://stackoverflow.com/questions/62430071/donald-knuth-algorithm-mastermind
"""

import sys
import argparse
import itertools
from collections import defaultdict


def response(guess, code):
    """Return the number of black and white pegs for a guess and a code.

    Black pegs are given for each peg in guess that has the correct both
    colour and position in the code.

    White pegs mean a correct colour but in wrong position. In case of
    more than 1 peg of a certain colour in the guess, only those
    corresponding to the number of same-colored pegs in the code will be
    get a white peg, not counting the peg awarded a black peg.

    Example:

        code = 'rgbb'
        guess = 'rrrb'
        response: blacks=2 (first 'r' and last 'b'), whites=0

        code = 'bggr'
        guess = 'rrbb'
        response: blacks=0, whites=2 (1 'r' and 1 'b')

    """

    _guess = list(guess)
    _code = list(code)

    blacks = whites = 0
    index_blacks = []
    for i, (c, g) in enumerate(zip(_code, _guess)):
        if c == g:
            blacks += 1
            index_blacks.append(i)

    index_blacks.reverse()
    for idx in index_blacks:
        del _code[idx]
        del _guess[idx]

    # WRONG: whites = sum([g in _code for g in _guess])
    whites = 0
    for g in _guess:
        if g in _code:
            whites += 1
            _code.remove(g)

    return blacks, whites


def knuth(guess='rrgg', code='ycmb', verbose=False):
    """Mastermind - Knuth algorithm to break the code.

    Implemented 6 colours, 4 pegs. Repeating colours is allowed.
    """

    # 1. Create the set S of 1,296 possible codes
    S = list(itertools.product('rgbcym', repeat=4))

    count = 0
    while True:
        count += 1

        # 3. Play the guess to get a response
        r = response(guess, code)
        blacks, whites = r

        print(f'[{count}] {guess=} -> {blacks=}, {whites=}')

        # 4. If the response is four colored key pegs, the game is won
        if blacks == 4:
            print(f'The code is {guess}.')
            return

        # Remove current guess
        S.remove(tuple(guess))

        # 5. Remove from S any code that would not give the same
        # response of colored and white pegs.
        for c in S:
            if not r == response(guess, c):
                S.remove(c)
        if verbose:
            print(f'    S has {len(S)} elements.')

        # 6. Apply minimax technique to find a next guess

        # Keep track of the worst score per guess
        # Higher score is worse, therefore `max(scores)`
        guesses_worst_score = dict()
        for g in S:
            scores = defaultdict(int)
            for c in S:
                scores[response(g, c)] += 1
            worst_score = max(scores.values())  
            guesses_worst_score[g] = worst_score

        # Minimax: best of the worst score: min(max(scores))
        best_score = min(guesses_worst_score.values())

        if verbose:
            num_best_score = list(
                guesses_worst_score.values()
                ).count(best_score)
            print(f'    best worst score is {best_score}, '
                  f'for {num_best_score} guesses: ',
                 end='')
            for tmp_guess, tmp_score in guesses_worst_score.items():
                if tmp_score == best_score:
                    print(f'"{"".join(tmp_guess)}"', end=' ')
            print()

        # Guesses with best_score are not necessarily unique.
        # Picks the first guess with `best_score`
        guess = ''.join(
            list(guesses_worst_score.keys()
                )[list(guesses_worst_score.values()).index(best_score)])


def main():

    parser = argparse.ArgumentParser(description="Mastermind's Knuth algorithm.")
    parser.add_argument('-v', '--verbose', action='store_const',
                        const=True, default=False)
    parser.add_argument('-g', '--guess', type=str, default='rrgg', nargs='?',
                        help='First guess.')
    parser.add_argument('-c', '--code', type=str, default='mcyb', nargs='?',
                        help='Code to be broken.')
    args = parser.parse_args()

    knuth(guess=args.guess, code=args.code, verbose=args.verbose)


if __name__ == '__main__':
    main()
