# Name: Courtlen Olmo
# Github Username: Mango-bear
# Date: 3/16/23
# Description: Functional Checkers game with error checking. Create a game object, player objects, then play game by
# calling game.play_game with the player name, starting square tuple, destination square tuple.

class OutofTurn(Exception):
    '''Raise when a player attempts to move a piece when it's not their turn'''
    pass


class InvalidSquare(Exception):
    '''Raise if the player doesn't own the checker in the selected square location'''
    pass


class InvalidPlayer(Exception):
    '''Raise if the players name is not valid'''
    pass


class InvalidSquare(Exception):
    '''Raise if square location doesn't exist'''
    pass


class Checkers():
    '''Contains various methods to interact with the chessboard.'''

    def __init__(self):
        self._game_board = {0: [None, 'White', None, 'White', None, 'White', None, 'White'],
                            1: ['White', None, 'White', None, 'White', None, 'White', None],
                            2: [None, 'White', None, 'White', None, 'White', None, 'White'],
                            3: [None, None, None, None, None, None, None, None],
                            4: [None, None, None, None, None, None, None, None],
                            5: ['Black', None, 'Black', None, 'Black', None, 'Black', None],
                            6: [None, 'Black', None, 'Black', None, 'Black', None, 'Black'],
                            7: ['Black', None, 'Black', None, 'Black', None, 'Black', None]}
        self._black_turn = True
        self._players = {}

    def check_if_valid_square(self, square_location):
        '''Checks to make sure that the passed square is valid'''
        if list(square_location)[0] > 7 or list(square_location)[1] > 7 \
                or list(square_location)[0] < 0 or list(square_location)[1] < 0:
            return False
        else:
            return True

    def create_player(self, player_name, piece_color):
        '''Creates Player object and adds it to the players dictionary'''
        self._players.update({player_name: Player(player_name, piece_color)})

    def play_game_error_check(self, player_name, starting_square_location, destination_square_location):
        '''Checks to make sure that the arguments passed to play_game function are valid.'''
        if self._black_turn is True and self._players.get(player_name).get_color() == 'White':
            raise OutofTurn
        elif self._black_turn is False and self._players.get(player_name).get_color() == 'Black':
            raise OutofTurn
        elif self.check_if_valid_square(starting_square_location) is False:
            raise InvalidSquare
        elif self.check_if_valid_square(destination_square_location) is False:
            raise InvalidSquare

    def play_game(self, player_name, starting_square_location, destination_square_location):
        '''Check if piece is white or black, calls error checking, calls movement function for the given color, if a
        is captured during movement do not switch turns'''
        if player_name not in self._players:
            raise InvalidPlayer
        if self._black_turn == True:
            self.play_game_error_check(player_name, starting_square_location, destination_square_location)
            if self.get_checkers_details(starting_square_location) == 'Black':
                # Before and after play variables determine whether player gets another turn or not
                before_play = self._players.get(player_name).get_captured_pieces_count()
                self.black_piece_movements(player_name, starting_square_location, destination_square_location)
                after_play = self._players.get(player_name).get_captured_pieces_count()
                if after_play > before_play:
                    self._black_turn = True
                    return after_play - before_play
                else:
                    self._black_turn = False
                    return 0
            elif self.get_checkers_details(starting_square_location) == "Black_king" \
                    or self.get_checkers_details(starting_square_location) == 'Triple_Black_king':
                before_play = self._players.get(player_name).get_captured_pieces_count()
                self.black_king_movements(player_name, starting_square_location, destination_square_location)
                after_play = self._players.get(player_name).get_captured_pieces_count()
                if after_play > before_play:
                    self._black_turn = True
                    return after_play - before_play
                else:
                    self._black_turn = False
                    return 0

        if self._black_turn == False:
            self.play_game_error_check(player_name, starting_square_location, destination_square_location)

            # Before and after play variables determine whether player gets another turn or not
            if self.get_checkers_details(starting_square_location) == 'White':
                before_play = self._players.get(player_name).get_captured_pieces_count()
                self.white_piece_movements(player_name, starting_square_location, destination_square_location)
                after_play = self._players.get(player_name).get_captured_pieces_count()
                if after_play > before_play:
                    self._black_turn = False
                    return after_play - before_play
                else:
                    self._black_turn = True
                    return 0
            elif self.get_checkers_details(starting_square_location) == 'White_king' \
                    or self.get_checkers_details(starting_square_location) == 'Triple_White_king':
                before_play = self._players.get(player_name).get_captured_pieces_count()
                self.black_king_movements(player_name, starting_square_location, destination_square_location)
                after_play = self._players.get(player_name).get_captured_pieces_count()
                if after_play > before_play:
                    self._black_turn = False
                    return after_play - before_play
                else:
                    self._black_turn = True
                    return 0

    def black_piece_movements(self, player_name, starting_square_location, destination_square_location):
        '''Create a list of valid movement options, check to see what is in those spaces. If it's none, set the
        starting_Square to None and the destination to Black.if it's white, add a new possible move, change the white
        square to none, and move the black piece'''
        destination_value = self.get_checkers_details(destination_square_location)
        possible_moves = [[list(starting_square_location)[0] - 1,
                           list(starting_square_location)[1] + 1],
                          [list(starting_square_location)[0] - 1,
                           list(starting_square_location)[1] - 1]]

        if list(destination_square_location)[1] - list(starting_square_location)[1] > 0:
            y_direction = 'right'
        else:
            y_direction = 'left'

        # Jump piece to the right
        if y_direction == 'right':
            try:
                if self.get_checkers_details(possible_moves[0]) == 'White' \
                        or self.get_checkers_details(possible_moves[0]) == 'White_king' \
                        or self.get_checkers_details(possible_moves[0]) == 'Triple_White_king' \
                        and destination_value is None:
                    self._players.get(player_name).set_captured_pieces()
                    self._game_board[list(starting_square_location)[0]][list(starting_square_location)[1]] = None
                    self._game_board[list(starting_square_location)[0] - 1][list(starting_square_location)[1] + 1] = None
                    if list(destination_square_location)[0] == 0:
                        self._game_board[destination_square_location[0]][destination_square_location[1]] = 'Black_king'
                        self._players.get(player_name).set_king_count()
                        return
                    else:
                        self._game_board[list(destination_square_location)[0]][list(destination_square_location)[1]] = 'Black'
                        return
            except:
                pass

            # Jump piece to the left
        if y_direction == 'left':
            try:
                if self.get_checkers_details(possible_moves[0]) == 'White' \
                        or self.get_checkers_details(possible_moves[0]) == 'White_king' \
                        or self.get_checkers_details(possible_moves[0]) == 'Triple_White_king' \
                        and destination_value is None:
                    self._players.get(player_name).set_captured_pieces()
                    self._game_board[list(starting_square_location)[0]][list(starting_square_location)[1]] = None
                    self._game_board[list(starting_square_location)[0] - 1][list(starting_square_location)[1] - 1] = None
                    if list(destination_square_location)[0] == 0:
                        self._game_board[destination_square_location[0]][destination_square_location[1]] = 'Black_king'
                        self._players.get(player_name).set_king_count()
                        return
                    else:
                        self._game_board[list(destination_square_location)[0]][list(destination_square_location)[1]] = 'Black'
                        return
            except:
                pass

        # No capture
        if destination_value is None:
            self._game_board[list(starting_square_location)[0]][list(starting_square_location)[1]] = None
            if list(destination_square_location)[0] == 0:
                self._game_board[destination_square_location[0]][destination_square_location[1]] = 'Black_king'
                self._players.get(player_name).set_king_count()
            else:
                self._game_board[list(destination_square_location)[0]][list(destination_square_location)[1]] = 'Black'

    def black_king_movements(self, player_name, starting_square_location, destination_square_location):
        '''Create a list of valid movement options, check to see what is in those spaces. If it's none, set the
        starting_Square to None and the destination to Black. if it's white, add a new possible move, change the white
        square to none, and move the black piece'''
        destination_value = self.get_checkers_details(destination_square_location)
        possible_moves = [[list(starting_square_location)[0] - 1,
                           list(starting_square_location)[1] + 1],
                          [list(starting_square_location)[0] - 1,
                           list(starting_square_location)[1] - 1],
                          [list(starting_square_location)[0] + 1,
                           list(starting_square_location)[1] + 1],
                          [list(starting_square_location)[0] + 1,
                           list(starting_square_location)[1] - 1]]

        if list(destination_square_location)[1] - list(starting_square_location)[1] > 0:
            y_direction = 'right'
        else:
            y_direction = 'left'

        if list(destination_square_location)[0] > list(starting_square_location)[0]:
            x_direction = 'down'
        else:
            x_direction = 'up'

        # Jump piece up and to the right
        if x_direction == 'up' and y_direction == 'right':
            try:
                if self.get_checkers_details(possible_moves[0]) == 'White' \
                        or self.get_checkers_details(possible_moves[0]) == 'White_king' \
                        or self.get_checkers_details(possible_moves[0]) == 'Triple_White_king' \
                        and destination_value is None:
                    self._players.get(player_name).set_captured_pieces()
                    self._game_board[list(starting_square_location)[0]][list(starting_square_location)[1]] = None
                    self._game_board[list(starting_square_location)[0] - 1][list(starting_square_location)[1] + 1] = None
                    self._game_board[list(destination_square_location)[0]][list(destination_square_location)[1]] = 'Black_king'
            except:
                pass

            # Jump piece up to the left
        if x_direction == 'up' and y_direction == 'left':
            try:
                if self.get_checkers_details(possible_moves[1]) == 'White' \
                        or self.get_checkers_details(possible_moves[1]) == 'White_king' \
                        or self.get_checkers_details(possible_moves[1]) == 'Triple_White_king' \
                        and destination_value is None:
                    self._players.get(player_name).set_captured_pieces()
                    self._game_board[list(starting_square_location)[0]][list(starting_square_location)[1]] = None
                    self._game_board[list(starting_square_location)[0] - 1][list(starting_square_location)[1] - 1] = None
                    self._game_board[list(destination_square_location)[0]][list(destination_square_location)[1]] = 'Black_king'
            except:
                pass

        # Jump piece down and to the right
        if x_direction == 'down' and y_direction == 'right':
            try:
                if self.get_checkers_details(possible_moves[2]) == 'White' \
                        or self.get_checkers_details(possible_moves[2]) == 'White_king' \
                        or self.get_checkers_details(possible_moves[2]) == 'Triple_White_king' \
                        and destination_value is None:
                    self._players.get(player_name).set_captured_pieces()
                    self._game_board[list(starting_square_location)[0]][list(starting_square_location)[1]] = None
                    self._game_board[list(starting_square_location)[0] + 1][list(starting_square_location)[1] + 1] = None
                    if list(destination_square_location)[0] == 7:
                        self._game_board[destination_square_location[0]][destination_square_location[1]] = 'Triple_Black_king'
                    else:
                        self._game_board[list(destination_square_location)[0]][
                            list(destination_square_location)[1]] = 'Black_king'
            except:
                pass

            # Jump piece down and to the left
        if x_direction == 'down' and y_direction == 'left':
            try:
                if self.get_checkers_details(possible_moves[3]) == 'White' \
                        or self.get_checkers_details(possible_moves[3]) == 'White_king' \
                        or self.get_checkers_details(possible_moves[3]) == 'Triple_White_king' \
                        and destination_value is None:
                    self._players.get(player_name).set_captured_pieces()
                    self._game_board[list(starting_square_location)[0]][list(starting_square_location)[1]] = None
                    self._game_board[list(starting_square_location)[0] + 1][list(starting_square_location)[1] - 1] = None
                    if list(destination_square_location)[0] == 7:
                        self._game_board[destination_square_location[0]][destination_square_location[1]] = 'Triple_Black_king'
                    else:
                        self._game_board[list(destination_square_location)[0]][
                            list(destination_square_location)[1]] = 'Black_king'
            except:
                pass

        # No jump
        if destination_value is None:
            self._game_board[list(starting_square_location)[0]][list(starting_square_location)[1]] = None
            if list(destination_square_location)[0] == 7:
                self._game_board[destination_square_location[0]][destination_square_location[1]] = 'Triple_Black_king'
            else:
                self._game_board[list(destination_square_location)[0]][list(destination_square_location)[1]] = 'Black_king'

    def white_king_movements(self, player_name, starting_square_location, destination_square_location):
        '''Create a list of valid movement options, check to see what is in those spaces. If it's none,
         set the starting_Square to None and the destination to White. if it's black, add a new possible move,
          change the black square to none, and move the white piece'''
        destination_value = self.get_checkers_details(destination_square_location)
        possible_moves = [[list(starting_square_location)[0] - 1,
                           list(starting_square_location)[1] + 1],
                          [list(starting_square_location)[0] - 1,
                           list(starting_square_location)[1] - 1],
                          [list(starting_square_location)[0] + 1,
                           list(starting_square_location)[1] + 1],
                          [list(starting_square_location)[0] + 1,
                           list(starting_square_location)[1] - 1]]

        if list(destination_square_location)[1] - list(starting_square_location)[1] > 0:
            y_direction = 'right'
        else:
            y_direction = 'left'

        if list(destination_square_location)[0] > list(starting_square_location)[0]:
            x_direction = 'down'
        else:
            x_direction = 'up'

        # Jump piece up and to the right
        if x_direction == 'up' and y_direction == 'right':
            try:
                if self.get_checkers_details(possible_moves[0]) == 'Black' \
                        or self.get_checkers_details(possible_moves[0]) == 'Black_king' \
                        or self.get_checkers_details(possible_moves[0]) == 'Triple_Black_king' \
                        and destination_value is None:
                    self._players.get(player_name).set_captured_pieces()
                    self._game_board[list(starting_square_location)[0]][list(starting_square_location)[1]] = None
                    self._game_board[list(starting_square_location)[0] - 1][list(starting_square_location)[1] + 1] = None
                    if list(destination_square_location)[0] == 0:
                        self._game_board[destination_square_location[0]][destination_square_location[1]] = 'Triple_White_king'
                    else:
                        self._game_board[list(destination_square_location)[0]][
                            list(destination_square_location)[1]] = 'White_king'
            except:
                pass

            # Jump piece up to the left
            if x_direction == "up" and y_direction == 'left':
                try:
                    if self.get_checkers_details(possible_moves[1]) == 'Black' \
                            or self.get_checkers_details(possible_moves[1]) == 'Black_king' \
                            or self.get_checkers_details(possible_moves[1]) == 'Triple_Black_king' \
                            and destination_value is None:
                        self._players.get(player_name).set_captured_pieces()
                        self._game_board[list(starting_square_location)[0]][list(starting_square_location)[1]] = None
                        self._game_board[list(starting_square_location)[0] - 1][list(starting_square_location)[1] - 1] = None
                        if list(destination_square_location)[0] == 0:
                            self._game_board[destination_square_location[0]][destination_square_location[1]] = 'Triple_White_king'
                        else:
                            self._game_board[list(destination_square_location)[0]][
                                list(destination_square_location)[1]] = 'White_king'
                except:
                    pass

        # Jump piece down and to the right
        if x_direction == 'down' and y_direction == 'right':
            try:
                if self.get_checkers_details(possible_moves[2]) == 'Black' \
                        or self.get_checkers_details(possible_moves[2]) == 'Black_king' \
                        or self.get_checkers_details(possible_moves[2]) == 'Triple_Black_king' \
                        and destination_value is None:
                    self._players.get(player_name).set_captured_pieces()
                    self._game_board[list(starting_square_location)[0]][list(starting_square_location)[1]] = None
                    self._game_board[list(starting_square_location)[0] + 1][list(starting_square_location)[1] + 1] = None
                    self._game_board[list(destination_square_location)[0]][list(destination_square_location)[1]] = 'White_king'
            except:
                pass

            # Jump piece down and to the left
        if x_direction == 'down' and y_direction == 'left':
            try:
                if self.get_checkers_details(possible_moves[3]) == 'Black' \
                        or self.get_checkers_details(possible_moves[3]) == 'Black_king' \
                        or self.get_checkers_details(possible_moves[3]) == 'Triple_Black_king' \
                        and destination_value is None:
                    self._players.get(player_name).set_captured_pieces()
                    self._game_board[list(starting_square_location)[0]][list(starting_square_location)[1]] = None
                    self._game_board[list(starting_square_location)[0] + 1][list(starting_square_location)[1] - 1] = None
                    self._game_board[list(destination_square_location)[0]][list(destination_square_location)[1]] = 'White_king'
            except:
                pass

        # No jump
        if destination_value is None:
            self._game_board[list(starting_square_location)[0]][list(starting_square_location)[1]] = None
            if list(destination_square_location)[0] == 0:
                self._game_board[destination_square_location[0]][destination_square_location[1]] = 'Triple_White_king'
                self._players.get(player_name).set_triple_king_count()
                return
            else:
                self._game_board[list(destination_square_location)[0]][
                    list(destination_square_location)[1]] = 'White_king'

    def white_piece_movements(self, player_name, starting_square_location, destination_square_location):
        '''Create a list of valid movement options, check to see what is in those spaces. If it's none, set the
         starting_Square to None and the destination to White. if it's white, add a new possible move, change the black
        square to none, and move the white piece'''
        destination_value = self.get_checkers_details(destination_square_location)
        if destination_value == 'Black':
            raise InvalidSquare
        possible_moves = [[list(starting_square_location)[0] + 1,
                           list(starting_square_location)[1] + 1],
                          [list(starting_square_location)[0] + 1,
                           list(starting_square_location)[1] - 1]]

        if list(destination_square_location)[1] - list(starting_square_location)[1] > 0:
            y_direction = 'right'
        else:
            y_direction = 'left'


        # Jump piece to the right
        if y_direction == 'right':
            try:
                if self.get_checkers_details(possible_moves[0]) == 'Black' \
                        or self.get_checkers_details(possible_moves[0]) == 'Black_king' \
                        or self.get_checkers_details(possible_moves[0]) == 'Triple_Black_king' \
                        and destination_value is None:
                    self._players.get(player_name).set_captured_pieces()
                    self._game_board[list(starting_square_location)[0]][list(starting_square_location)[1]] = None
                    self._game_board[list(starting_square_location)[0] + 1][list(starting_square_location)[1] + 1] = None
                    if list(destination_square_location)[0] == 7:
                        self._players.get(player_name).set_king_count()
                        self._game_board[destination_square_location[0]][destination_square_location[1]] = 'White_king'
                        return
                    else:
                        self._game_board[list(destination_square_location)[0]][list(destination_square_location)[1]] = 'White'
                        return
            except:
                pass

            # Jump piece to the left
        if y_direction == 'left':
            try:
                if self.get_checkers_details(possible_moves[1]) == 'Black' \
                        or self.get_checkers_details(possible_moves[1]) == 'Black_king' \
                        or self.get_checkers_details(possible_moves[1]) == 'Triple_Black_king' \
                        and destination_value is None:
                    self._players.get(player_name).set_captured_pieces()
                    self._game_board[list(starting_square_location)[0]][list(starting_square_location)[1]] = None
                    self._game_board[list(starting_square_location)[0] + 1][list(starting_square_location)[1] - 1] = None
                    if list(destination_square_location)[0] == 7:
                        self._players.get(player_name).set_king_count()
                        self._game_board[destination_square_location[0]][destination_square_location[1]] = 'White_king'
                        return
                    else:
                        self._game_board[list(destination_square_location)[0]][list(destination_square_location)[1]] = 'White'
                        return
            except:
                pass

        if destination_value is None:
            self._game_board[list(starting_square_location)[0]][list(starting_square_location)[1]] = None
            if list(destination_square_location)[0] == 7:
                self._game_board[list(destination_square_location)[0]][list(destination_square_location)[1]] = 'White_king'
                self._players.get(player_name).set_king_count()
            else:
                self._game_board[list(destination_square_location)[0]][list(destination_square_location)[1]] = 'White'

    def get_checkers_details(self, square_location):
        '''Checks if the square is in range, then loops through the rows until it finds the correct row and column'''
        if self.check_if_valid_square(square_location) is False:
            raise InvalidSquare
        for i in self._game_board:
            if i == list(square_location)[0]:
                row = self._game_board.get(i)
                checker_location = row[list(square_location)[1]]
                if checker_location is None:
                    return None
                elif checker_location == "Black":
                    return "Black"
                elif checker_location == 'White':
                    return "White"
                elif checker_location == 'Black_king':
                    return "Black_king"
                elif checker_location == 'White_king':
                    return 'White_king'
                elif checker_location == 'Black_Triple_king':
                    return 'Black_Triple_king'
                elif checker_location == 'White_Triple_king':
                    return "White_Triple_king"

    def print_board(self):
        '''Prints each row of the board'''
        for i in self._game_board.values():
            print(i)

    def game_winner(self):
        '''if either player has captured all the enemy pieces return the name of the player,
        or "game has not ended" if the game isn't over yet'''
        if list(self._players.items())[0][1].get_captured_pieces_count() == 12:
            return list(self._players.items())[0][0]
        if list(self._players.items())[1][1].get_captured_pieces_count() == 12:
            return list(self._players.items())[1][0]
        return 'Game has not ended'

class Player():
    '''Player class which contains name, color, and details about pieces captured.'''

    def __init__(self, playername, color):
        self._player_name = playername
        self._color = color
        self._captured_pieces = 0
        self._king_pieces = 0
        self._triple_king_pieces = 0

    def get_color(self):
        '''Returns the players color'''
        return self._color

    def set_king_count(self):
        '''Increments the number of king_pieces by 1'''
        self._king_pieces += 1

    def get_king_count(self):
        '''Returns the number of kings the player has'''
        return self._king_pieces

    def set_triple_king_count(self):
        '''Increments the number of triple kings by 1'''
        self._triple_king_pieces += 1

    def get_triple_king_count(self):
        '''Returns the number of triple kings the player has'''
        return self._triple_king_pieces

    def get_captured_pieces_count(self):
        '''Returns how many pieces the player has captured'''
        return self._captured_pieces

    def set_captured_pieces(self):
        '''Increment captured pieces by 1'''
        self._captured_pieces += 1
