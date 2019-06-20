import tkinter
from game import Game
from display import Display

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


root = tkinter.Tk()
display = Display(root, game)
root.mainloop()


