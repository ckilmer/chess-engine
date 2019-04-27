from Pieces.piece import Piece, Pieces


class Pawn(Piece):
    kind = Pieces.PAWN

    def __init__(self, *args):
        super().__init__(*args)
        self.canEnPassant = False

    def possibleMoves(self):
        moves = []
        rank = self.position[0]
        file = self.position[1]
        direction = 2*(self.player.color=='White') - 1
        checkposition = (rank + 1*direction, file)
        if self.movesOnBoard([checkposition]) and self.board[checkposition] is None:
            moves.append((checkposition))
            checkposition = (rank + 2*direction, file)
            if self.movesOnBoard([checkposition]) and self.board[checkposition] is None and self.moves==0:
                moves.append((checkposition))
        checkposition = (rank + 1*direction, file + 1)
        if self.movesOnBoard([checkposition]) and self.board[checkposition] is not None and self.board[checkposition].player != self.player:
            moves.append((checkposition))
        checkposition = (rank + 1*direction, file - 1)
        if self.movesOnBoard([checkposition]) and self.board[checkposition] is not None and self.board[checkposition].player != self.player:
            moves.append(checkposition)
        lastmoveStartPosition = self.board.lastmove[2]
        lastmoveEndPosition = self.board.lastmove[3]
        if (abs(lastmoveStartPosition[1] - file) == 1
        and abs(lastmoveEndPosition[0] - lastmoveStartPosition[0]) == 2
        and self.board[lastmoveEndPosition].kind == Pieces.PAWN
        and rank == (3.5 + 0.5*direction)):
            moves.append(rank+1, lastmoveStartPosition[1])
        return self.movesOnBoard(moves)