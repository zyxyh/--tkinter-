import tkinter as tk
from tkinter import messagebox
import random

FPS = 300  # 刷新页面的毫秒间隔
cell_size = 30  # 每格的宽度
Columns = 12
Rows = 20
height = Rows * cell_size
width = Columns * cell_size    
score = 0  # 得分
p_s = False  # 暂停/开始 pause/start

# 定义各种形状 字典
SHAPES = {
    "O": [(-1, -1), (0, -1), (-1, 0), (0, 0)],
    "S": [(-1, 0), (0, 0), (0, -1), (1, -1)],
    "T": [(-1, 0), (0, 0), (0, -1), (1, 0)],
    "I": [(0, 1), (0, 0), (0, -1), (0, -2)],
    "L": [(-1, 0), (0, 0), (-1, -1), (-1, -2)],
    "J": [(-1, 0), (0, 0), (0, -1), (0, -2)],
    "Z": [(-1, -1), (0, -1), (0, 0), (1, 0)],
}

# 定义各种形状的颜色
SHAPESCOLOR = {
    "O": "#d25b6a",
    "S": "#d2835b",
    "T": "#e5e234",
    "I": "#83d05d",
    "L": "#2862d2",
    "J": "#35b1c0",
    "Z": "#5835c0"
}

board_cell_list = []  # 存储行、列内容

current_block = None  # 存储当前的俄罗斯方块
next_block = None  # 存储下一个俄罗斯方块

win = tk.Tk()    # tkinter GUI编程必备
win.title("俄罗斯方块") # 标题
win.geometry('520x600')  # 设置窗体大小

SVar = tk.StringVar()  # 这句放在win = tk.Tk()前面不可以，编译报错，奇怪
# StringVar类型的内容和Label联系起来后可以自动更新标签内容
# SVar.set("得分：%s"%score)  # set设置内容  get获取内容

frame0 = tk.Frame(win,width=width, height=height) #左边框架，放置canvas
frame0.pack(side='left')
canvas = tk.Canvas(frame0, width=width, height=height) # 俄罗斯方块板
canvas.pack()

frame1 = tk.Frame(win,width=160, height=height,bg="#cccccc") # 右边框架，防止标签等
frame1.pack(side='right')

label = tk.Label(frame1,textvariable=SVar, font=("黑体", 20),bg="#cccccc")
label.place(x=2, y=30)   # 显示得分，textvariable=SVar 可以根据SVar自动改变显示

bufCanvas = tk.Canvas(frame1,width=160,height=160,bg="#cccccc",relief="flat")
bufCanvas.place(x=0,y=200)  # 缓冲区，显示下一个待用的俄罗斯方块

label2 = tk.Label(frame1,text="← →移动\n↑旋转\n空格 暂停/继续", font=("黑体", 16),bg="#cccccc")
label2.place(x=2, y=400)  # 提示

