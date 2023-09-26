"""

Solver for Mastermind code breaking game.

Implement Donald Knuth algorithm.

Multiple game modes

             | Mode 1   | Mode 2   | Mode 3   | Mode 4
Code breaker | computer | computer | human    | human 
Code keeper  | computer | human    | computer | human 

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


PEGS = 'rgbcym'


def get_response(guess, code):
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

    index_blacks = [
        i for i, (c, g) in 
        enumerate(zip(_code, _guess)) if c == g
    ]
    blacks = len(index_blacks)

    index_blacks.reverse()
    for idx in index_blacks:
        del _code[idx]
        del _guess[idx]

    whites = 0
    for g in _guess:
        if g in _code:
            whites += 1
            _code.remove(g)

    return blacks, whites


def get_response_iteractive():
    """In an interactive game, the code keeper gives the reponse
    manually for each guess.
    """
    while True:
        blacks = int(input('    How many blacks? '))
        
        if blacks == 4:
            return 4, 0

        whites = int(input('    How many whites? '))
        if (0 <= blacks <= 4 and
            0 <= whites <= 4 and
            whites + blacks <= 4 and
            not (blacks == 3 and whites == 1)
        ):
            return blacks, whites
        else:
            print('Invalid input. Again...')


def prune(S, T, guess, resp, verbose):
        # Remove current guess
        S.remove(tuple(guess))
        T.remove(tuple(guess))

        # 5. Remove from S any code that would not give the same
        # response of colored and white pegs.
        S[:] = [c for c in S if get_response(guess, c) == resp]

        if verbose:
            print(f'    S has {len(S)} elements.')


def get_next_guess(S, T, verbose):
    # 6. Apply minimax technique to find a next guess

    # Keep track of the worst score per guess
    # Higher score is worse, therefore `max(scores)`
    guesses_worst_score = dict()
    for g in S:
        scores = defaultdict(int)
        for c in T:
            r = get_response(g, c)
            scores[r] += 1
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
    #guess = ''.join(
    #    list(guesses_worst_score.keys()
    #        )[list(guesses_worst_score.values()).index(best_score)])
    next_guesses = []
    for tentative_guess, score in guesses_worst_score.items():
        if score == best_score:
            next_guesses.append(tentative_guess)

    for next_guess in next_guesses:
        if next_guess in T:
            guess = ''.join(next_guess)
            return guess

    for next_guess in next_guesses:
        if next_guess in S:
            guess = ''.join(next_guess)
            return guess

    return None


def get_next_guess_iteractive():
    """In an iteractive game, human gives next guess"""
    while True:
        guess = input('    Next guess: ')
        
        if (len(guess) == 4 and
            set(guess).issubset(set(PEGS))
        ):
            return guess
        else:
            print('Invalid guess. Again...')


def mastermind(
    guess='rrgg', 
    code='ycmb', 
    iteractive_codekeeper=False, 
    iteractive_codebreaker=False,
    verbose=False,
):
    """Mastermind - Knuth algorithm to break the code.

    Implemented 6 colours, 4 pegs. Repeating colours is allowed.
    """

    # 1. Create the set S of 1,296 possible codes
    S = list(itertools.product(PEGS, repeat=4))
    T = S[:]
    if verbose:
        print(f'    S has {len(S)} elements.')

    if iteractive_codebreaker:
        guess = get_next_guess_iteractive()

    count = 0
    while True:
        count += 1
        if count > 12:
            print('Code not found.')
            return

        # 3. Play the guess to get a response
        print(f'[{count}] {guess=} ', end='')
        if not iteractive_codekeeper:
            resp = get_response(guess, code)
            blacks, whites = resp
            print(f'-> {blacks=}, {whites=}')
        else:
            print()
            resp = get_response_iteractive()
            blacks, whites = resp

        # 4. If the response is four colored key pegs, the game is won
        if blacks == 4:
            print(f'The code is {guess}.')
            return

        if not iteractive_codebreaker:
            prune(S, T, guess, resp, verbose)
            guess = get_next_guess(S, T, verbose)
        else:
            guess = get_next_guess_iteractive()

        assert guess is not None


def main():

    parser = argparse.ArgumentParser(description="Mastermind's Knuth algorithm.")
    parser.add_argument('-v', '--verbose', action='store_const',
                        const=True, default=False)
    parser.add_argument('-g', '--guess', type=str, default='rrgg', nargs='?',
                        help='First guess.')
    parser.add_argument('-c', '--code', type=str, default='ycmb', nargs='?',
                        help='Code to be broken.')
    parser.add_argument('-k', '--iteractive_codekeeper', action='store_const',
                        help='Play the game as code keeper. '
                             ' User inputs the response per guess.',
                        const=True, default=False)
    parser.add_argument('-b', '--iteractive_codebreaker', action='store_const',
                        help='Play the game as code breaker. '
                             ' User inputs the next guess.',
                        const=True, default=False)
    args = parser.parse_args()

    mastermind(
        guess=args.guess, 
        code=args.code, 
        verbose=args.verbose,
        iteractive_codekeeper=args.iteractive_codekeeper,
        iteractive_codebreaker=args.iteractive_codebreaker,
    )


if __name__ == '__main__':
    main()
