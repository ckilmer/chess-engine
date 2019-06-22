from Pieces.piece import Piece, Pieces


class Pawn(Piece):
    kind = Pieces.PAWN

    def __init__(self, *args):
        super().__init__(*args)
        self.canEnPassant = False

    def possibleMoves(self):
        moves = []
        rank = self.position[1]
        file = self.position[0]
        direction = 2*(self.player.color=='White') - 1
        checkposition = (file, rank + 1*direction)
        if self.movesOnBoard([checkposition]) and self.board[checkposition] is None:
            moves.append((checkposition))
            checkposition = (file, rank + 2*direction)
            if self.movesOnBoard([checkposition]) and self.board[checkposition] is None and self.moves==0:
                moves.append((checkposition))
        checkposition = (file + 1, rank + 1*direction)
        if self.movesOnBoard([checkposition]) and self.board[checkposition] is not None and self.board[checkposition].player != self.player:
            moves.append((checkposition))
        checkposition = (file - 1, rank + 1*direction)
        if self.movesOnBoard([checkposition]) and self.board[checkposition] is not None and self.board[checkposition].player != self.player:
            moves.append(checkposition)
        if len(self.board.priorMoves) > 0:
            lastmove = self.board.priorMoves[len(self.board.priorMoves) - 1]
            lastmoveStartPosition = lastmove[2]
            lastmoveEndPosition = lastmove[3]
            if (abs(lastmoveStartPosition[0] - file) == 1
            and abs(lastmoveEndPosition[1] - lastmoveStartPosition[1]) == 2
            and self.board[lastmoveEndPosition].kind == Pieces.PAWN
            and rank == (3.5 + 0.5*direction)):
                moves.append((lastmoveStartPosition[0], rank+1))
        moves = self.movesOnBoard(moves)
        moves = [(self.position, move) for move in moves]
        return moves
