from Pieces.piece import Piece, Pieces

class King(Piece):
    kind = Pieces.KING

    def possibleMoves(self):
        moves = []
        rank = self.position[0]
        file = self.position[1]
        if self.player.canCastleKingSide:
            pass
        if self.player.canCastleQueenSide:
            pass
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (rank+i, file+j) != self.position:
                    moves.append((rank+i,file+j))
        moves = self.movesOnBoard(moves)
        moves = [move for move in moves if self.board[move] is None or self.board[move].player != self.player]
        return moves