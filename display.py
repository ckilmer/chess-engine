import tkinter
from Pieces.piece import Pieces

class Display():
    def __init__(self, root, game):
        self.root = root
        self.game = game
        self.square_size = 25*3
        self.canvas_height = 1000
        self.canvas_width = 1000
        self.margin_left = int((self.canvas_width - 8*self.square_size)/2)
        self.margin_top = int((self.canvas_height - 8*self.square_size)/2)

        self.current_piece = None
        self.startcoord = None
        self.currentcoord = None
        self.canvas = tkinter.Canvas(master=self.root, bg="#969696", height=self.canvas_height, width=self.canvas_width)
        self.canvas.pack(fill='both')
        self.pieceimg = {
            ('White', Pieces.KING):tkinter.PhotoImage(file='images/white_king.png').subsample(4,4),
            ('White', Pieces.QUEEN):tkinter.PhotoImage(file='images/white_queen.png').subsample(4,4),
            ('White', Pieces.BISHOP):tkinter.PhotoImage(file='images/white_bishop.png').subsample(4,4),
            ('White', Pieces.KNIGHT):tkinter.PhotoImage(file='images/white_knight.png').subsample(4,4),
            ('White', Pieces.ROOK):tkinter.PhotoImage(file='images/white_rook.png').subsample(4,4),
            ('White', Pieces.PAWN):tkinter.PhotoImage(file='images/white_pawn.png').subsample(4,4),
            ('Black', Pieces.KING):tkinter.PhotoImage(file='images/black_king.png').subsample(4,4),
            ('Black', Pieces.QUEEN):tkinter.PhotoImage(file='images/black_queen.png').subsample(4,4),
            ('Black', Pieces.BISHOP):tkinter.PhotoImage(file='images/black_bishop.png').subsample(4,4),
            ('Black', Pieces.KNIGHT):tkinter.PhotoImage(file='images/black_knight.png').subsample(4,4),
            ('Black', Pieces.ROOK):tkinter.PhotoImage(file='images/black_rook.png').subsample(4,4),
            ('Black', Pieces.PAWN):tkinter.PhotoImage(file='images/black_pawn.png').subsample(4,4),
        }
        self.img_size = self.pieceimg[('White', Pieces.KING)].width()
        print(self.img_size)
        self.redraw()
    def board_to_canvas_coords(self, x, y):
        return self.margin_left + (self.square_size+1)/2 + x*self.square_size, self.margin_top + (self.square_size+1)/2 + (7-y)*self.square_size

    def canvas_to_board_coords(self, x, y):
        return round((x - self.margin_left - (self.square_size+1)/2)/self.square_size), round(7 - (y - self.margin_left - (self.square_size+1)/2)/self.square_size)

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
        self.startcoord = self.canvas_to_board_coords(x, y)[1], self.canvas_to_board_coords(x, y)[0]
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
            print(self.startcoord, (j, i))
            #dx = self.board_to_canvas_coords(i, j)[0] - self.currentcoord[0]
            #dy = self.board_to_canvas_coords(i, j)[1] - self.currentcoord[1]
            #self.canvas.move(self.current_piece, dx, dy)
            self.game.move(self.startcoord, (j, i))
            self.redraw()
        self.current_piece = None
        self.startcoord = None
        self.currentcoord = None

    def redraw(self):
        self.draw_blank_board()
        for i in range(8):
            for j in range(8):
                piece = self.game.board[i,j]
                if piece is not None:
                    img = self.pieceimg[(piece.player.color, piece.kind)]
                    if piece.player == self.game.currentplayer():
                        tags = 'piece'
                    else:
                        tags = None
                    self.draw_piece(img, j, i, tags)
        self.canvas.tag_bind('piece', '<ButtonPress-1>', self.select_piece)
        self.canvas.tag_bind('piece', '<B1-Motion>', self.move_piece)
        self.canvas.tag_bind('piece', '<ButtonRelease-1>', self.snap_piece)