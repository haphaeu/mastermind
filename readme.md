# Mastermind

Classical
[Mastermind](https://en.wikipedia.org/wiki/Mastermind_(board_game))
code braking game, where one player, the code keeper, creates a secret
code and the other player, the code breaker, tries to guess the code
based on feedback from the code keeper on each guess.

The code is composed of 4 *pegs*. Each peg can have 6 colors.

The code keepers gives feedback using black and white pegs. One black
peg for each guess peg that has the correct color at the correct place.
One white peg is given for each remaining guess peg with the right color
but in the wrong place.

The code has been broken when the code keeper feedback is 4 black pegs.

For exaple:

    code = cybm

    guess = rrgg => blacks = 0, whites = 0
    guess = bbcc => clacks = 0, whites = 2
    guess = ccyy => blacks = 1, whites = 1
    guess = cybm => blacks = 4

# Use - CLI

This implementation has 4 game modes:

| Role         | Mode 1   | Mode 2   | Mode 3   | Mode 4 |
|--------------|----------|----------|----------|--------|
| Code breaker | computer | computer | human    | human  |
| Code keeper  | computer | human    | computer | human  |

The default is Mode 1 - a non-iteractive automatic solver
using Donald Knuth's algorithm.

To play the game iteractivelly, use the argument options `-k` to
play as code keeer, and `-b` to play as code breaker. Note that
passing both `-k -b` will lead to a game where the user has to
input both the guesses and give feedback - in this case, wouldn't it
be more fun to play on a piece of paper?

# Use - GUI

A graphical interface, a very ugly and simple one at that, is
implemented for the game. 

This interface has 3 game modes: `Auto`, `Breaker`, `Keeper`. Just
press `A-B-K` to switch between modes.

In `Breaker` mode, use the mouse to switch between colors for 
each peg. When you're happy with your guess, press `P` to play
that round and get feedback on your guess.

In `Auto` mode, the computer will do the guess and give feedback,
just press `P` to move on to new round.

The `Keeper` mode is not implemented.

Press `R` anytime to reset the board.

# TODO

## CLI

  - [x] Implement game modes
  - [x] Add command line arguments


## GUI

  - [ ] Input code to be broken, for `Auto` and `Breaker` modes.
  - [ ] Show messages in the GUI rather than in the prompt.
  - [ ] Highlight active row
  - [ ] Implement use feedback
  