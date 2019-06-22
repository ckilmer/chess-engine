from Pieces.piece import Piece, Pieces

class Rook(Piece):
    kind = Pieces.ROOK

    def possibleMoves(self):
        moves = []
        rank = self.position[1]
        file = self.position[0]
        for i in range(1,8-file):
            square = (file+i, rank)
            moves.append(square)
            if self.board[square] is not None:
                break
        for i in range(1,1+file):
            square = (file-i, rank)
            moves.append(square)
            if self.board[square] is not None:
                break
        for i in range(1,8-rank):
            square = (file, rank+i)
            moves.append(square)
            if self.board[square] is not None:
                break
        for i in range(1,1+rank):
            square = (file, rank-i)
            moves.append(square)
            if self.board[square] is not None:
                break
        moves = [move for move in moves if self.board[move] is None or self.board[move].player != self.player]
        moves = [(self.position, move) for move in moves]
        return moves