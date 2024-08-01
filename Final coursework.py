# -*- coding: utf-8 -*-
"""
A simulation of the board game Nine Men's Morris
"""

def request_location(question_str):
    """
    Prompt the user for a board location, and return that location.
    
    Takes a string parameter, which is displayed to the user as a prompt.
    
    Raises ValueError if input is not a valid integer, 
    or RuntimeError if the location typed is not in the valid range.
    
    *************************************************************
    DO NOT change this function in any way
    You MUST use this function for ALL user input in your program
    *************************************************************
    """
    loc = int(input(question_str))
    if loc<0 or loc>=24:
        raise RuntimeError("Not a valid location")
    return loc


def draw_board(g):
    """
    Display the board corresponding to the board state g to console.
    Also displays the numbering for each point on the board, and the
    number of counters left in each players hand, if any.
    A reference to remind players of the number of each point is also displayed.
    
    You may use this function in your program to display the board
    to the user, but you may also use your own similar function, or
    improve this one, to customise the display of the game as you choose
    """
    def colored(r, g, b, text):
        """
        Spyder supports coloured text! This function creates coloured
        version of the text 'text' that can be printed to the console.
        The colour is specified with red (r), green (g), blue (b) components,
        each of which has a range 0-255.
        """
        return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

    def piece_char(i):
        """
        Return the (coloured) character corresponding to player i's counter,
        or a + to indicate an unoccupied point
        """
        if i==0:
            return colored(100,100,100,'+')
        elif i==1:
            return colored(255,60,60,'X')
        elif i==2:
            return colored(60,120,255,'O')

        
    board = '''
x--------x--------x  0--------1--------2 
|        |        |  |        |        |
|  x-----x-----x  |  |  3-----4-----5  |
|  |     |     |  |  |  |     |     |  |
|  |  x--x--x  |  |  |  |  6--7--8  |  |
|  |  |     |  |  |  |  |  |     |  |  |
x--x--x     x--x--x  9-10-11    12-13-14
|  |  |     |  |  |  |  |  |     |  |  |
|  |  x--x--x  |  |  |  | 15-16-17  |  |
|  |     |     |  |  |  |     |     |  |
|  x-----x-----x  |  |  18---19----20  |
|        |        |  |        |        |
x--------x--------x  21------22-------23
'''    
    boardstr = ''
    i = 0
    for c in board:
        if c=='x':
            boardstr += piece_char(g[0][i])
            i += 1
        else:
            boardstr += colored(100,100,100,c)
    if g[1]>0 or g[2]>0:
        boardstr += '\nPlayer 1: ' + (piece_char(1)*g[1])
        boardstr += '\nPlayer 2: ' + (piece_char(2)*g[2])
    print(boardstr)
    
    
    
    
#############################    
# The functions for each task
    
def is_adjacent(i, j):
    """
    Takes two integers i and j representing points on the game board and 
    returns True if the two points are adjacent to one another (i.e. connected 
    by a line without going through another point), or False otherwise. A point 
    is not adjacent to itself.
    """
    # A list of lists of the points adjacent to each point on the board (i.e. 
    # the first element is [1, 9] as 0 is adjacent to 1 and 9)
    list_of_adjacent_points = [[1, 9], [0, 2, 4], [1, 14], [4, 10], [1, 3, 5, 7], [4, 13], [7, 11], [4, 6, 8], [7, 12], [0, 10, 21], [3, 9, 11, 18], [6, 10, 15], [8, 13, 17], [5, 12, 14, 20], [2, 13, 23], [11, 16], [15, 17, 19], [12, 16], [10, 19], [16, 18, 20, 22], [13, 19], [9, 22], [19, 21, 23], [14, 22]]
    # We check if j is in the list of points adjacent to i
    if j in list_of_adjacent_points[i]:
        return True
    else:
        return False
    
        
