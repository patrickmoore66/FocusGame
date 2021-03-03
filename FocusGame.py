# Author: Patrick Moore
# Date: 12/2/2020
# Description: Program allows players to play an abstraction of the board game Focus/Domination. The board is
# simplified to a 6x6 grid, ignoring the 1x4 areas on the outside.Has a Player class, a Stack class, and a FocusGame
# class.Either Player can start then game, then turns alternate. Players can only move a piece or stack that they
# control. (The top piece of the stack is their color) The goal of the game is to capture 6 of the enemies pieces.
# Pieces are captured or placed in reserve when a stack is larger than 5 pieces tall as a result of a move. If a move
# is illegal, the game will print an error message and return False.

import pygame
from pygame.locals import *



class Player:
    """
    Represents a player of the game, with each player having a name, color, reserve pieces list, and a captured
    pieces list. Contains an initialization method that takes a name and a color, and get methods for every field.
    Has add functions to add a piece to the reserves or captured list.
    """
    def __init__(self, name, color):
        """
        Initializes a Player with a name and color, and reserves and captured list set to null lists.
        :param name: The name of the player
        :param color: The color/team of the player
        """
        self._name = name
        self._color = color
        self._reserves = []
        self._captured = []

    def get_name(self):
        """
        Returns the name of the player
        :return: The name of the player
        """
        return self._name

    def get_color(self):
        """
        Returns the color(team) of the player
        :return: The color of the player
        """
        return self._color

    def get_reserves(self):
        """
        Returns the reserve list of the player
        :return: The reserves list of the player
        """
        return self._reserves

    def add_reserve(self, piece):
        """
        Adds a piece passed as a parameter to the reserve list of the player
        :param piece: A string containing 'G' or 'R' representing a focus game piece
        """
        self._reserves.append(piece)

    def sub_reserve(self):
        if self._reserves[0] != []:
            del self._reserves[0]
        else:
            print("No reserves")
            return False

    def get_captured(self):
        """
        Returns the captured list of the player
        :return: The captured list of the player
        """
        return self._captured

    def add_captured(self, piece):
        """
        Adds a piece to the captured list
        :param piece:A string containing 'G' or 'R' representing a focus game piece
        """
        self._captured.append(piece)


class Stack:
    """
    Represents a stack of piece(s) on the board. Each stack has a color, size, and location on the board
    initialized as a private data member. Has get methods for every field. Has methods to add and remove pieces to
    the bottom of the stack, and a method to add a piece to the top of the stack.  Also has a get method to specifically get the
    bottom piece of the stack
    """
    def __init__(self, color):
        """
        Initializes a Stack object representing a stack of focus pieces.
        :param color: The controlling color of the stack, i.e. the player's color must match the stack color
        to move the stack.(may phase this out in favor of looking at self._pieces[0] to determine "control" of
        the stack) (Size may also be phased out in favor of using len(self._pieces))
        """
        self._color = color
        self._size = 1
        self._pieces =[color]

    def get_color(self):
        """
        Gets the controlling color of the stack
        :return: The controlling color of the stack, a string of either "G" or "R"
        """
        return self._color

    def get_size(self):
        """
        Gets the number of pieces or size of the stack
        :return: The size of the stack, an integer
        """
        return self._size


    def add_bottom_piece(self, color):
        """
        Adds a piece represented by a color entry in a list to the bottom of the stack/end of the pieces list
        (Note: Will I ever need to add a piece to the bottom?)
        :param color: A string containing "G" or "R", representing a focus piece.
        """
        self._pieces.append(color)
        self._size += 1

    def sub_bottom_piece(self):
        """
        Removes the last piece in the list by slicing at index :-1
        """
        self._pieces = self._pieces[:-1]
        self._size -= 1

    def add_piece_to_top(self, piece):
        """
        Adds a piece to the top controlling position of the stack
        :param piece: A string containing "G" or "R" representing a focus piece
        """
        self._pieces.insert(0, piece)
        self._size += 1

    def get_stack_list(self):
        """
        Gets the list of pieces on the stack, with the 0th piece as the "top" piece
        :return: A list of pieces in the stack
        """
        return self._pieces

    def get_bottom_piece(self):
        """
        Returns the color of the piece at the bottom of the stack of pieces. Returns None if there are no pieces
        in the stack
        :return: None if the stack has no pieces, the last piece of the pieces list if not.
        """

        if self._pieces == []:
            print("no pieces")
            return None
        else:
            return self._pieces[(len(self._pieces) - 1)]