# 定义一个Board类，操作与之相关的初始化、绘制、清空、检查等
class Board():  
    def __init__(self): # 类的初始化函数，自动调用
        for r in range(Rows): # Rows X Columns 初始都为''
            i_row = ['' for j in range(Columns)]
            board_cell_list.append(i_row)
    
    def draw_blankboard(self):  # 画一个空白板
        canvas.create_rectangle(0,0,width,height,
                                fill="#CCCCCC", # 浅灰色
                                outline="gray", 
                                width=1) # 先画一个空矩形
        for ri in range(1,Rows): # 画横线
            canvas.create_line(0,ri*cell_size,width,ri*cell_size,
                            fill="#dcdcdc",
                            width=1)
        for ci in range(1,Columns):  # 画竖线
            canvas.create_line(ci*cell_size,0,ci*cell_size,height,
                            fill="#dcdcdc",
                            width=1)  
    def draw_board(self):
        self.draw_blankboard()
        # 根据board_cell_list内容，把面板上每个方块画出来
        for ri in range(Rows):
            for ci in range(Columns):        
                cell_type = board_cell_list[ri][ci]
                if cell_type:   #如果cell有内容，则画出其颜色（由SHAPESCOLOR字典确定）
                    canvas.create_rectangle(ci*cell_size,ri*cell_size,(ci+1)*cell_size,(ri+1)*cell_size,
                                            fill=SHAPESCOLOR[cell_type],
                                            outline="black",
                                            width=1)
    
    #把确定的方块存到board_cell_list表里
    def save_block_to_list(self, shape_type, c, r, block_list):
        '''
        param shape_type: 方块的颜色
        param c,r : 方块的位置
        block_list: 方块的形状
        '''
        for cell in block_list:
            cc, cr = cell
            # block_list 在对应位置记下其类型
            board_cell_list[r+cr][c+cc] = shape_type
    
    def check_row_complete(self, row): # 检查第row行是否满了
        for cell in row:
            if cell=='': # 如果有一个为''，则说明本行不满
                return False
        return True  # 如果没有'',则说明本行满了
    
    def check_and_clear(self):
        global score
        for ri in range(Rows):
            if self.check_row_complete(board_cell_list[ri]):
                score += 10  # 加10分
                for cur_ri in range(ri, 1, -1):
                    board_cell_list[cur_ri] = board_cell_list[cur_ri-1][:]
                board_cell_list[0] = ['' for j in range(Columns)]
                self.draw_board()
        
    def clearboard(self):  # 清空板子
        for r in range(Rows):
            for c in range(Columns):
                board_cell_list[r][c] = ''
        self.draw_blankboard()

board = Board()
board.draw_blankboard()

