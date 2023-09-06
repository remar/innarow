import json
import pytest
from Game import Game, PlayersMissingError, NotPlayersTurnError, IllegalMoveError
import itertools

def test_Game_WithoutConstructorArguments_CreatesEmptyGame():
    game = Game()
    assert game.player1 == None
    assert game.player2 == None
    assert game.moves == []

def test_Game_WithPlayerArguments_AssignsPlayers():
    game = Game("p1", "p2")
    assert game.player1 == "p1"
    assert game.player2 == "p2"

def test_Game_WithMoveArguments_AssignsMoves():
    game = Game(moves = [[1,1]])
    assert [1,1] in game.moves

def test_Move_WithNoPlayersAssigned_RaisesPlayersMissingError():
    game = Game()
    with pytest.raises(PlayersMissingError):
        game.move("player1", 8, 8)

def test_Move_LegalFirstMove_InsertsMove():
    game = Game("p1", "p2")
    game.move("p1", 8, 8)
    assert [8, 8] in game.moves

def test_Move_NotPlayersTurn_RaisesNotPlayersTurnError():
    game = Game("p1", "p2")
    with pytest.raises(NotPlayersTurnError):
        game.move("p2", 7, 7)

@pytest.mark.parametrize("x,y", [(-1, 7), (7, -1), (15, 7), (7, 15)])
def test_Move_OutsideField_RaisesIllegalMoveError(x, y):
    game = Game("p1", "p2")
    with pytest.raises(IllegalMoveError):
        game.move("p1", x, y)

def test_Move_PositionAlreadyTaken_RaisesIllegalMoveError():
    game = Game("p1", "p2", [[7, 7]])
    with pytest.raises(IllegalMoveError):
        game.move("p2", 7, 7)

def test_ToJson_WithValidContents_ReturnsJson():
    game = Game("p1", "p2", [[1, 1], [2, 2]])
    game_object = json.loads(game.to_json())
    assert game_object["player1"] == "p1"
    assert game_object["player2"] == "p2"
    assert game_object["moves"] == [[1,1],[2,2]]

def test_GetWinner_WithNoWinner_ReturnsNone():
    game = Game("p1", "p2")
    assert game.get_winner() == None

def test_GetWinner_FirstPlayerWinsHorizontally_ReturnsX():
    board = """
x x x x x . . . . . . . . . .
o o o o . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
"""
    game = make_game(board)
    assert game.get_winner() == "x"

def test_GetWinner_FirstPlayerWinsVertically_ReturnsX():
    board = """
x o . . . . . . . . . . . . .
x o . . . . . . . . . . . . .
x o . . . . . . . . . . . . .
x o . . . . . . . . . . . . .
x . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
"""
    game = make_game(board)
    assert game.get_winner() == "x"

def test_GetWinner_FirstPlayerWinsDiagonally_ReturnsX():
    board = """
x o . . . . . . . . . . . . .
. x o . . . . . . . . . . . .
. . x o . . . . . . . . . . .
. . . x o . . . . . . . . . .
. . . . x . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
"""
    game = make_game(board)
    assert game.get_winner() == "x"

def test_extract_moves():
    board = """
x o . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . x x . . . . . .
. . . . . . . o . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
"""
    assert extract_moves(board) == {"x":[[0, 0], [7, 7], [8, 7]],
                                    "o":[[1, 0], [7, 8]]}

def test_join_moves():
    board = """
x x o . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
"""
    assert join_moves(extract_moves(board)) == [[0,0],[2,0],[1,0]]

def test_make_game():
    board = """
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . o x . . . . . .
. . . . . . . x o . . . . . .
. . . . . . . x . o . . . . .
. . . . . . . . . . x . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
. . . . . . . . . . . . . . .
"""
    game = make_game(board)
    assert game.player1 == "p1"
    assert game.player2 == "p2"
    assert game.moves == [[8, 5], [7, 5], [7, 6], [8, 6], [7, 7], [9, 7], [10, 8]]

def make_game(board):
    return Game("p1", "p2", join_moves(extract_moves(board)))

def join_moves(moves):
    result = moves["x"] + moves["o"]
    result[::2] = moves["x"]
    result[1::2] = moves["o"]
    return result

def extract_moves(board):
    xs = []
    os = []
    x = 0
    y = 0
    lines = board.split("\n")[1:-1]
    assert len(lines) == 15
    for line in lines:
        moves = line.split(" ")
        assert len(moves) == 15
        for move in moves:
            assert move in [".", "x", "o"]
            if move == "x":
                xs.append([x, y])
            elif move == "o":
                os.append([x, y])
            x += 1
        y += 1
        x = 0
    return {"x":xs, "o":os}
