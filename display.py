import tkinter
from Pieces.piece import Pieces

class Display():
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.square_size = 25*3
        self.canvas_height = 8*self.square_size + 50
        self.canvas_width = 8*self.square_size + 50
        self.margin_left = int((self.canvas_width - 8*self.square_size)/2)
        self.margin_top = int((self.canvas_height - 8*self.square_size)/2)
        self.current_piece = None
        self.startcoord = None
        self.currentcoord = None
        self.canvas = tkinter.Canvas(master=self.root, bg="#969696", height=self.canvas_height, width=self.canvas_width)
        self.canvas.tag_bind('piece', '<ButtonPress-1>', self.select_piece)
        self.canvas.tag_bind('piece', '<B1-Motion>', self.move_piece)
        self.canvas.tag_bind('piece', '<ButtonRelease-1>', self.snap_piece)
        self.text = tkinter.Entry(root, justify='center', font=("Times", "50", "bold"))
        self.canvas.pack(fill='x')
        self.text.pack(fill='x')
        self.pieceimg = {}
        for color in ['White', 'Black']:
            for piece in Pieces:
                self.pieceimg[(color, piece)] = tkinter.PhotoImage(file='images/{}_{}.png'.format(color, piece.name)).subsample(4,4)
        self.img_size = self.pieceimg[('White', Pieces.KING)].width()
        print(self.img_size)
        self.redraw()




    def board_to_canvas_coords(self, x, y):
        return self.margin_left + (self.square_size+1)/2 + x*self.square_size, self.margin_top + (self.square_size+1)/2 + (7-y)*self.square_size

    def canvas_to_board_coords(self, x, y):
        return round((x - self.margin_left - (self.square_size+1)/2)/self.square_size), round(7 - (y - self.margin_left - (self.square_size+1)/2)/self.square_size)

    def draw_message(self):
        self.text.delete(0, tkinter.END)
        if not self.game.isOver():
            self.text.insert(tkinter.END, '{} to move'.format(self.game.currentplayer().color))
        else:
            self.text.insert(tkinter.END, '{} wins!'.format(self.game.otherplayer().color))

    def draw_blank_board(self):
        for i in range(8):
            for j in range(8):
                x, y = self.board_to_canvas_coords(i, j)
                coords = x-(self.square_size + 1)/2, y-(self.square_size + 1)/2, x+(self.square_size + 1)/2, y+(self.square_size + 1)/2
                self.canvas.create_rectangle(coords, fill=('#82ba78' if (i+j) % 2 == 0 else '#dddddd'), outline='black')

    def draw_piece(self, img, i, j, tags=None):
        coords = self.board_to_canvas_coords(i, j)
        self.canvas.create_image(coords, image=img, tags=tags)

    def select_piece(self, event):
        self.current_piece = self.canvas.find_closest(event.x, event.y, halo=self.square_size/3)
        x = self.canvas.bbox(self.current_piece)[0] + (self.square_size + 1)/2
        y = self.canvas.bbox(self.current_piece)[1] + (self.square_size + 1)/2
        self.startcoord = self.canvas_to_board_coords(x, y)
        self.currentcoord = x, y

    def move_piece(self, event):
        dx = event.x - self.currentcoord[0]
        dy = event.y - self.currentcoord[1]
        self.canvas.move(self.current_piece, dx, dy)
        self.currentcoord = event.x, event.y
    
    def snap_piece(self, event):
        x, y = tuple(self.canvas.bbox(self.current_piece)[0:2])
        i, j = self.canvas_to_board_coords(x + (self.img_size)/2, y + (self.img_size)/2)
        if i < 0 or i > 7 or j < 0 or j > 7:
            pass
        else:
            print(self.startcoord, (i, j))
            self.game.move(self.startcoord, (i, j))
        self.redraw()
        self.current_piece = None
        self.startcoord = None
        self.currentcoord = None

    def redraw(self):
        self.canvas.delete('all')
        self.draw_blank_board()
        self.draw_message()
        for i in range(8):
            for j in range(8):
                piece = self.game.board[i,j]
                if piece is not None:
                    img = self.pieceimg[(piece.player.color, piece.kind)]
                    if piece.player == self.game.currentplayer():
                        tags = 'piece' if not self.game.isOver() else None
                    else:
                        tags = None
                    self.draw_piece(img, i, j, tags)

import tkinter
dir(tkinter.Canvas.create_text)