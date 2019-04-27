from game import Game

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