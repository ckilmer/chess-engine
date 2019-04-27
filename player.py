class Player(object):
    def __init__(self, color='White'):
        self.color = color
        self.pieces = []
        self.king = None
        self.captures = []
        self.canCastleKingSide = True
        self.canCastleQueenSide = True

    def allMoves(self):
        moves = []
        for piece in self.pieces:
            moves = moves + piece.possibleMoves()
        return moves