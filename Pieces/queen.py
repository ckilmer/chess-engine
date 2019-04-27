from Pieces.piece import Pieces
from Pieces.bishop import Bishop
from Pieces.rook import Rook
class Queen(Rook, Bishop):
    kind = Pieces.QUEEN

    def possibleMoves(self):
        moves = []
        moves += Rook.possibleMoves(self)
        moves += Bishop.possibleMoves(self)
        return moves