import tkinter as tk
from random import randint
from math import hypot

BRICK_W = 40 # ширина кирпича 
BRICK_H = 20 # высота кирпича
BRICK_S = 5 # промежуток между кирпичами

WALL_X = 10 # количество кирпичей по x
WALL_Y = 5 # количество кирпичей по y
# вычисляем ширину игрового пространства (холста)
WIDTH = WALL_X * BRICK_W + BRICK_S * (WALL_X + 1) # промежутков на один больше чем кирпичей
HEIGHT = 400#BRICK_H * WALL_Y * 10 # высота холста в N раза больше высоты кирпичей
CANVAS_COLOR = '#212f3c' # цвет холста

SPACE_TOP = 100 # смещение кирпичей от верха
TABLE_H = 10 # высота ракетки
TABLE_W = 40 # ширина ракетки
# рисуем ракетку посередине, почти внизу
table_start_x, table_start_y = WIDTH/2, HEIGHT - 20

class Table: # ракетка
    # конструктор
    def __init__(self,
                 table_x,
                 table_y
                 ):#,
                 #table_w
                 #):
        self.table_x = table_x
        self.table_y = table_y
        #self.table_w = TABLE_W
        '''
        # прямоугольня ракетка
        self.table_id = canvas.create_rectangle(table_x - table_w,
                                                table_y - TABLE_H,
                                                table_x + table_w,
                                                table_y + TABLE_H,
                                                fill = 'orange',
                                                width = 0,
                                                outline='yellow'
                                                )
        '''
        # дуговая ракетка
        self.table_id = canvas.create_oval(table_x - TABLE_W,
                                           table_y - TABLE_H,
                                           table_x + TABLE_W,
                                           table_y + TABLE_H,
                                           fill = 'orange',
                                           #stipple='gray25',
                                           width = 0,
                                           outline='yellow'
                                                )
        
    # метод класса - ставим ракетку на новые координаты
    def move_table(self, xnew, ynew):
        xold, yold = self.table_x, self.table_y
        dx = xnew - xold
        dy = ynew - yold
        canvas.move(self.table_id, dx, dy)
        self.table_x, self.table_y = xnew, ynew


class Ball: # летающий шарик 
    # конструктор
    def __init__(self):
        self.ball_x = table_start_x
        self.ball_y = table_start_y - TABLE_H * 2
        self.ball_r = 10
        self.dx, self.dy = -2, -10
        self.ball_id = canvas.create_oval(self.ball_x - self.ball_r,
                                          self.ball_y - self.ball_r,
                                          self.ball_x + self.ball_r,
                                          self.ball_y + self.ball_r,
                                          fill = 'light green',
                                          width = 0,
                                          outline='gold'
                                          )
        
    # методы класса - шарик летит и отскакивает от стен
    def move_ball(self):
        # проверяем на столкновение с боковыми стенками
        if self.ball_x + self.ball_r > WIDTH or self.ball_x - self.ball_r <= 0:
            self.dx = -self.dx
        # проверяем на столкновение с низом
        if self.ball_y + self.ball_r > HEIGHT:
            ball.game_over()
            self.dy = -self.dy
        # проверяем на столкновение с верхом
        if self.ball_y - self.ball_r <= 0:
            self.dy = -self.dy

        # определяем столкновения шарика с ракеткой и кирпичами
        overlapping = canvas.find_overlapping(self.ball_x - self.ball_r,
                                          self.ball_y - self.ball_r,
                                          self.ball_x + self.ball_r,
                                          self.ball_y + self.ball_r)
        for f in overlapping: # просмотрим кортеж с номерами встреченых объектов
            if f == 1: # первый созданный объект это ракетка
                self.dy = -self.dy
                self.dx=(self.ball_x - table.table_x)/5 # меняем угол отскока
                            #в зависим. от месте соударения шарика по ракетке
            elif f == 2: # второй - это сам шарик
                pass
            else:
                self.dy = -self.dy
                brick[f - 3].kill_brick()# с 3-го объекта это уже кирпичи       
                # подсчитываем очки
                lbl_score['text'] = 'SCORE ' + str(WALL_X * WALL_Y - len(count_brick))
                # проверяем есть ли еще кирпичи
                if len(count_brick) == 0:
                      ball.game_win()
                break # выходим из просмотра кортежа чтоб исчезал только 1 кирпич
                   
        self.ball_x += self.dx
        self.ball_y += self.dy        
        canvas.move(self.ball_id, self.dx, self.dy)


    def game_over(self):
        canvas.create_text(WIDTH/2, SPACE_TOP/2,
                           text = "GAME OVER",
                           fill = 'red',
                           font='Arial 50')
        self.dx, self.dy = 0, 0

    def game_win(self):
            canvas.create_text(WIDTH/2, SPACE_TOP/2,
                               text = "YOU WIN!",
                               fill = 'green',
                               font='Arial 50')
            self.dx, self.dy = 0, 0


