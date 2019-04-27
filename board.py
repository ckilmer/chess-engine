from Pieces.pawn import Pawn
from Pieces.knight import Knight
from Pieces.bishop import Bishop
from Pieces.rook import Rook
from Pieces.queen import Queen
from Pieces.king import King

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
        self.priorMoves = []
        self.displayMode = True
    
    def __str__(self):
        separator = ' | '
        boardStr = ''
        if self.displayMode:
            files = list('ABCDEFGH')
            rank = 8
        else:
            rank = 7
            files = list('01234567')
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
        self.priorMoves.append((player, otherplayer, startPosition, endPosition))
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
        lastmove = self.priorMoves.pop()
        player = lastmove[0]
        otherplayer = lastmove[1]
        startposition = lastmove[2]
        endposition = lastmove[3]
        self[startposition] = self[endposition]
        self[startposition].moves -= 1
        self[startposition].position = startposition
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
        #index 1 of a move is the end position
        if endPosition not in [move[1] for move in piece.possibleMoves()]:
            print('{} cannot move to {}'.format(repr(piece), endPosition))
            return
        capture = self.confirmMove(player, otherplayer, startPosition, endPosition)
        return capture