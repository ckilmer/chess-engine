from enum import Enum

Pieces = Enum('Piece', 'PAWN KNIGHT BISHOP ROOK QUEEN KING')

class Piece(object):
    kind = None
    def __init__(self, board, player, position=(0,0)):
        self.board = board
        self.player = player
        self.moves = 0
        self.position = position
    
    def __repr__(self):
        return '{} {} at position {}'.format(self.player.color[0], self.kind.name, self.position) 

    def __str__(self):
        if self.kind == Pieces.KNIGHT:
            pieceString = self.kind.name[1]
        else:
            pieceString = self.kind.name[0]
        if self.player.color == 'White':
            return pieceString.upper()
        else:
            return pieceString.lower()

    def possibleMoves(self):
        pass 
    
    def movesOnBoard(self, moves):
        return [v for v in moves if v[0]>=0 and v[0] <= 7 and v[1]>=0 and v[1] <= 7]