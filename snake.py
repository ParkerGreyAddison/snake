### Import Statements
import curses as cs
import random
import time

### Menu Screen
screen = cs.initscr()
cs.start_color()

"""
Will add menu screen here
"""

### Setting up my Window
ylim, xlim = cs.LINES - 2, cs.COLS - 4  #setting our window limits
win = cs.newwin(ylim, xlim, 1, 2)
win.keypad(1)                           #lets us use things like KEY_LEFT instead of weird terminal characters
cs.noecho()                             #hides the character inputs from being typed
cs.curs_set(0)                          #hides the cursor
win.border(0)                           #draws a border around our window (a subspace of our terminal screen)
win.nodelay(True)                       #allows user input at any time

### Initializing Snake, Food, and Variables
sy, sx = int(ylim/2), int(xlim/2)
snake = [[sy, sx], [sy, sx-1], [sy, sx-2]]
food = [int(ylim/3), int(xlim/3)]

pressed = cs.KEY_RIGHT
prev_press = pressed
score = 0
running = True
ingame = True
# Direction will be a factor into snake speed
direction = 0

win.addch(food[0], food[1], cs.ACS_PI)

### Main game loop, plays while ESC (ord == 27) isn't pressed
while running:

    while ingame:

        # Adding border, title, score
        win.border(0)
        win.addstr(ylim-1, 1, 'SNAKE GAME', cs.A_BOLD)
        win.addstr(ylim-1, xlim - 15, 'Score : ' + str(score))

        # Setting the speed of the snake
        rest = (1 / len(snake)) * .8 * 1.5 ** direction
        """
        A bit too slow at the very beginning, then gets too fast
        Try for a log type of result? (obviously keep the 1.8 ** direction at the end)
        """
        time.sleep(.08 * 1.5 ** direction)

        # Getting my next press if an input is detected
        """
        Will add prevention of pulling a 180
        """
        next_press = win.getch()
        if next_press in [cs.KEY_RIGHT, cs.KEY_LEFT, cs.KEY_UP, cs.KEY_DOWN, 27, ord(' '), ord('w'), ord('a'), ord('s'), ord('d')]:
            prev_press = pressed
            pressed = next_press

        # Pause functionality
        if pressed == ord(' '):
            ingame = False
            break
                
        # If ESC (ord 27) is pressed, stop entire game
        if pressed == 27:
            running = False
            break

        # Adding the new snake head
        if pressed == cs.KEY_RIGHT or pressed == ord('d'):
            direction = 0
            snake.insert(0, [snake[0][0], snake[0][1] + 1])
        if pressed == cs.KEY_LEFT or pressed == ord('a'):
            direction = 0
            snake.insert(0, [snake[0][0], snake[0][1] - 1])
        if pressed == cs.KEY_UP or pressed == ord('w'):
            direction = 1
            snake.insert(0, [snake[0][0] - 1, snake[0][1]])
        if pressed == cs.KEY_DOWN or pressed == ord('s'):
            direction = 1
            snake.insert(0, [snake[0][0] + 1, snake[0][1]])

        # Losing the game if head at a border, or if head in the rest of the snake
        if snake[0][0] == 0 or snake[0][0] == ylim-1 or snake[0][1] == 0 or snake[0][1] == xlim-1:
            running = False
            break
        if snake[0] in snake[1:]:
            running = False
            break

        # Remove the old snake tail unless the head == food
        if snake[0] == food:
            score += 1
            # Make sure the new food isn't in the snake
            food = []
            while food == []:
                food = [random.randint(1, ylim-2), random.randint(1, xlim-2)]
                if food in snake:
                    food = []
            # Add a new bit of food
            win.addch(food[0], food[1], cs.ACS_PI)
        else:
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')        

        # Draw the snake
        win.addch(snake[0][0], snake[0][1], '#')

    if pressed == ord(' '):
        key = -1
        while key != ord(' '):
            key = win.getch()
            if key == 27:
                running = False
                break
        ingame = True
        pressed = prev_press

    ### Ending Sequence, game over, score, and highscores list
    """
    Will add game over screen
    ask for initials _ _ _, writes score to list of scores (txt file)
    displays score and position on list of high scores
    """

### Closing sequence, returns terminal to its original function
win.keypad(0)
cs.echo()
cs.endwin()