class FocusGame:
    """
    Abstracts the game of Focus/Domination. Initializes the board with pieces placed and two Players. Contains an
    initialization method that takes two tuples with a player name and color, and fills the board. Has a make_move
    method which validates the move input by the user, makes the move, and checks if a player has won. The
    process_move method assists the make move function, and the class also has methods to show captured and reserved
     pieces, pieces at a given location, as well as a method to print the game board. Has methods to validate the users
     move, whose turn it is, whether or not a player has won, and to place a reserved piece. Has a method to change
     turns, a method to get a player object when given a player name.
    """

    def __init__(self, player1, player2):
        """
        Takes as its parameters two tuples, each containing player name and color of the piece that player is
        playing  and it initializes the board  and then calls the fill_board function to fill the board
        with the pieces placed in the correct positions.
        """
        if player1[1] == player2[1]:
            print("Players must be on different teams")
        else:
            self._players = []
            self._players.append(Player(player1[0], player1[1]))
            self._players.append(Player(player2[0], player2[1]))
            self._turn = None

            self._board = [[],[],[],[],[],[]]
            for row in self._board:
                i = 0
                while i<6:
                    row.append([])
                    i+=1

            self.fill_board(self._board)                            #fill the board


    def fill_board(self, board):
        """
        Initializes the game board according to diagram given in the README
        :param board: a list made up of 6 null lists
        """
        i = 0
        piece1 = self._players[0].get_color()
        piece2 = self._players[1].get_color()
        while i < 6:
            board[i] = [Stack(piece1),Stack(piece1),Stack(piece2), Stack(piece2), Stack(piece1), Stack(piece1)]
            i+=2

        i = 1
        while i < 6:
            board[i] = [Stack(piece2),Stack(piece2),Stack(piece1),Stack(piece1),Stack(piece2),Stack(piece2)]
            i+=2

    def move_piece(self, player, start, move, num_pieces):
        """
        Takes the following parameters in order: the player name who is making the move, a tuple that represents the
        coordinate from where the move is being made, another tuple that represents the location to where the move
        is being made, an integer that represents the number of pieces that are being moved. It returns an error or
        proper message if the following scenarios occur. If a player is trying to make a move out of turn returns
        'not your turn.' If the player provides invalid locations (source or destination), return 'invalid location.'
        If the player is trying to move invalid number of pieces, return 'invalid number of pieces.' It returns
        'successfully moved' message if the move was successful. If the move makes the player win, it returns
        <player name> Wins message (e.g. "PlayerB Wins") If the number of pieces at the moved location are more than
         5 in number, then it automatically captures bottom pieces if they belong to other player and moves to
         current players reserve if the pieces belong to current player
        :param player: The name of the player making the move
        :param start: The tuple coordinates (row, column) the player wants to start from
        :param move: The tuple coordinates (row, column) the player wants to end at
        :param num_pieces:The number of pieces the player wants to move
        :return: returns 0 and prints an error message
        """
        if self.check_turn(player) == False:
            return False
        elif self.check_move(player, start, move, num_pieces) == False:
            return False
        else:
            self.process_move(start,move,num_pieces, player)

            if self.check_win(player) == False:               #check win, update turn, and return
                self.change_turn(player)
                print("Changed turn to")
                print(self.get_turn())
                return 'successfully moved'
            else:
                self._turn = 1
                return player + " wins"

    def process_move(self, start, move, num_pieces, player):
        """
        Assists the make_move method in processing the players move. This function specifically notes the stack of
        pieces being moved, removes them from their source stack, combines the stack being moved with the stack
        (if any) already at the destination. If the newly combined stack is longer than 5 pieces, the pieces at the
        bottom of the stack past 5 are captured or placed in reserve as appropriate.
        :param start: Tuple of the coordinates on the board where the move is starting
        :param move: Tuple of the coordinates on the board where the move will end
        :param num_pieces: The number of pieces the user wishes to move from the start coordinates
        :param player: String identifying the player making the move.
        """
        temp_list  = [None] * num_pieces
        i = 0
        while i < num_pieces:
            temp_list[i] = self._board[start[0]][start[1]].get_stack_list()[i]
            i += 1

        if num_pieces == len(self._board[start[0]][start[1]].get_stack_list()):  #clear starting position appropriate number of spots
            self._board[start[0]][start[1]] = None
        else:
            i = 0
            while i < num_pieces:
                del self._board[start[0]][start[1]].get_stack_list()[0]
                i+=1

        i = len(temp_list)                                                      #combine stacks
        while i >= 1:
            temp_piece = temp_list[i-1]
            if self._board[move[0]][move[1]] == None or self._board[move[0]][move[1]] == []:
                print("HEYOOOOOOO")
                self._board[move[0]][move[1]] = Stack(temp_piece)
                i -= 1
            else:
                self._board[move[0]][move[1]].add_piece_to_top(temp_piece)
                i -= 1

        while len(self._board[move[0]][move[1]].get_stack_list()) > 5:         #capture or reserve pieces
            captured_piece = self._board[move[0]][move[1]].get_bottom_piece()
            self._board[move[0]][move[1]].sub_bottom_piece()
            if captured_piece == self.get_player(player).get_color():
                self.get_player(player).add_reserve(captured_piece)
            else:
                self.get_player(player).add_captured(captured_piece)


    def show_pieces(self, location):
        """
        Takes a position on the board and returns a list showing the pieces that are present at that location with
        the bottom-most pieces at the 0th index of the array and other pieces on it in the order.
        :param location: - The coordinates at which to show the pieces, as a tuple
        :return:None if there are no pieces at the location,otherwise returns a list of pieces with the bottommost
        piece at the 0th index.
        """
        if self._board[location[0]][location[1]] == None:
            print("No pieces")
            return False
        else:
            list = self._board[location[0]][location[1]].get_stack_list()
            list.reverse()
            return list

    def show_reserve(self, player_name):
        """
        Takes the player name as the parameter and shows the count of pieces that are in reserve for the player.
        If no pieces are in reserve, return 0.
        :param player_name: The name of the player whose reserve count is to be shown
        :return:0 if the player has no reserves, otherwise the number of reserve pieces the player has
        """
        player = self.get_player(player_name)
        if player.get_reserves() == 0:
            return 0
        else:
            return len(player.get_reserves())

    def show_captured(self, player_name):
        """
        Takes the player name as the parameter and shows the number of pieces captured by that player. If no pieces
        have been captured, return 0.
        :param player_name: The name of the player whose captured pieces are to be shown
        :return: The number of pieces captured by the player
        """
        player = self.get_player(player_name)
        if player.get_captured() == 0:
            return 0
        else:
            return len(player.get_captured())


    def reserved_move(self, player, move):
        """
        Takes the player name and the location on the board as the parameters. It places the piece from the reserve
        to the location. Reduces the reserve pieces of that player by one and make appropriate adjustments to
        pieces at the location. If there are no pieces in reserve, returns 'no pieces in reserve'
        :param player: Name of the player making the move
        :param move: Tuple coordinates denoting where the play would like to place a reserve piece
        :return: 0 and an error message if the move cannot be made, otherwise just returns
        """
        if self.check_reserved_move(player, move) == False:
            return False
        else:
            piece = self.get_player(player).get_color()

            if self._board[move[0]][move[1]] == None:                                   # empty space
                self._board[move[0]][move[1]] = Stack(piece)
                self.get_player(player).sub_reserve()                                   #remove piece from reserved list
                self.change_turn(player)
                return "successfully moved"
            else:                                                                       #space has an existing stack on it
                self._board[move[0]][move[1]].add_piece_to_top(piece)
                self.get_player(player).sub_reserve()
                self.change_turn(player)

                while len(self._board[move[0]][move[1]].get_stack_list()) > 5:          #capture and check win conditions
                    captured_piece = self._board[move[0]][move[1]].get_bottom_piece()
                    self._board[move[0]][move[1]].sub_bottom_piece()
                    if captured_piece == self.get_player(player).get_color():
                        self.get_player(player).add_reserve(captured_piece)
                    else:
                        self.get_player(player).add_captured(captured_piece)

                if self.check_win(player) == False:
                    return 'successfully moved'
                else:
                    self._turn = 1
                    return player + " wins"

    def print_board(self):
        """
        Displays the game board because visualizing the board can be helpful
        """
        for row in self._board:
            for stack in row:
                if stack == None:
                    print("X", end = '      ')
                else:
                    print(stack.get_stack_list()[0] + str(len(stack._pieces)), end = '      ')
            print("\n")


    def check_win(self, player):
        """
        Returns True if the player's captured list is 6 or more pieces long, otherwise returns False
        :param player: Player whose win condition is to be checked
        :return: True if the player has captured 6 or more pieces and has won, False if not
        """
        for user in self._players:
            if user.get_name() == player:
                if len(user.get_captured()) >= 6:
                    return True
        else:
            return False

    def check_turn(self, player):
        """
        Checks that the parameter of player passed matches the game's turn, otherwise prints "Not your turn"
        and returns false. If this is the first move and self._turn == None, sets self._turn to equal the player
        making the move, and returns True.
        :param player: Name of the player to be checked
        :return: True if it is the first turn or it is the turn of the player given by the parameter, False otherwise
        """
        if self._turn == None:
            self._turn = player
            return True
        elif self._turn == 1:
            print("Game is over")
            return False
        elif self._turn != player:
            print("not your turn")
            return False
        else:
            return True

    def check_move(self, player, start, move, num_pieces):
        """
        Checks that the player's move is valid by checking that the player owns the stack at start, that the number
        of pieces selected match the move, that the move is possible, and that the destination is within the
        boundaries of the board
        :param player:  Name of the player trying to make the move
        :param start: Tuple coordinates of the space the user would like to start from
        :param move: Tuple coordinates of the space the user would like to finish at
        :param num_pieces: The number of pieces the user would like to move
        :return: False if move is invalid, along with a printed message, True if the move is valid.
        """
        #check player owns the stack self.check_coords(start, move) == False:
        if self.check_coords(start, move) == False:
            return False
        elif self._board[start[0]][start[1]] == None or self._board[start[0]][start[1]] == []:
            print("invalid location(not your piece)")
            return False
        elif self.get_player(player).get_color() != self._board[start[0]][start[1]].get_stack_list()[0]:
            print("invalid location(not your piece)")
            return False
        # check number of pieces
        elif num_pieces > self._board[start[0]][start[1]].get_size() or num_pieces < 1:
            print("invalid number of pieces")
            return False
        else:
            #check the move
            if (start[0] + num_pieces) == move[0] and start[1] == move[1]:
                return True
            elif (start[0] - num_pieces) == move[0] and start[1] == move[1] :
                return True
            elif (start[1] + num_pieces) == move[1] and start[0] == move[0]:
                return True
            elif (start[1] - num_pieces) == move[1] and start[0] == move[0]:
                return True
            else:
                print("invalid location(move not possible)")
                return False

    def check_reserved_move(self, player, move):
        """
        Takes a player name and a tuple of coordinates as parameters, and checks that the player's reserved move
        is valid. Checks that the player has a reserve piece to use, that it is that player's turn, and that the
        coordinates of the move are on the game board.
        :param player:A string of a player's name
        :param move: A tuple of coordinates between 0 and 5 where the player is trying to place a piece
        :return: False if the move is invalid, True if it is valid
        """
        if self.get_player(player).get_reserves() == []:
            print("No pieces in reserve")
            return False
        elif self.check_turn(player) == False:
            return False
        elif move[0] < 0 or move[0] > 5:
            print("Move coordinates invalid")
            return False
        elif move[1] < 0 or move[1] > 5:
            print("Move coordinates invalid")
            return False
        else:
            return True

    def check_coords(self, start, destination):
        """
        Checks that the user input coordinates fall inside of the game board.
        :param start: Tuple coordinates the user would like to start at
        :param destination: Tuple coordinates the user would like to finish at
        :return: False if the move is invalid, True if the move is valid
        """
        if start[0] < 0 or start[0] > 5:
            print("Source coordinates invalid")
            return False
        elif start[1] < 0 or start[1] > 5:
            print("Source coordinates invalid")
            return False
        elif destination[0] < 0 or destination[0] > 5:
            print("Destination coordinates invalid")
            return False
        elif destination[1] < 0 or destination[1] >5:
            print("Destination coordinates invalid")
            return False
        else:
            return True


    def get_player(self, player):
        """
        Returns player object from list of players, takes a player name as a parameter
        :param player: Name of the player to be found
        :return: A Player object with the same name as the parameter, or None if the player is not found
        """
        for user in self._players:
            if user.get_name() == player:
                return user
        print("Player not found")
        return None

    def change_turn(self, player):
        """
        Switches the turn to the other player.
        :param player: Player making the move, whose turn it will no longer be
        """
        if self._players[0].get_name() == player:
            self._turn = self._players[1].get_name()
        else:
            self._turn = self._players[0].get_name()

    def get_turn(self):
        """
        gets the current player whose turn it is
        :return: the player whose turn it is as a string
        """
        return self._turn