class Wall: # стена из кирпичей
    # конструктор
    def __init__(self,
                 x,
                 y):
        self.br_x = x
        self.br_y = y
        c='#' + str("{0:X}".format(randint(100,255))) + \
                str("{0:X}".format(randint(100,255))) + \
                str("{0:X}".format(randint(100,255))) # цвет в формате '#12AB5F'
        self.brick_id = canvas.create_rectangle(self.br_x,
                                                self.br_y,
                                                self.br_x + BRICK_W,
                                                self.br_y + BRICK_H,
                                                fill = c,
                                                width = 0,
                                                outline = c
                                                )
        global count_brick # счетчик кирпичей для определения конца игры
        count_brick = [i for i in range(WALL_X * WALL_Y)]
        
    # методы класса
    def kill_brick(self):
        canvas.delete(self.brick_id)
        count_brick.pop(-1) # уменьшаем счетчик кирпичей
        

def canvas_left_click(event):
    x, y = event.x, event.y
    # запускаем таймер
    tick()

    
def canvas_mouse_motion(event):
    x, y = event.x, event.y
    table.move_table(x,y)
    

def tick():
    ball.move_ball() # шарик двигается ...
    root.after(50, tick) # ...через каждые 50 миллисекунд


def main():
    global root, canvas, brick, table, ball, lbl_score
    #настройка окна
    root = tk.Tk()
    root.title('Arcanoid') #название окна
    root.resizable(width=False, height=False) #окно неизменяемое
    xcenter = (root.winfo_screenwidth() - WIDTH) / 2 #в центр экрана
    ycenter = (root.winfo_screenheight() - HEIGHT) / 2
    root.geometry('%dx%d+%d+%d' % (WIDTH+200, HEIGHT, xcenter, ycenter))
    root.configure(background = 'cornflower blue')#'#3498db')
    # настройка холста (игрового поля)
    canvas = tk.Canvas(root, background = CANVAS_COLOR, width=WIDTH, height=HEIGHT)
    canvas.pack(side=tk.RIGHT) # пусть холст будет справа


    lbl_level = tk.Label(text="LEVEL 1", width = 15)
    lbl_level.place(x=20, y=20)
    lbl_score = tk.Label(text="SCORE 0", width = 15)
    lbl_score.place(x=20, y=50)
    

    # создаем ракетку
    table = Table(table_start_x, table_start_y)

    # создаем шарик
    ball = Ball()

    # связываем методы с мышкой   
    canvas.bind('<Button-1>', canvas_left_click)
    canvas.bind('<Motion>', canvas_mouse_motion)

    # создаем кирпичи 
    brick=[]
    for j in range(WALL_Y):
        for i in range(WALL_X):
            x = BRICK_S + i*(BRICK_W + BRICK_S)
            y = SPACE_TOP + j*(BRICK_H + BRICK_S)
            brick.append(Wall(x ,y))
            
    #lbl_score['text'] = 'fdsfdsf'

    root.mainloop()

if __name__ == "__main__":
    main()