def new_game():
    """
    Returns the game state for a game in which no counters have been placed.
    The game state is a list of four elements:
        1. The first element is a list of 24 integers representing points on
        the board; for each integer returning 0 if the point is unoccupied, 1
        if the point contains a counter of player 1, and 2 if the point contains
        a counter of player 2. In this case 0 is returned for each integer as 
        board is empty.
        2. The second element returns the number of counters player 1 has in
        hand (9 in this case).
        3. The third element returns the number of counters player 2 has in 
        hand (9 in this case).
        4. The fourth element returns an integer, 1 or 2, represnting whether
        the player currently taking their turn is player 1 or 2, respectively.
        1 is returned in this case as Player 1 starts.
    """
    # We start with g as an empty list
    g = []
    # We then add an empty list to g, which we will turn into a list of 24 
    # elements
    g.append([]) 
    # Here we are appending 0 to the first element of g 24 times
    for i in range(24):
        g[0].append(0)
    p1_counters = 9
    p2_counters = 9
    active_player = 1
    # We then add the remaining elements to g
    g.extend([p1_counters, p2_counters, active_player]) 
    return g

def remaining_counters(g):
    """
    Takes a game state g and returns an integer representing the total number
    of counters that the current player (g[3]) has available. This is the sum
    of the number of counters the player has in hand and the number of counters
    they have on the board.
    """
    # The number of counters the current player has in hand is g[1] if g[3] = 1
    # or g[2] if g[3] = 2. The counters they have on the board is the number of
    # times g[3] appears in g[0]
    return g[g[3]] + g[0].count(g[3])
    

def is_in_mill(g, i):
    """
    A mill is formed if a player manages to occupy all 3 adjacent points in a 
    straight line. This function takes a game state g and an integer index of a 
    point i. 
    The function returns:
    - -1 if i is outside the range 0-23 inclusive, or if there is no counter at 
      point i
    - 0 if the counter at point i is not in a mill,
    - 1 if the counter at point i belongs to Player 1 and is in (one or more) 
      mills
    - 2 if the counter at point i belongs to Player 2 and is in (one or more) 
      mills
    """
    # A list of all the rows and columns of 3 on the board
    possible_mills = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17], [18, 19, 20], [21, 22, 23], [0, 9, 21], [3, 10, 18], [6, 11, 15], [1, 4, 7], [16, 19, 22], [8, 12, 17], [5, 13, 20], [2, 14, 23]]
    # If i is outside the range 0-23 inclusive, or there is no counter at point i
    if i<0 or i>=24 or g[0][i] == 0:
        return -1
    # We loop over the row/columns that point i belongs to (there are 16 
    # possible mills)
    for j in range(16): 
        if i in possible_mills[j]:
            # If the counter at point i belongs to Player 1/2 and is in (one or 
            # more) mills, this can be written as the counters on the board at 
            # the indexes of the points of the row/column being equal
            if g[0][possible_mills[j][0]] == g[0][possible_mills[j][1]] == g[0][possible_mills[j][2]]:
                # If it's Player 1's counter at i            
                if g[0][i] == 1: 
                    return 1
                # If it's Player 2's counter at i            
                elif g[0][i] == 2: 
                    return 2
    # If the above is not true in any case, the counter at point i is not in a
    # mill
    return 0
            

def player_can_move(g):
    """
    Takes a game state g and returns True if the current player has a valid move
    to make, or False if they do not. A player has a valid move to make if they
    have one or more counters left in hand, or if not, if any of their counters 
    on the board are next to an adjacent unoccupied space.
    """
    # If the current player has any counters left in hand
    if g[g[3]] > 0: 
        return True
    # For all the sets of adjacent points on the board, check if one of the
    # points contains a counter of the current player and the other point is
    # unoccupied. If there is at least one case of this, the current player can
    # move
    for i in range(24):
        for j in range(24):
            if is_adjacent(i, j) == True:
                if (g[0][i] == g[3] and g[0][j] == 0) or (g[0][j] == g[3] and g[0][i] == 0):
                        return True
    # If the above is not true in any case, the current player cannot move
    return False

def place_counter(g, i):
    """
    Takes a game state g and a point on the board i and places a counter of 
    the current player at this point. A RuntimeError is raised if there is
    already a counter at this point. This function updates the game state g
    to place the counter on the board and decrements the number of counters the
    current player has in their hand.
    """
    # If point i is not unoccupied, the current player cannot place a counter 
    # here
    if g[0][i] != 0: 
        raise RuntimeError("There is already a counter in position " + str(i)) 
    # Otherwise, we place the current player's counter at point i
    g[0][i] = g[3]
    # We update the game state to reduce the number of counters in the current 
    # player's hand by 1
    g[g[3]] += -1 