class FocusDisplay:

    def __init__(self):
        """

        """
        # initialize
        pygame.init()

        # define colors
        BLACK = (0, 0, 0)
        GRAY = (127, 127, 127)
        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        GREEN = (0, 255, 0)
        BLUE = (0, 0, 255)

        self.create_board(BLACK, WHITE, BLUE, RED, GREEN)

    def run_game(self, screen, RED, GREEN):
        #Run unitl user quits
        BLACK = (0,0,0)
        WHITE = (255,255,255)
        BLUE = (0,0,255)
        running = True
        move = (None, None)
        pieces = 1

        while running:

            #update board:
            self.fill_pieces(screen, RED, GREEN, game)
            pygame.display.flip()

            #Did the user click close?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    print(event)
                #MOUSEBUTTONUP represents the user selecting a space
                elif event.type == MOUSEBUTTONUP:
                    if move == (None, None):
                        print(event)
                        mpos_x, mpos_y = event.pos
                        move = self.translate_click(mpos_x, mpos_y)
                        print(move)
                        print("start")
                    else:
                        print(event)
                        mpos_x, mpos_y = event.pos
                        end = self.translate_click(mpos_x, mpos_y)
                        turn = game.get_turn()
                        print(turn)
                        if turn == None:
                            turn = "PlayerA"
                            game.move_piece(turn, move, end, pieces)
                            move = (None, None)
                            self.create_board(BLACK, WHITE, BLUE, RED, GREEN)
                            self.fill_pieces(screen, RED, GREEN, game)
                            pygame.display.flip()
                        else:
                            game.move_piece(turn, move, end, pieces)
                            move = (None, None)
                            self.create_board(BLACK, WHITE, BLUE, RED, GREEN)
                            self.fill_pieces(screen, RED, GREEN, game)
                            pygame.display.flip()

        pygame.quit()

    def draw_grid_vert(self, start_pos, end_pos, width, screen, color):
        """
        Draws the vertical lines of the game board separating spaces
        :param start_pos:
        :param end_pos:
        :param width:
        :param height:
        :return:
        """

        pygame.draw.line(screen, color, start_pos, end_pos, width)
        i = 0
        temp_start = start_pos[0]
        temp_end = end_pos[0]

        while i <= 6:
            pygame.draw.line(screen, color, (temp_start,start_pos[1]), (temp_end, end_pos[1]), width)
            temp_start += 75
            temp_end += 75
            i += 1

        return


    def draw_grid_horizontal(self, start_pos, end_pos, width, screen, color):
        """
        Draws a horizontal set of lines
        :param start_pos:
        :param end_pos:
        :param width:
        :param screen:
        :param color:
        :return:
        """
        pygame.draw.line(screen, color, start_pos, end_pos, width)
        i = 0
        temp_start = start_pos[1]
        temp_end = end_pos[1]

        while i <= 6:
            pygame.draw.line(screen, color, (start_pos[0],temp_start), (end_pos[0], temp_end), width)
            temp_start += 75
            temp_end += 75
            i += 1

        return

    def create_board(self, BLACK, WHITE, BLUE, RED, GREEN):
        """

        :return:
        """

        # make a window
        screen = pygame.display.set_mode((950, 500))
        screen.fill(WHITE)

        #window caption
        pygame.display.set_caption("Focus the game!")

        #make the board
        pygame.draw.rect(screen, BLACK, (50, 20, 450, 450))

        #draw vertical lines
        self.draw_grid_vert((50, 20), (50, 470), 2, screen, BLUE)

        #draw horizontal lines
        self.draw_grid_horizontal((50, 20), (500, 20), 2, screen, BLUE)

        #display
        pygame.display.flip()
        self.run_game(screen, RED, GREEN)

    def fill_pieces(self, screen, RED, GREEN, game):
        """

        :param screen:
        :param RED:
        :param GREEN:
        :param game:
        :return:
        """
        left_coord = 80
        top_coord = 84

        for row in game._board:
            for stack in row:
                if stack == None:
                    j = 0
                    while j < 6:
                        pygame.draw.rect(screen, (0,0,0), (left_coord, top_coord, 20, 10))
                        top_coord -= 11
                        j += 1
                    top_coord += j * 11

                else:
                    temp_stack = stack.get_stack_list()
                    temp_stack.reverse()
                    counter = len(stack.get_stack_list())
                    i = 0
                    while i < counter:
                        if temp_stack[i] == "R":
                            pygame.draw.rect(screen, RED, (left_coord, top_coord, 20, 10))
                            top_coord -= 11
                            i+=1
                        else:
                            pygame.draw.rect(screen, GREEN, (left_coord, top_coord, 20, 10))
                            top_coord -= 11
                            i+=1
                    temp_stack.reverse()
                    top_coord += i*11
                left_coord += 75

            #reset to left side
            left_coord = 80
            top_coord += 75


    def translate_click(self, mpos_x, mpos_y):
        """
        Determines the column and row of the board selected by the user with a MOUSEBUTTONUP event
        :param mpos_x: X-axis position of the mouse at the time of the event
        :param mpos_y: Y-axis position of the mouse at the time of the event
        :return: A tuple of coordinates on the board, able to be understood by the game
        """

        row = None
        column = None

        if mpos_x < 50 or mpos_x > 500:
            print("Please select a valid square")
            return False
        else:
            if mpos_x >= 50 and mpos_x <= 125:
                column = 0
                row = self.translate_click_y(mpos_y)
                return (row, column)
            elif mpos_x > 125 and mpos_x <= 200:
                column = 1
                row = self.translate_click_y(mpos_y)
                return (row, column)
            elif mpos_x > 200 and mpos_x <= 275:
                column = 2
                row = self.translate_click_y(mpos_y)
                return (row, column)
            elif mpos_x > 275 and mpos_x <= 350:
                column = 3
                row = self.translate_click_y(mpos_y)
                return (row, column)
            elif mpos_x > 350 and mpos_x <= 425:
                column = 4
                row = self.translate_click_y(mpos_y)
                return (row, column)
            elif mpos_x > 425 and mpos_x <= 500:
                column = 5
                row = self.translate_click_y(mpos_y)
                return (row, column)

    def translate_click_y(self, mpos_y):
        """
        Determines the row of the board selected by the user with a MOUSEBUTTONUP
        :param mpos_y: Position of the mouse at the time of the MOUSEBUTTONUP event
        :return:integer representing with row the user selected
        """

        if mpos_y < 20 or mpos_y > 470:
            return False
        else:
            if mpos_y >= 20 and mpos_y < 95:
                return 0
            elif mpos_y >= 95 and mpos_y < 170:
                return 1
            elif mpos_y >= 170 and mpos_y < 245:
                return 2
            elif mpos_y >= 245 and mpos_y < 320:
                return 3
            elif mpos_y >= 320 and mpos_y < 395:
                return 4
            elif mpos_y >= 395 and mpos_y <= 470:
                return 5

if __name__ == '__main__':
    p1 = ('PlayerA', 'R')
    p2 = ('PlayerB', 'G')
    game = FocusGame(p1, p2)
    game_screen = FocusDisplay()




