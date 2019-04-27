from Pieces.piece import Piece, Pieces
from board import Board
from player import Player

def parseStrToCoord(coord):
    filemapping = {}
    for i,letter in enumerate('ABCDEFGH'):
        filemapping[letter] = i
    file = coord[0].upper()
    try:
        file = filemapping[file]
        rank = int(coord[1]) - 1
        return rank, file
    except:
        print('not valid coordinate')


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

    def currentplayer(self):
        return self.players[self.moves % 2]

    def otherplayer(self):
        return self.players[(self.moves+1) % 2]

    def isLegalmove(self, startPostion, endPosition):
        isLegal = False
        capture = self.board.move(self.currentplayer(), self.otherplayer(), startPostion, endPosition)
        if capture is not None:
            #index 1 of a move is the end position
            if self.currentplayer().king.position not in [move[1] for move in self.otherplayer().allMoves()]:
                isLegal = True
            self.board.rollbackLastMove(capture)
        return isLegal

    
    def getLegalMoves(self):
        legalMoves = []
        for move in self.currentplayer().allMoves():
            if self.isLegalmove(*move):
                legalMoves.append(move)
        return legalMoves

    def isOver(self):
        ended = len(self.getLegalMoves()) == 0
        return ended
    def move(self, startPostion, endPosition):
        if startPostion is None and endPosition is None:
            return False
        move = (startPostion, endPosition)
        if move in self.getLegalMoves():
            print('{} moves {} to {}'.format(self.currentplayer().color, move[0], move[1]))
            self.board.move(self.currentplayer(), self.otherplayer(), *move)
            self.moves += 1
            return True
        else:
            print('Not a legal move, king is in check')
            return False

game = Game()
print(game.board)
game.move((1,5), (2,5))
game.move((6,4), (4,4))
game.move((1,6), (3,6))
print(game.board)
while(not game.isOver()):
    startcoord, endcoord = None, None
    while(not game.move(startcoord, endcoord)):
        startcoord = parseStrToCoord(input('{} choose a coordinate to move: '.format(game.currentplayer().color)))
        endcoord = parseStrToCoord(input('{} choose a coordinate to move to: '.format(game.currentplayer().color)))
    print(game.board)
print('{} is the winner!'.format(game.otherplayer().color))