def move_counter(g, i, j):
    """
    Takes a game state g and two points i and j on the board, and moves the 
    current player's counter from point i to the adjacent point j. A
    RuntimeError is raised if this move is not possible, i.e., if i and j are not
    adjacent, if point i doesn't contain a counter of the current player, or if
    there is already a counter at point j. The function updates the game state
    g to reflect the moved counter.
    """
    # If points i and j are not adjacent
    if is_adjacent(i, j) == False:
        raise RuntimeError("Points " + str(i) + " and " + str(j) + " are not adjacent")
    # If the current player does not have a counter at point i
    elif g[0][i] != g[3]:
        raise RuntimeError("You don't have a counter at point " + str(i))
    # If there is already a counter at point j
    elif g[0][j] != 0:
        raise RuntimeError("There is already a counter at point " + str(j))
    # Otherwise, we move the counter from point i to j
    g[0][j] = g[0][i]
    # We update the game state to reflect that space i is now empty
    g[0][i] = 0

def remove_opponent_counter(g, i):
    """
    Takes a game state g and a point on the board i and removes the counter 
    currently at point i. A RuntimeError is raised if point i is NOT occupied 
    by a counter of the opposing player (i.e., the space is either empty or 
    occupied by a counter of the current player)
    """
    # If the current player has a counter at point i
    if g[0][i] == g[3]: 
        raise RuntimeError("Point " + str(i) + " is occupied by you")
    # If there is no counter at point i
    elif g[0][i] == 0: 
        raise RuntimeError("There is no counter at point " + str(i))
    # Otherwise, point i is occupied by the opposing player and we remove its
    # counter
    g[0][i] = 0 

