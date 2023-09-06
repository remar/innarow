class Board:
    def __init__(self, moves):
        self.board = [[None for i in range(15)] for j in range(15)]
        current = "x"
        for move in moves:
            self.set(move[0], move[1], current)
            current = "o" if current == "x" else "x"

    def get(self, x, y):
        if x >= 15 or y >= 15:
            return None
        return self.board[x][y]

    def set(self, x, y, symbol):
        self.board[x][y] = symbol

    def get_winner(self):
        for y in range(15):
            for x in range(15):
                offsets_lists = [
                    [[1, 0], [2, 0], [3, 0], [4, 0]],
                    [[0, 1], [0, 2], [0, 3], [0, 4]],
                    [[1, 1], [2, 2], [3, 3], [4, 4]]
                ]
                for offsets in offsets_lists:
                    winner = self.get_winner_given_offsets(x, y, offsets)
                    if winner:
                        return winner
        return None

    def get_winner_given_offsets(self, x, y, offsets):
        symbol = self.get(x, y)
        for offset in offsets:
            if self.get(x + offset[0], y + offset[1]) != symbol:
                return None
        return symbol
