import json
import pytest
from Game import Game, PlayersMissingError, NotPlayersTurnError

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

# move: outside field -> IllegalMoveError

# move: already taken position -> IllegalMoveError

def test_ToJson_WithValidContents_ReturnsJson():
    game = Game("p1", "p2", [[1, 1], [2, 2]])
    game_object = json.loads(game.to_json())
    assert game_object["player1"] == "p1"
    assert game_object["player2"] == "p2"
    assert game_object["moves"] == [[1,1],[2,2]]
