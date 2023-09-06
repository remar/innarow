import json
from Board import Board

class Game:
    def __init__(self, player1 = None, player2 = None, moves = None) -> None:
        self.player1 = player1
        self.player2 = player2
        self.moves = moves or []

    def move(self, player, x, y):
        self.__verify_move(player, x, y)
        self.moves.append([x, y])

    def get_winner(self):
        return Board(self.moves).get_winner()

    def to_json(self):
        return json.dumps({"player1":self.player1, "player2":self.player2, "moves":self.moves})

    def __verify_move(self, player, x, y):
        if not self.__players_are_assigned():
            raise PlayersMissingError
        if not self.__is_players_turn(player):
            raise NotPlayersTurnError
        if not self.__is_legal_move(x, y):
            raise IllegalMoveError

    def __players_are_assigned(self):
        return self.player1 and self.player2

    def __is_players_turn(self, player):
        return self.__current_turn() == player

    def __current_turn(self):
        return self.player1 if len(self.moves) % 2 == 0 else self.player2

    def __is_legal_move(self, x, y):
        return self.__is_inside_board(x, y) and self.__is_free_space(x, y)

    def __is_inside_board(self, x, y):
        return x >= 0 and x < 15 and y >= 0 and y < 15

    def __is_free_space(self, x, y):
        return [x, y] not in self.moves

class PlayersMissingError(Exception): pass
class NotPlayersTurnError(Exception): pass
class IllegalMoveError(Exception): pass
