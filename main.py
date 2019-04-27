from Pieces.piece import Piece, Pieces
from board import Board
from player import Player

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


game = Game()
print(game.board)