class TetrisBlock():
    '定义俄罗斯方块类'
    def __init__(self):
        # 随机生成俄罗斯方块
        self.type = random.choice(list(SHAPES.keys()))
        self.color = SHAPESCOLOR[self.type]
        self.block_cell = SHAPES[self.type]
        self.cr = [Columns//2,0]
        self.ids = []  # 当前俄罗斯方块的绘图id值 
        angle = random.randint(0,3) # 旋转次数
        if angle > 0 :
            self.block_cell = self.rotate_angle(self.block_cell, angle)
        
    def rotate_angle(self, block_cell_list, angle=1):
        angle_dict = {
            0: (1, 0, 0, 1),
            1: (0, 1, -1, 0),
            2: (-1, 0, 0, -1),
            3: (0, -1, 1, 0),
        }
        a, b, c, d = angle_dict[angle]

        rotate_block_cell_list = []
        for cell in block_cell_list:
            cc, cr = cell
            rc, rr = a * cc + b * cr, c*cc+d*cr
            rotate_block_cell_list.append((rc, rr))

        return rotate_block_cell_list

    def draw_block(self, c, r):
        """
        绘制指定形状指定颜色的俄罗斯方块
        :param r: 该形状设定的原点所在的行
        :param c: 该形状设定的原点所在的列
        :return:
        """
        for cell in self.block_cell:
            cell_c, cell_r = cell
            # 判断该位置方格在画板内部(画板外部的方格不再绘制)
            if 0 <= c < Columns and 0 <= r < Rows:
                x0 = (cell_c + c)*cell_size
                y0 = (cell_r + r)*cell_size
                cell_id = canvas.create_rectangle(x0,y0,x0+cell_size,y0+cell_size,
                                            fill=self.color,
                                            outline="black",
                                            width=1)
                self.ids.append(cell_id)

    # 绘制向指定方向移动后的俄罗斯方块
    def move(self, direction=[0, 0]):
        """
        绘制向指定方向移动后的俄罗斯方块
        :param direction: 俄罗斯方块移动方向
        :return:
        """
        dc, dr = direction
        self.cr[0] += dc
        self.cr[1] += dr
        for cell_id in self.ids:
            canvas.move(cell_id, dc * cell_size, dr * cell_size)


    #判断俄罗斯方块是否可以朝指定方向移动
    def check_move(self, direction=[0, 0]):
        """
            判断俄罗斯方块是否可以朝指定方向移动
            :param direction: 俄罗斯方块移动方向
            :return: boolean 是否可以朝指定方向移动
            """
        c1, r1 = self.cr
        
        for cell in self.block_cell:
            cell_c, cell_r = cell
            c = cell_c + c1 + direction[0]
            r = cell_r + r1 + direction[1]
            # 判断该位置是否超出左右边界，以及下边界
            # 一般不判断上边界，因为俄罗斯方块生成的时候，可能有一部分在上边界之上还没有出来
            if c < 0 or c >= Columns or r >= Rows:
                return False

            # 必须要判断r不小于0才行，具体原因你可以不加这个判断，试试会出现什么效果
            if r >= 0 and board_cell_list[r][c]:
                return False

        return True
    
    def save_block_to_list(self):
        for cell in self.block_cell:
            c0,r0 = cell
            board_cell_list[self.cr[1]+r0][self.cr[0]+c0] = self.type
    
    def rotate(self):
        old_block = self.block_cell
        self.block_cell = self.rotate_angle(old_block, 1)

        if self.check_move([0,0]) is False:
            self.block_cell = old_block
            return
        else:
            for i in range(len(self.block_cell)):
                cell_c,cell_r = old_block[i]
                rotate_c,rotate_r = self.block_cell[i]
                dc = rotate_c - cell_c
                dr = rotate_r - cell_r
                canvas.move(self.ids[i],dc*cell_size,dr*cell_size)
        
    def land(self):

        max_down = 0
        for i in range(Rows):
            if self.check_move([0,i]) is True:
                max_down = i
            else:
                break
        self.move([0,max_down])
        
    def draw_buf(self):
        bufCanvas.create_rectangle(0,0,160,160,fill='#cccccc',width=0)
        top=bottom=left=right=0
        for cell in self.block_cell:
            c,r = cell
            top = min(r,top)
            bottom = max(r,bottom)
            left = min(c,left)
            right = max(c,right)
        
        dx0 = 80-(left+right+1)*cell_size/2
        dy0 = 80-(top+bottom+1)*cell_size/2
        
        for cell in self.block_cell:
            c,r = cell
            x0 = c * cell_size + dx0
            y0 = r * cell_size + dy0
            bufCanvas.create_rectangle(x0,y0,x0+cell_size,y0+cell_size,
                                       fill=self.color,
                                       outline='black' )

def game_loop():
    global current_block, next_block, score, SVar, board, p_s    
    
    if p_s is True:
        return
    
    win.update()
    
    if next_block is None:
        next_block = TetrisBlock()
    
    if current_block is None:
        current_block = next_block
        next_block = TetrisBlock()
        # 新生成的俄罗斯方块需要先在生成位置绘制出来
        current_block.draw_block(Columns//2, 0)
        next_block.draw_buf()
        if not current_block.check_move([0, 0]):
            tryagain = messagebox.askretrycancel("Game Over! Your Score is %s" % score,"Tra again?")
            if tryagain:
                current_block = None 
                next_block = None 
                score = 0
                board.clearboard()
                game_loop()
            else:
                win.destroy()
                return
    else:
        if current_block.check_move([0, 1]):
            current_block.move([0, 1])
        else:
            # 无法移动，记入 block_list 中
            current_block.save_block_to_list()
            board.draw_board()
            current_block = None
    
    board.check_and_clear()
    SVar.set('得分:%s'%score)
    # win.title("SCORES: %s" % score)  标题中展示分数

    win.after(FPS, game_loop)

def left(event):
    global current_block
    if current_block is not None:
        if current_block.check_move([-1,0]):
            current_block.move([-1,0])

def right(event):
    global current_block
    if current_block is not None:
        if current_block.check_move([1,0]):
            current_block.move([1,0])

def rotate(event):
    global current_block
    if current_block is not None:
        current_block.rotate()

def land(event):
    global current_block
    if current_block is not None:
        current_block.land()

def pause_start(event):
    global p_s
    p_s = not(p_s) 
    game_loop()
    
canvas.focus_set() # 聚焦到canvas画板对象上
canvas.bind("<KeyPress-Left>", left)
canvas.bind("<KeyPress-Right>", right)
canvas.bind("<KeyPress-Up>", rotate)
canvas.bind("<KeyPress-Down>", land)
canvas.bind("<space>", pause_start)

win.update()
win.after(FPS, game_loop) # 在FPS 毫秒后调用 game_loop方法

win.mainloop()