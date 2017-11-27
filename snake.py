### Import Statements
import curses as cs
import random
import time

screen = cs.initscr()
cs.start_color()

### Set up global variables
rainbowsnake = False
for i in range(1, 8):
    cs.init_pair(i, 0, i)

score = 0

pi = '3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745'

""" Guide """
### Guide Screen, txt and animations
def guide():
    pass
""" /Guide """




""" Options """
### Options, allowing global variable changes
def options():
    global rainbowsnake
    screen.clear()
    screen.addstr(1, int(cs.COLS/2) - 4, 'Options', cs.A_BOLD)

    hover = 0

    in_options = True
    while in_options:

        highlights = [0] * 4
        highlights[hover] = cs.A_REVERSE

        screen.addstr(int(cs.LINES/2) - 1, int(cs.COLS/2) - len('Colorful Snake') - 2,
                          'Colorful Snake : ' + str(rainbowsnake) + ' ' * rainbowsnake, highlights[0])
        screen.addstr(int(cs.LINES/2), int(cs.COLS/2) - 13,
                      'Coming Soon : ', highlights[1])
        screen.addstr(int(cs.LINES/2) + 1, int(cs.COLS/2) - 13,
                      'Coming Soon : ', highlights[2])
        screen.addstr(cs.LINES - 2, int(cs.COLS/2) - 4,
                      '<- Back', highlights[3])

        screen.refresh()

        pressed = screen.getch()
        if pressed == cs.KEY_UP:
            hover = (hover - 1) %4
        elif pressed == cs.KEY_DOWN:
            hover = (hover + 1) %4
        elif pressed == 27:
            in_options = False
            menu()
        elif pressed == ord('\n'):
            if hover == 0:
                rainbowsnake = not rainbowsnake
            if hover == 3:
                in_options = False
                menu()

    
""" /Options """



""" High Scores """
### High scores list
def highscores():
    pass
""" /High Scores """




""" Game Over """
### Ending Sequence, game over, score, and highscores list
def gameover():
    screen.addstr(int(cs.LINES/2) - 2, int((cs.COLS - len('Game Over'))/2), 'Game Over', cs.A_BOLD)
    screen.refresh()
    screen.nodelay(0)
    time.sleep(2)
    screen.clear()
    while True:
        
        screen.addstr(int(cs.LINES/2) - 2, int(cs.COLS/2) - 5, 'Game Over', cs.A_BOLD)
        screen.addstr(int(cs.LINES/2), int(cs.COLS/2) - 13, 'You found ' + str(score) + ' digits of pi!')
        screen.addstr(1, int(cs.COLS/2 - len(pi[0:score])/2), pi[0:score])
        
        screen.refresh()

        pressed = screen.getch()

        if pressed == 27:
            break
        
    """
    ask for initials _ _ _, writes score to list of scores (txt file)
    displays score and position on list of high scores
    """
""" /Game Over """




