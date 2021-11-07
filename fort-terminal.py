'''
###===                  FORT - File Operations Retro Terminal                 ===###
####===                  Written by Phillip Gallas, 2021                     ===####

    This retro, Fallout-inspired Terminal is designed to be quick, light and secure.
Type your password with arrow keys in a screen with characters in randomized order
to avoid keystrokes spying malware to steal your password.
    Store the password inside the FORTified file itself, which is encrypted, together 
with the files you want to protect.
    Already different and working software for protecting your data do exist, so one 
would think, "Why then?". First, it's fun to use, and that's good enough. Second, the 
idea of creating another layer of protection against keystrokes spying is interesting 
in on itself.    
'''

import numpy as np
import curses
from timeit import default_timer as timer
import sys

initial_row = 3
row = initial_row # Points the current row? I could change that to object

char_pool = [
            "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q",
            "R","S","T","U","V","W","X","Y","Z","a","b","c","d","e","f","g","h",
            "i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y",
            "z",".",",","<",">","{","}","[","]","(",")","/","?","!","*",
            "@","#","$","%","_","-"]
            ## Put NUMBERS and all characters used in creating passwords
            ## List might be incomplete. Filling it correctly might cause problem with 'char_objects' function
# chars = dict(...:..., ...:..., ...:...)
number_rows = 6
number_cols = round(len(char_pool)/number_rows)

stdscr = curses.initscr()
curses.start_color()
curses.curs_set(0)



class character:

    def __init__(self,char,row,col,color):
        self.char = char
        self.row = row
        self.col = col
        self.color = color




