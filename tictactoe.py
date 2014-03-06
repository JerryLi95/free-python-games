"""
Tic Tac Toe.

Written by Grant Jenks
http://www.grantjenks.com/

Copyright (c) 2012 Grant Jenks

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.

Exercises
1. Why does the computer player try to win two ways?
2. Draw an X as a square instead.
3. Make the computer play itself.
"""

import sys, pygame, random
from pygame.locals import *

pygame.init()

size = width, height = 480, 480
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

black, red, blue, white = (0, 0, 0), (255, 0, 0), (0, 0, 255), (255, 255, 255)
lose, tie, win = xxx, empty, ooo = -1, 0, 1
human = ooo

def draw_game():
    pygame.draw.rect(screen, white, (0, 0, width, height))

    pygame.draw.line(screen, black, (160, 0), (160, 480), 5)
    pygame.draw.line(screen, black, (320, 0), (320, 480), 5)
    pygame.draw.line(screen, black, (0, 160), (480, 160), 5)
    pygame.draw.line(screen, black, (0, 320), (480, 320), 5)

    for row, line in enumerate(board):
        for col, val in enumerate(line):
            if val == xxx:
                # Draw an X as two crossing lines.

                upper_left = (col * 160 + 5, row * 160 + 5)
                lower_right = (col * 160 + 155, row * 160 + 155)
                pygame.draw.line(screen, red, upper_left, lower_right, 5)

                upper_right = (col * 160 + 155, row * 160 + 5)
                lower_left = (col * 160 + 5, row * 160 + 155)
                pygame.draw.line(screen, red, upper_right, lower_left, 5)
            elif val == ooo:
                rect = (col * 160 + 5, row * 160 + 5, 150, 150)
                pygame.draw.ellipse(screen, blue, rect, 5)
            else:
                assert val == empty
                continue

    pygame.display.flip()

def is_won():
    for val in range(3):
        # Check matching row.

        if board[0][val] == board[1][val] == board[2][val] != empty:
            return board[0][val]

        # Check matching column.

        if board[val][0] == board[val][1] == board[val][2] != empty:
            return board[val][0]

    # Check matching diagonal.

    if board[0][0] == board[1][1] == board[2][2] != empty:
        return board[1][1]

    if board[0][2] == board[1][1] == board[2][0] != empty:
        return board[1][1]

    return empty

def calc_move(player):
    if all(val == empty for line in board for val in line):
        row = random.randrange(3)
        col = random.randrange(3)
        result = (tie, (row, col))
    else:
        result = best_move(player)
    return result

def best_move(player):
    """
    Return (outcome, (row, col)) indicating this player's best move.
    """
    best = None
    for row, line in enumerate(board):
        for col, val in enumerate(line):
            if val == empty:
                # Simulate this move.

                board[row][col] = player

                if is_won() == player:
                    board[row][col] = empty
                    return (win, (row, col))

                # Compute the best counter-move result.

                counter = best_move(player * -1)

                # Update our best move based on the counter-move result.

                if best is None or best[0] <= (counter[0] * -1):
                    best = (counter[0] * -1, (row, col))

                # Undo simulated move.

                board[row][col] = empty

    if best is None: best = (tie, None)

    return best

def restart():
    global board, turn, human
    human *= -1
    board = [[empty] * 3, [empty] * 3, [empty] * 3]
    turn = xxx
    draw_game()
    pygame.display.flip()

restart()

while True:
    clock.tick(12)
    event = pygame.event.poll()

    pos = None

    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == KEYDOWN:
        if event.key == K_r:
            restart()
            draw_game()
            pygame.display.flip()
        elif event.key == K_q:
            pygame.event.post(pygame.event.Event(QUIT))
    elif event.type == MOUSEBUTTONDOWN and event.button == 1:
        pos = (event.pos[1] / 160, event.pos[0] / 160)

    if human != turn:
        pos = calc_move(turn)[1]

    if pos is None or is_won(): continue

    row, col = pos

    if board[row][col] == empty:
        board[row][col] = turn
        turn *= -1
        draw_game()