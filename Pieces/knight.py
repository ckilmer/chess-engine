from Pieces.piece import Piece, Pieces

class Knight(Piece):
    kind = Pieces.KNIGHT

    def possibleMoves(self):
        moves = []
        rank = self.position[1]
        file = self.position[0]
        for j in (-1,1):
            for k in (-1,1):
                moves.append((file+1*k, rank+2*j))
                moves.append((file+2*k, rank+1*j))
        moves = self.movesOnBoard(moves)
        moves = [move for move in moves if self.board[move] is None or self.board[move].player != self.player]
        moves = [(self.position, move) for move in moves]
        return moves