def char_objects(char_pool,number_rows):
    # Creates a dictionary that holds all characters available for creating a password
    # Each dictionary element corresponds to an object that holds a 
    #   char, position (row,col) and color (default: unselected)

    chars = {} # dictionary that will store many objects
    order = np.arange(len(char_pool))
    np.random.shuffle(order) 
    
    color = 1 # Not selected color
    rounded = round(len(char_pool)/number_rows) # Number of cols at the last row
    size_equal_rows = ((len(char_pool)-rounded)//(number_rows-1)) # Number of cols in all other rows
    list_row = []
    list_col = []
    for row_number in range(number_rows-1):
        list_row.append([row_number]*size_equal_rows) # append the sequence
        list_col.append(list(range(size_equal_rows)))
    else: 
        list_row.append([number_rows-1]*rounded)
        list_col.append(list(range(rounded)))

    ## example: 11/3(rows) = 3.3 > round: 3.    11-3 = 8/(3-1 = 2) = 4. 
    # Hence, [4, 4, 3] is the number of elements in each row
    list_col = [col for cols in list_col for col in cols] # Flattening list
    list_row = [row for rows in list_row for row in rows] # equivalent to 'for rows in list_row {for row in rows {row}}'

    for element,position,row,col in zip(range(len(char_pool)),order,list_row,list_col):
        chars[element] = character(char_pool[position],row,col,color)

    return chars




def header(stdscr_size):
    # Writes the header of the terminal
    # Is it better for it 
    # global row or passed row?

    global row
    str_string_ = ["FORT",
    "File Operator Retro Terminal",
    "Developed by Phillip Gallas"]
    str_position_ = []
    str_color_ = []

    for N in range(len(str_string_)): # Cycling through each character of the header string
        str_position_.append(round((stdscr_size-len(str_string_[N]))/2)) # Centering the text for whatever size. 
        # Starting at half of the remaining blank space
        if N == 0:
            str_color_.append(2)
        
        str_color_.append(1)

    for row in range(len(str_string_)):
        stdscr.addstr(row, str_position_[row], str_string_[row],curses.color_pair(str_color_[row]))
        row += 1
    # ADD CAPABILITY OF USING THE SAME TERMINAL BACKGROUD AND OTHER COLORS




def writing_into_terminal(stdscr_size,row,number_rows,number_cols,chars,current,size_courier): 
    global char_pool
    scrrow = row + 4 # (cushion) Row at which writing starts in the screen. Take three empty rows
    scrcol = (stdscr_size - number_cols*2)//2 # Starting half the blank side from the left

    for elem in range(len(char_pool)): # Writing all element
        stdscr.addstr(chars[elem].row + scrrow,chars[elem].col + scrcol,
        chars[elem].char,curses.color_pair(chars[elem].color))
    else: # Writing 'current'
        stdscr.addstr(current.row + scrrow,current.col + scrcol,current.char,curses.color_pair(current.color))

    # Displaying number of characters in the courier
    stdscr.addstr(row+4+number_rows+4,0,"*"*size_courier,curses.color_pair(1))




def choosing(action,current): # arrow keys & enter keys
    # Moves the cursor around the chars keyboard
    # 'choosing' receives a chars[element], the object containing all attributes of the chosen character
    
    global row, chars, number_rows, number_cols
    
    '''
    1. Set boudaries lower & upper for rows & columns
    2. When <Arrow> keys are pressed,
        2.1. compare with the position & boundaries
        2.2. move to the desired place if possible, and hold current position
        2.3. check which character is currently aimed
        2.4. highlight the currently aimed character
    3. When <Enter> is pressed,
        3.1. read the character and send it to the buffer
        3.2. update the part of the screen where the password is being typed with temporarily enabled echo()
        3.3. double <Enter> sends the buffer to hash & compare with password's hash
    '''

    # Boundaries for up, down and sideways? 
    if action == "up":

        ##################################################################################
        # Considering that upper elements are row = 0 and left-most elements are col = 0 #
        ##################################################################################

        if current.row > 0:
            # find_elem(current.row-1)
            for elem in chars:
                if (chars[elem].row == current.row-1) and (chars[elem].col == current.col):
                    current.color = 1
                    current = chars[elem]
                    current.color = 2 # Selected color
                    # return current
                    break 
    elif action == "down":
        if current.row < number_rows:
            for elem in chars:
                if (chars[elem].row == current.row+1) and (chars[elem].col == current.col):
                    current.color = 1
                    current = chars[elem]
                    current.color = 2 # Selected color
                    # return current
                    break 
    elif action == "left":
        if current.col > 0:
            for elem in chars:
                if (chars[elem].row == current.row) and (chars[elem].col == current.col-1):
                    current.color = 1
                    current = chars[elem]
                    current.color = 2 # Selected color
                    # return current
                    break 
    else: # right
        if current.col < number_cols:
            for elem in chars:
                if (chars[elem].row == current.row) and (chars[elem].col == current.col+1):
                    current.color = 1
                    current = chars[elem]
                    current.color = 2 # Selected color
                    # return current              
                    break

    return current # Holds the currently selected character. This char will be forwarded to 'passwords'




def terminal(stdscr,chars):
    # Manages important functions and
    # Assigns the character that was chosen at the Enter key press

    # Wrapper automatically executes curses.start_color()
    global row, initial_row, number_rows, number_cols # Appoints to current row
    courier = [] # List of characters that comprise the password
    curses.cbreak() # Characters will be read one by one (as I type), instead of buffered until <Enter> call
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK) # pair 1 - Green in Black # Unselected color
    curses.init_pair(2,curses.COLOR_BLACK,curses.COLOR_GREEN) # pair 2 - Black in Green # Selected color
    # For multiple colors, rework code to create 2 variables: selected_color & unselected_color
    stdscr_size = [0,0] # Stores screen size
    
    # Find chars in position [y,x]
    for elem in chars:
        if (chars[elem].row == round(number_rows/2 -1)) and (chars[elem].col == round(number_cols/2)):
            current = chars[elem]
            current.color = 2 # Selected color
            break 

    PASSWORD_CHECK = False # Condition
    while(PASSWORD_CHECK == False):
        while(True):
            if (stdscr_size != stdscr.getmaxyx()): # If screen was resized, adjust its content
                stdscr_size = list(stdscr.getmaxyx())
                stdscr.clear()
                row = initial_row
                header(stdscr_size[1])
                writing_into_terminal(stdscr_size[1],row,number_rows,number_cols,chars,current,len(courier))
            
            stdscr.refresh()
            KEY = stdscr.getkey() # use getch to see the unicode for certain key
            if KEY == "KEY_UP":
                current = choosing("up",current)
               
            elif KEY == "KEY_DOWN":
                current = choosing("down",current)
               
            elif KEY == "KEY_LEFT":
                current = choosing("left",current)
               
            elif KEY == "KEY_RIGHT":
                current = choosing("right",current)
               
            elif KEY == chr(127): # Backspace?
                # Delete characters in the courier, popping out from the last position
                courier.pop()
            elif KEY == "\n":
                start = timer()
                KEY = stdscr.getkey()
                finish = timer()
                elapsed = finish - start

                if (KEY == "\n") and (elapsed < 0.5): # Double <ENTER>
                    PASSWORD_CHECK = True 
                    break

                # Single <ENTER>
                courier.append(current.char)
                writing_into_terminal(stdscr_size[1],row,number_rows,number_cols,chars,current,len(courier))
                stdscr.refresh()

            elif KEY == chr(27): # ESC
                curses.endwin()
                sys.exit() 

    curses.delay_output(100)




if __name__ == '__main__':
    chars = char_objects(char_pool,number_rows)

    curses.wrapper(terminal,chars)
