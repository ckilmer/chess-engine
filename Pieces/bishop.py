from Pieces.piece import Piece, Pieces

class Bishop(Piece):
    kind = Pieces.BISHOP

    def possibleMoves(self):
        moves = []
        rank = self.position[1]
        file = self.position[0]
        for i in range(1, min(8-file, 8-rank)):
            square = (file+i, rank+i)
            moves.append(square)
            if self.board[square] is not None:
                break
        for i in range(1, min(1+file, 1+rank)):
            square = (file-i, rank-i)
            moves.append(square)
            if self.board[square] is not None:
                break
        for i in range(1, min(8-file, 1+rank)):
            square = (file+i, rank-i)
            moves.append(square)
            if self.board[square] is not None:
                break
        for i in range(1, min(1+file, 8-rank)):
            square = (file-i, rank+i)
            moves.append(square)
            if self.board[square] is not None:
                break
        moves = [move for move in moves if self.board[move] is None or self.board[move].player != self.player]
        moves = [(self.position, move) for move in moves]
        return moves