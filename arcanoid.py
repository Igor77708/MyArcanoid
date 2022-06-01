import tkinter as tk
from random import randint
from math import hypot

BRICK_W = 40 # ширина кирпича 
BRICK_H = 10 # высота кирпича
BRICK_S = 5 # промежуток между кирпичами

WALL_X = 10 # количество кирпичей по x
WALL_Y = 4  # количество кирпичей по y
# вычисляем ширину игрового пространства (холста)
WIDTH = WALL_X * BRICK_W + BRICK_S * (WALL_X + 1) # промежутков на один больше чем кирпичей
HEIGHT = BRICK_H * WALL_Y * 10 # высота холста в N раза больше высоты кирпичей
CANVAS_COLOR = '#212f3c' # цвет холста

TABLE_H = 10 # высота ракетки

class Table: # рвкетка
    # конструктор
    def __init__(self,
                 table_x,
                 table_y,
                 table_w
                 ):
        self.table_x = table_x
        self.table_y = table_y
        self.table_w = table_w
        
        self.table_id = canvas.create_rectangle(table_x - table_w,
                                                table_y - TABLE_H,
                                                table_x + table_w,
                                                table_y + TABLE_H,
                                                fill = 'orange',
                                                width = 3,
                                                outline='yellow'
                                                )

    # методы класса
    def move(self, xnew, ynew):
        xold, yold = self.table_x, self.table_y
        dx = xnew - xold
        dy = ynew - yold
        canvas.move(self.table_id, dx, 0)
        self.table_x, self.table_y = xnew, ynew


class Ball: # летающий шарик 
    # конструктор
    def __init__(self):
        self.ball_x = 220
        self.ball_y = 220
        self.ball_r = 10
        self.dx, self.dy = -2, -10#randint(-10,10), randint(-10,-1)
        self.ball_id = canvas.create_oval(self.ball_x - self.ball_r,
                                          self.ball_y - self.ball_r,
                                          self.ball_x + self.ball_r,
                                          self.ball_y + self.ball_r,
                                          fill = 'light green',
                                          width = 0,
                                          outline='gold'
                                          )
        
    # методы класса
    def move(self):
        if self.ball_x + self.ball_r > WIDTH or self.ball_x - self.ball_r <= 0:
            self.dx = -self.dx
        if self.ball_y + self.ball_r > HEIGHT or self.ball_y - self.ball_r <= 0:
            self.dy = -self.dy
        self.ball_x += self.dx
        self.ball_y += self.dy
        canvas.move(self.ball_id, self.dx, self.dy)


class Wall: # стена из кирпичей
    # конструктор
    def __init__(self,
                 x,
                 y):
        self.br_x = x
        self.br_y = y
        c='#' + str("{0:X}".format(randint(50,255))) + \
                str("{0:X}".format(randint(50,255))) + \
                str("{0:X}".format(randint(50,255))) # цвет в формате '#12AB5F'
        self.brick_id = canvas.create_rectangle(self.br_x,
                                                self.br_y,
                                                self.br_x + BRICK_W,
                                                self.br_y + BRICK_H,
                                                fill = c,
                                                width = 3,
                                                outline = c#'gold'
                                                )

        
    # методы класса
    def move(self):
        pass

def canvas_left_click(event):
    x, y = event.x, event.y
    #    canvas.create_text(WIDTH/2, HEIGHT/2, text = "GAME OVER", font = "Ubuntu 36")
        
    
def canvas_mouse_motion(event):
    x, y = event.x, event.y
    table.move(x,y)
    

def tick():
    ball.move()
    root.after(50, tick)


def main():
    global root, canvas, brick, table, ball
    #настройка окна
    root = tk.Tk()
    root.title('Arcanoid') #название окна
    root.resizable(width=False, height=False) #окно неизменяемое
    xcenter = (root.winfo_screenwidth() - WIDTH) / 2 #в центр экрана
    ycenter = (root.winfo_screenheight() - HEIGHT) / 2
    root.geometry('%dx%d+%d+%d' % (WIDTH+100, HEIGHT, xcenter, ycenter))
    root.configure(background = '#3498db')
    # настройка холста (игрового поля)
    canvas = tk.Canvas(root, background = CANVAS_COLOR, width=WIDTH, height=HEIGHT)
    canvas.pack(side=tk.RIGHT)
    
    #a=canvas.create_text(10,10, text = "LEVEL 1",font='28')
    
    """
    label_level = tk.Label(text = "LEVEL 1")
    label_level.pack(side=tk.LEFT)

    label_score = tk.Label(text = "SCORE 0")
    label_score.pack(side=tk.TOP)
    """   
    #canvas.pack(fill=tk.BOTH, expand=1)
    
    table = Table(250,250,40)
    ball = Ball()
    
    

    
    canvas.bind('<Button-1>', canvas_left_click)
    canvas.bind('<Motion>', canvas_mouse_motion)

    # create wall
    #bricks=[]
    #for i in range(WALL_X):
    #    for j in range(WALL_Y):
    #        bricks.append = Brick(i, j)
    
    dy=100
    brick = [Wall(BRICK_S + i*(BRICK_W + BRICK_S) , dy + j*(BRICK_H + BRICK_S)) for j in range(WALL_Y) for i in range(WALL_X)]

    tick()
    root.mainloop()


if __name__ == "__main__":
    main()