def turn(g):
    """
    This function simulates taking a turn of the game. It takes a game state g
    and does the following five things in sequence:
        1) If the current player is unable to move or has otherwise lost the
           game, the function returns False without modifying g.
        
        2) If the current player has one or more counters in hand, the function:
            - Asks them where on the board they would like to place a counter 
              using request_location
            - Updates the game state g to place this counter
           
           **If the player gives an invalid location, or the placement is not 
           possible under the rules of the game, they are prompted to 
           enter the location again, until a valid placement is made.**
           
           Otherwise, the current player has no counters left in hand, so the 
           function:
            - Asks them which of their counters on the board they would like to 
              move using request_location
            - Asks them where on the board they would like to move said counter 
              to, again using request_location
            - Updates the game state g to move this counter
           
           **If the player gives invalid location(s), or the move is not 
           possible under the rules of the game, they are prompted to
           enter BOTH the locations again, until a valid move can be made.**
        
        3) If the play in step 2 has formed a mill, the current player is asked
           which opposing counter they would like to be removed, and the game
           state is updated to remove this counter. If an invalid location is 
           given, they are re-prompted until a valid location of an 
           opposing counter is provided.
        
        4) The game state is updated to switch the current player.
    
        5) True is returned to indicate that the game is not over yet.
    
    The function displays the board at appropriate points during the turn.
    """
    # We store the points on the board of the current player that are already 
    # in a mill so we can check whether they have in fact formed a new mill later
    mills_of_current_player_before_turn = [] 
    # Counting the number of counters of the current player that are in a mill
    for x in range(24):
        if is_in_mill(g, x) == g[3]:
            mills_of_current_player_before_turn.append(x)
    
    # If the current player can't move or has only two counters left on the
    # board, we return False. (Even though remaining_counters(g) is the sum of 
    # the counters the current player has in hand AND on the board, it is not 
    # possible for a player to have one counter on the board and one in hand, or 
    # none on the board and two in hand, so remaining_counters == 2 is 
    # sufficient to say they have 2 counters left on the board)
    if player_can_move(g) == False or remaining_counters(g) == 2:
        return False
    
    # We display the board so the player can see the available spaces
    draw_board(g)
    print("Player " + str(g[3]) + ", you are now the current player")
    # If the current player has at least one counter left in hand
    if g[g[3]] >= 1:
        # We continue prompting the user for input until they enter a valid input
        while True:
            try:
                i = request_location("Player " + str(g[3]) + ", where would you like to place your counter?")
                place_counter(g, i)
                # If the location is valid, move on to the next step
                break
            except RuntimeError as error_message:
                # If the location given is outside the range 0 to 23 inclusive
                if str(error_message) == "Not a valid location":
                    print(error_message)
                # If there is already a counter at this point on the board
                elif str(error_message) == "There is already a counter in position " + str(i):
                    print(error_message)
            # If the input is not a valid integer
            except ValueError: 
                print("Not a valid integer")
    # Otherwise, the player has no counters left in hand
    else: 
        # We continue prompting the user for input until they enter a valid input
        while True:
            try:
                i = request_location("Player " + str(g[3]) + ", which of your counters would you like to move?")
                j = request_location("Where would you like to move this counter to?")
                move_counter(g, i, j)
                # If the locations are valid, move on to the next step
                break
            except RuntimeError as error_message:
                # If the location i or j given is outside the range 0 to 23 
                # inclusive
                if str(error_message) == "Not a valid location":
                    print(error_message)
                # If the player doesn't have a counter at point i
                elif str(error_message) == "You don't have a counter at point " + str(i):
                    print("This move is not possible under the rules of the game:", error_message)
                # If the locations given are not adjacent
                elif str(error_message) == "Points " + str(i) + " and " + str(j) + " are not adjacent":
                    print("This move is not possible under the rules of the game:", error_message)
                # If there is already a counter at point j
                elif str(error_message) == "There is already a counter at point " + str(j):
                    print("This move is not possible under the rules of the game:", error_message)
            # If the input is not a valid integer
            except ValueError:
                print("Not a valid integer")

    # We want to compare how many counters of the current player are now in a 
    # mill compared to before their turn
    mills_of_current_player_after_turn = [] 
    # Counting the number of mills the current player now has
    for x in range(24):
        if is_in_mill(g, x) == g[3]:
            mills_of_current_player_after_turn.append(x)
    # If the number of the current player's counters in (one or more) mills is 
    # greater than it was before their turn, or if the number of their counters 
    # in (one or more) mills is the same but one of the points that is in (one 
    # or more) mills is different to before their turn, then the current player 
    # has formed a mill and hence they can remove an opposing counter
    if (len(mills_of_current_player_after_turn) > len(mills_of_current_player_before_turn)) or ((len(mills_of_current_player_after_turn) == len(mills_of_current_player_before_turn)) and (mills_of_current_player_before_turn != mills_of_current_player_after_turn)):
        # We display the board so the player can see the updated board
        draw_board(g)
        # We continue prompting the user for input until they enter a valid input
        while True:
            try:
                i = request_location("Player " + str(g[3]) + ", you have formed a mill! Which of the other player's counters would you like to remove?")
                remove_opponent_counter(g, i)
                # If the location is valid, move on to the next step
                break
            except RuntimeError as error_message:
                # If one of the current player's own counters is already here
                if str(error_message) == "Point " + str(i) + " is occupied by you":
                    print(error_message)
                # If the space is empty
                elif str(error_message) == "There is no counter at point " + str(i):
                    print(error_message)
                # If the location given is outside the range 0 to 23 inclusive
                elif str(error_message) == "Not a valid location":
                    print(error_message)
            # If the input is not a valid integer
            except ValueError:
                print("Not a valid integer")
    
    # Updating the game state to switch the current player
    # If Player 1 is the current player, switch to Player 2
    if g[3] == 1:
        g[3] = 2 
    # If Player 2 is the current player, switch to Player 1
    elif g[3] == 2:
        g[3] = 1 
    
    # If the game is not over yet
    return True

def save_state(g, filename):
    """
    Takes a game state g and a filename, and saves the game state g to a text
    file, naming it the name provided. A RuntimeError is raised if the file 
    cannot be saved. The text file saved has four lines, in the following format:
        Line 1) The board state g[0], stored as integers from g[0][0] to
                g[0][23], separated by spaces and commas (e.g. 0, 2, 1,...)
        Line 2) The number of counters Player 1 has in hand
        Line 3) The number of counters Player 2 has in hand
        Line 4) The number of the current player (1 or 2)
    """      
    try:
        # We use the write mode 'w' as we are writing into the file
        with open(filename, 'w') as f:
            # we convert the elements of g[0] into strings and separate them 
            # with commas
            board_state = ", ".join(str(el) for el in (g[0]))
            f.write(board_state + "\n") 
            # Number of counters Player 1 has in hand
            f.write(str(g[1]) + "\n")
            # Number of counters Player 2 has in hand
            f.write(str(g[2]) + "\n") 
            # Current player
            f.write(str(g[3])) 
    except OSError:
        raise RuntimeError("File cannot be saved")

