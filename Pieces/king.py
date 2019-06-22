from Pieces.piece import Piece, Pieces

class King(Piece):
    kind = Pieces.KING

    def possibleMoves(self):
        moves = []
        rank = self.position[1]
        file = self.position[0]
        for i in range(-1, 2):
            for j in range(-1, 2):
                possibleMove = (file+j, rank+i)
                if possibleMove != self.position:
                    moves.append(possibleMove)
        moves = self.movesOnBoard(moves)
        moves = [move for move in moves if self.board[move] is None or self.board[move].player != self.player]
        moves = [(self.position, move) for move in moves]
        return moves