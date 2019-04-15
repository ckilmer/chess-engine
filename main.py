from enum import Enum

Pieces = Enum('Piece', 'PAWN KNIGHT BISHOP ROOK QUEEN KING')

class Board(object):
    def __init__(self):
        self.squares = [[None]*8,
                        [None]*8,
                        [None]*8,
                        [None]*8,
                        [None]*8,
                        [None]*8,
                        [None]*8,
                        [None]*8]
        self.lastmove = None
    
    def __str__(self):
        separator = ' | '
        boardStr = ''
        rank = 7
        for row in reversed(self.squares):
            rowStr = str(rank) + separator
            for square in row:
                if square is None:
                    rowStr += '_'
                else:
                    rowStr += str(square)
                rowStr += separator
            boardStr += rowStr + '\n'
            rank -= 1
        files = list('01234567')
        filesSeparator = '   '
        boardStr += ' '+ filesSeparator \
                    + filesSeparator.join(files) \
                    + filesSeparator
        return boardStr

    def __getitem__(self, position):
        return self.squares[position[0]][position[1]]

    def __setitem__(self, position, value):
        self.squares[position[0]][position[1]] = value

    def setup(self, players):
        for rank, player in [(1,0), (6,1)]:
            for i in range(8):
                self[rank,i] = Pawn(self, players[player], (rank,i))
        for rank, player in [(0,0), (7,1)]:
            self[rank,0] = Rook(self, players[player], (rank,0))
            self[rank,1] = Knight(self, players[player], (rank,1))
            self[rank,2] = Bishop(self, players[player], (rank,2))
            self[rank,3] = Queen(self, players[player], (rank,3))
            self[rank,4] = King(self, players[player], (rank,4))
            self[rank,5] = Bishop(self, players[player], (rank,5))
            self[rank,6] = Knight(self, players[player], (rank,6))
            self[rank,7] = Rook(self, players[player], (rank,7))
        # need to add other pieces

    def confirmMove(self, player, otherplayer, startPosition, endPosition):
        capture = False
        self.lastmove = (player, otherplayer, startPosition, endPosition)
        if self[endPosition] is not None:
            capture = True
            player.captures.append(self[endPosition])
            otherplayer.pieces.remove(self[endPosition])
        self[endPosition] = self[startPosition]
        self[endPosition].position = endPosition
        self[endPosition].moves += 1
        self[startPosition] = None
        return capture

    def rollbackLastMove(self, capture):
        player = self.lastmove[0]
        otherplayer = self.lastmove[1]
        startposition = self.lastmove[2]
        endposition = self.lastmove[3]
        self[startposition] = self[endposition]
        self[startposition].moves -= 1
        if capture:
            self[endposition] = player.captures.pop()
            otherplayer.pieces.append(self[endposition])
        else:
            self[endposition] = None


    def move(self, player, otherplayer, startPosition, endPosition):
        piece = self[startPosition]
        if piece is None:
            print('No piece')
            return
        if piece.player is not player:
            print('{} does not belong to {}'.format(repr(piece), player.color))
            return
        if endPosition not in self[startPosition].possibleMoves():
            print('{} cannot move to {}'.format(repr(piece), endPosition))
            return
        capture = self.confirmMove(player, otherplayer, startPosition, endPosition)
        return capture

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

class Game(object):
    def __init__(self):
        self.board = Board()
        self.players = (Player('White'), Player('Black'))
        self.moves = 0
        self.board.setup(self.players)
        for i in range(2):
            for row in self.board.squares:
                for square in row:
                    if square is not None and square.player is self.players[i]:
                        self.players[i].pieces.append(square)
                        if square.kind == Pieces.KING:
                            self.players[i].king = square

    def move(self, startPostion, endPosition):
        player = self.players[self.moves % 2]
        otherplayer = self.players[(self.moves+1) % 2]

        capture = self.board.move(player, otherplayer, startPostion, endPosition)
        if capture is not None:
            self.moves += 1
            if player.king.position in otherplayer.allMoves():
                print('cannot move there, king is in check')
                self.board.rollbackLastMove(capture)
                self.moves -= 1


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
        and self.board[lastmoveEndPosition].kind = Pieces.PAWN
        and rank == (3.5 + 0.5*direction):
            moves.append(rank+1, lastmoveStartPosition[1])


        return self.movesOnBoard(moves)

class Knight(Piece):
    kind = Pieces.KNIGHT

    def possibleMoves(self):
        moves = []
        rank = self.position[0]
        file = self.position[1]
        for j in (-1,1):
            for k in (-1,1):
                moves.append((rank+2*j, file+1*k))
                moves.append((rank+1*j, file+2*k))
        moves = self.movesOnBoard(moves)
        moves = [move for move in moves if self.board[move] is None or self.board[move].player != self.player]
        return moves

class Rook(Piece):
    kind = Pieces.ROOK

    def possibleMoves(self):
        moves = []
        rank = self.position[0]
        file = self.position[1]
        for i in range(1,8-file):
            square = (rank, file+i)
            moves.append(square)
            if self.board[square] is not None:
                break
        for i in range(1,1+file):
            square = (rank, file-i)
            moves.append(square)
            if self.board[square] is not None:
                break
        for i in range(1,8-rank):
            square = (rank+i, file)
            moves.append(square)
            if self.board[square] is not None:
                break
        for i in range(1,1+rank):
            square = (rank-i, file)
            moves.append(square)
            if self.board[square] is not None:
                break
        moves = [move for move in moves if self.board[move] is None or self.board[move].player != self.player]
        return moves

class Bishop(Piece):
    kind = Pieces.BISHOP

    def possibleMoves(self):
        moves = []
        rank = self.position[0]
        file = self.position[1]
        for i in range(1, min(8-file, 8-rank)):
            square = (rank+i, file+i)
            moves.append(square)
            if self.board[square] is not None:
                break
        for i in range(1, min(1+file, 1+rank)):
            square = (rank-i, file-i)
            moves.append(square)
            if self.board[square] is not None:
                break
        for i in range(1, min(8-file, 1+rank)):
            square = (rank-i, file+i)
            moves.append(square)
            if self.board[square] is not None:
                break
        for i in range(1, min(1+file, 8-rank)):
            square = (rank+i, file-i)
            moves.append(square)
            if self.board[square] is not None:
                break
        moves = [move for move in moves if self.board[move] is None or self.board[move].player != self.player]
        return moves

class Queen(Rook, Bishop):
    kind = Pieces.QUEEN

    def possibleMoves(self):
        moves = []
        moves += Rook.possibleMoves(self)
        moves += Bishop.possibleMoves(self)
        return moves

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

game = Game()
print(game.board)