def load_state(filename):
    """
    Takes a text file of the name given in the string filename and returns the 
    game state loaded from said file in its original form 
    (i.e. the list [[...], p1_counters, p2_counters, active_player]). A 
    RuntimeError is raised if the file cannot be loaded. The text file has four 
    lines, in the following format:
        Line 1) The board state g[0], stored as integers from g[0][0] to
                g[0][23], separated by spaces and commas (e.g. 0, 2, 1,...)
        Line 2) The number of counters Player 1 has in hand
        Line 3) The number of counters Player 2 has in hand
        Line 4) The number of the current player (1 or 2)
    """
    try:
        with open(filename) as f:
            # We start with g as an empty list
            g = []
            # We remove the new line character "\n" from the first line of the 
            # file using .strip()
            line_1 = f.readline().strip()
            # We split line 1 by its commas so that we can convert each number 
            # string in line 1 into an integer and create a list of these 
            # integers
            board_state = [int(el) for el in line_1.split(", ")]
            # We add this list to g
            g.append(board_state)
            # We have read the first line, so this for loop starts at line 2
            for line in f:
                # We convert lines 2, 3 and 4 into integers and add them to g
                g.append(int(line.strip()))
            return g
    except FileNotFoundError:
        raise RuntimeError("File not found")
    except PermissionError:
        raise RuntimeError("You do not have permission to access this file")
    except OSError:
        raise RuntimeError("File cannot be loaded")

def play_game():
    """
    Creates a new game state g and repeatedly calls turn(g) to simulate an
    entire game of Nine Men's Morris. Once the game is over, the winner is
    congratulated.
    """
    print("""
    Welcome to Nine Men's Morris! The board (shown below) starts with no 
    counters on it, and each player starts with nine counters in their hand. 
    Starting with Player 1, players take it in turns to place their counters on 
    unoccupied points on the board. If, in placing a piece, a player manages to 
    occupy all three adjacent points on a straight line with one of their counters 
    (called forming a mill), then they may then remove one of their opponent's 
    counters from the board. Such removed counters play no further part in the 
    game. Only one opposing counter may be removed per turn, even if more than 
    one mill is created. This continues until both players have placed all their 
    counters.

    Players continue to alternate turns. In a turn, a player moves one of their 
    counters along a line to an adjacent unoccupied point. As before, if this 
    move forms a mill, then the player removes one of their opponent's counters 
    from the board. A player loses if they are unable to move any of their 
    pieces, or if they have only two counters left on the board.
          """)
    # We start with a new game
    g = new_game() 
    # While the game is still going, the players continue to take turns
    while turn(g) == True: 
        turn(g)
        # Once someone has lost the game, we exit this loop
        if turn(g) == False:
            break
    # The current player is the player who has lost
    if g[3] == 1:
        winner = 2
    if g[3] == 2:
        winner = 1
    print("Congratulations Player " + str(winner) + ", you are the winner!")

    
