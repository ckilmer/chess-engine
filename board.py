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