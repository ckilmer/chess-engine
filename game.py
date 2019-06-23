from Pieces.piece import Piece, Pieces
from board import Board
from player import Player

class Game(object):
    def __init__(self):
        self.board = Board()
        self.players = (Player('White'), Player('Black'))
        self.moves = 0
        self.board.setup(self.players)
        for player in self.players:
            for row in self.board.squares:
                for square in row:
                    if square is not None and square.player is player:
                        player.pieces.append(square)
                        if square.kind == Pieces.KING:
                            player.king = square

    def currentplayer(self):
        '''
        Returns player object that needs to move
        '''
        return self.players[self.moves % 2]

    def otherplayer(self):
        '''
        Returns the Player object that is not moving
        '''
        return self.players[(self.moves+1) % 2]

    def isLegalmove(self, startPostion, endPosition):
        '''
        Checks if resulting move puts current player's king in check,
        if so rolls back the move
        '''
        isLegal = False
        capture = self.board.move(self.currentplayer(), self.otherplayer(), startPostion, endPosition)
        if capture is not None:
            #index 1 of a move is the end position
            attackedSquares = [move[1] for move in self.otherplayer().allMoves()]
            if self.currentplayer().king.position not in attackedSquares:
                isLegal = True
            self.board.rollbackLastMove(capture)
        return isLegal

    
    def getLegalMoves(self):
        '''
        Returns a list of the current player's legal moves
        '''
        legalMoves = []
        for move in self.currentplayer().allMoves():
            if self.isLegalmove(*move):
                legalMoves.append(move)
        return legalMoves

    def isOver(self):
        '''
        Returns boolean whether self.getLegalMoves is empty
        '''
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
            print(f'{move} is not legal')
            return False