""" Game """
### Game Definition
def game():
    global score

    ### Setting up my Window
    ylim, xlim = cs.LINES - 2, cs.COLS - 4  #setting our window limits
    win = cs.newwin(ylim, xlim, 1, 2)
    win.keypad(1)                           #lets us use things like KEY_LEFT instead of weird terminal characters
    cs.noecho()                             #hides the character inputs from being typed
    cs.curs_set(0)                          #hides the cursor
    win.border(0)                           #draws a border around our window (a subspace of our terminal screen)
    win.nodelay(1)                       #allows user input at any time

    """
    Will add support for start length, grow length
    """

    ### Initializing Snake, Food, and Variables
    sy, sx = int(ylim/2), int(xlim/2)
    snake = [[sy, sx], [sy, sx-1], [sy, sx-2]]
    food = [int(ylim/3), int(xlim/3)]

    pressed = cs.KEY_RIGHT
    next_press = pressed
    score = 0
    running = True
    ingame = True
    # Verticality will be a factor into snake speed
    vertical = 0

    # Adding dictionary object to map each direction to an integer
    directions = {cs.KEY_RIGHT:1, ord('d'):1, cs.KEY_LEFT:-1, ord('a'):-1,
                  cs.KEY_UP:2, ord('w'):2, cs.KEY_DOWN:-2, ord('s'):-2}

    win.addch(food[0], food[1], cs.ACS_PI)

    ### Main game loop, plays while ESC (ord == 27) isn't pressed
    """ Running """
    while running:

        """ Ingame """
        while ingame:

            # Adding border, title, score
            win.border(0)
            win.addstr(ylim-1, 1, 'SNAKE GAME', cs.A_BOLD)
            win.addstr(ylim-1, xlim - 12, 'Score : ' + str(score))

            # Setting the speed of the snake
            rest = (1 / len(snake)) * .8 * 1.5 ** vertical
            """
            A bit too slow at the very beginning, then gets too fast
            Try for a log type of result? (obviously keep the 1.5 ** direction at the end)
            """
            time.sleep(.08 * 1.5 ** vertical)

            # Getting my next press if an input is detected
            next_press = win.getch()

            # Pause functionality
            if next_press == ord(' '):
                win.addstr(0, 1, 'PAUSED', cs.A_BLINK)
                ingame = False
                break
                    
            # If ESC (ord 27) is pressed, game over
            if next_press == 27:
                running = False
                break
            
            acceptable_keys = [cs.KEY_RIGHT, cs.KEY_LEFT, cs.KEY_UP, cs.KEY_DOWN,
                               ord('w'), ord('a'), ord('s'), ord('d')]
            # If valid input and if not the opposite direction as currently pressed
            if next_press in acceptable_keys and directions[pressed] + directions[next_press] != 0:
                pressed = next_press


            # Adding the new snake head
            if pressed == cs.KEY_RIGHT or pressed == ord('d'):
                vertical = 0
                snake.insert(0, [snake[0][0], snake[0][1] + 1])
            if pressed == cs.KEY_LEFT or pressed == ord('a'):
                vertical = 0
                snake.insert(0, [snake[0][0], snake[0][1] - 1])
            if pressed == cs.KEY_UP or pressed == ord('w'):
                vertical = 1
                snake.insert(0, [snake[0][0] - 1, snake[0][1]])
            if pressed == cs.KEY_DOWN or pressed == ord('s'):
                vertical = 1
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
            if rainbowsnake:
                win.addch(snake[0][0], snake[0][1], 32, cs.color_pair(random.randint(1, 7)))
            else:
                win.addch(snake[0][0], snake[0][1], 32, cs.A_REVERSE)
        """ /Ingame """

        if next_press == ord(' '):
            key = -1
            while key != ord(' '):
                key = win.getch()
                if key == 27:
                    running = False
                    break
            ingame = True

    """ /Running """
    gameover()
        
""" /Game """




""" Menu """
### Menu Screen
def menu():
    cs.noecho()
    cs.curs_set(0)
    screen.keypad(1)
    screen.nodelay(1)
    
    selected = False
    hover = 0

    screen.clear()
    screen.addstr(1, int(cs.COLS/2) - 3, 'SNAKE', cs.A_BOLD)
    
    """ Not selected """
    while not selected:

        highlights = [0] * 5
        highlights[hover] = cs.A_REVERSE

        screen.addstr(int(cs.LINES/2) - 1, int(cs.COLS/2) - 5, 'Play Game', highlights[0])
        screen.addstr(int(cs.LINES/2), int(cs.COLS/2) - 3, 'Guide', highlights[1])
        screen.addstr(int(cs.LINES/2) + 1, int(cs.COLS/2) - 4, 'Options', highlights[2])
        screen.addstr(int(cs.LINES/2) + 2, int(cs.COLS/2) - 6, 'High Scores', highlights[3])
        screen.addstr(cs.LINES - 2, int(cs.COLS/2) - 4, '[] Exit', highlights[4])

        screen.refresh()

        pressed = screen.getch()
        if pressed == cs.KEY_UP:
            hover = (hover - 1) %5
        elif pressed == cs.KEY_DOWN:
            hover = (hover + 1) %5
        elif pressed == 27:
            break
        elif pressed == ord('\n'):
            selected = True

    """ /Not selected """
    if selected:
        if hover == 0:
            game()
        elif hover == 1:
            guide()
        elif hover == 2:
            options()
        elif hover == 3:
            highscores()
        elif hover == 4:
            pass
       
        """
        Will add list of most recent n inputs -> cheat codes!!!!
        insert and pop
        """
""" /Menu """        


### Game Sequence, everything is prompted from the menu() call
menu()




### Closing sequence, returns terminal to its original function
cs.echo()
cs.endwin()
