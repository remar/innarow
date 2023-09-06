from Board import Board

def test_Board_WithEmptyMoveList_HasEmptyBoard():
    board = Board([])
    for y in range(15):
        for x in range(15):
            assert board.get(x, y) == None

def test_Board_WithOneMoveForX_HasBoardWithXInTheMiddle():
    board = Board([[7,7]])
    assert board.get(7, 7) == "x"

def test_Board_WithOneMoveForXAndOneForO_HasBoardWithXAndO():
    board = Board([[7,7],[7,8]])
    assert board.get(7, 7) == "x"
    assert board.get(7, 8) == "o"