def main():
    # You could add some tests to main()
    # to check your functions are working as expected

    # The main function will not be assessed. All code to
    # play the game should be in the play_game() function,
    # and so your main function should simply call this.
    print("Game board with new game:", draw_board(new_game()))
    print("Game board with example game (counters in hand):", draw_board([[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0], 3, 4, 2]))
    print("Game board with example game (no counters in hand):", draw_board([[1, 2, 1, 2, 1, 2, 0, 2, 0, 0, 2, 1, 1, 2, 1, 0, 0, 0, 2, 1, 2, 1, 2, 1], 0, 0, 2]))
    
    # Problem 1 tests (is_adjacent(i,j))
    print("Problem 1 tests")
    print("Should return True:", is_adjacent(1, 2))
    print("Should return True:", is_adjacent(4, 1))
    print("Should return False:", is_adjacent(19, 19))
    print("Should return False:", is_adjacent(2, 3))
    
    # Problem 2 tests (new_game())
    print("Problem 2 tests")
    print("Game state of new game:", new_game())
    
    # Problem 3 tests (remaining_counters(g))
    print("Problem 3 tests")
    print("Should return 9:", remaining_counters([[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0], 3, 4, 2]))
    print("Should return 9:", remaining_counters(new_game()))
    print("Should return 3:", remaining_counters([[0, 1, 2, 0, 1, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], 0, 0, 2]))
    
    # Problem 4 tests (is_in_mill(g, i))
    print("Problem 4 tests")
    print("Should return -1", is_in_mill([[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0], 3, 4, 2], -1))
    print("Should return -1", is_in_mill([[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0], 3, 4, 2], 0))
    print("Should return 0", is_in_mill([[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0], 3, 4, 2], 8))
    print("Should return 1", is_in_mill([[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0], 3, 4, 2], 4))
    
    # Problem 5 tests (player_can_move(g))
    print("Problem 5 tests")
    print("Should return True:", player_can_move([[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0], 3, 4, 2]))
    print(draw_board([[1, 2, 1, 2, 1, 2, 0, 2, 0, 0, 2, 1, 1, 2, 1, 0, 0, 0, 2, 1, 2, 1, 2, 1], 0, 0, 2]))
    print("Should return True:", player_can_move([[1, 2, 1, 2, 1, 2, 0, 2, 0, 0, 2, 1, 1, 2, 1, 0, 0, 0, 2, 1, 2, 1, 2, 1], 0, 0, 2]))
    print("Should return False:", player_can_move([[1, 2, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 2, 1], 0, 0, 2]))
    
    # Problem 6 tests (place_counter(g, i))
    print("Problem 6 tests")
    #print("Should raise RuntimeError:", place_counter([[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0], 3, 4, 2], 19))
    #print("Should add a '2' in position 21", place_counter([[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0], 3, 4, 2], 21))
    
    # Problem 7 tests (move_counter(g, i, j))
    #print("Problem 7 tests")
    #print ("Should raise RuntimeError due to 10 and 15 not being adjacent", move_counter([[1, 2, 1, 2, 1, 2, 0, 2, 0, 0, 2, 1, 1, 2, 1, 0, 0, 0, 2, 1, 2, 1, 2, 1], 0, 0, 2], 10, 15))
    #print ("Should raise RuntimeError due to player not having a counter at point 0", move_counter([[1, 2, 1, 2, 1, 2, 0, 2, 0, 0, 2, 1, 1, 2, 1, 0, 0, 0, 2, 1, 2, 1, 2, 1], 0, 0, 2], 0, 9))
    #print ("Should raise RuntimeError due to there already being a counter at point 11", move_counter([[1, 2, 1, 2, 1, 2, 0, 2, 0, 0, 2, 1, 1, 2, 1, 0, 0, 0, 2, 1, 2, 1, 2, 1], 0, 0, 2], 10, 11))
    #print("Should move a 2 from 10 to 9", move_counter([[1, 2, 1, 2, 1, 2, 0, 2, 0, 0, 2, 1, 1, 2, 1, 0, 0, 0, 2, 1, 2, 1, 2, 1], 0, 0, 2], 10, 9))
    
    # Problem 8 tests (remove_opponent_counter(g, i))
    #print("Problem 8 tests")
    #print("Should raise RuntimeError due to current player having a counter at point 22", remove_opponent_counter([[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0], 3, 4, 2], 22))
    #print("Should raise RuntimeError due to there being no counter at point 6", remove_opponent_counter([[1, 2, 1, 2, 1, 2, 0, 2, 0, 0, 2, 1, 1, 2, 1, 0, 0, 0, 2, 1, 2, 1, 2, 1], 0, 0, 2], 6))
    #print("Should remove Player 1's counter at point 1", remove_opponent_counter([[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0], 3, 4, 2], 1))
    
    # Problem 9 tests (turn(g))
    #print("Problem 9 tests")
    #print(turn(new_game()))
    
    # Problem 10 tests (save_state(g, filename) and load_state(g, filename))
    print("Problem 10 tests")
    print(save_state([[0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 0, 2, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 2, 0], 3, 4, 2], 'my_file2.txt'))
    g_new = load_state("my_file2.txt")
    print(g_new)
    
    play_game()
    
main()