import tkinter as tk
from tkinter import messagebox
import random

cell_size = 30  # 每格的宽度
Columns = 12
Rows = 20

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

# 定义一个Board类，操作与之相关的初始化、绘制、清空、检查等
class Board():  
    def __init__(self, canvas): # 类的初始化函数，自动调用
        self.cell_table = []
        self.cellID_table = []
        self.canvas = canvas
        
        for r in range(Rows): # Rows X Columns 初始都为''对应颜色为底色（灰色）
            i_row = ['' for j in range(Columns)]  # '' means blank
            self.cell_table.append(i_row)
        for r in range(Rows): # Rows X Columns 初始都为''
            i_row = [None for j in range(Columns)]
            self.cellID_table.append(i_row)
        for ri in range(Rows): 
            for ci in range(Columns):  
                self.cellID_table[ri][ci] = \
                    self.canvas.create_rectangle(
                    ci*cell_size,ri*cell_size,
                    (ci+1)*cell_size,(ri+1)*cell_size,
                    fill="#CCCCCC",
                    outline="#dcdcdc",
                    width=1)
     
    def update_board(self):  # 更新
        for ri in range(Rows):
            for ci in range(Columns):
                if self.cell_table[ri][ci] != '':
                    fillcolor = SHAPESCOLOR[self.cell_table[ri][ci]]
                else:
                    fillcolor = "#CCCCCC"
                self.canvas.itemconfigure(self.cellID_table[ri][ci],
                                            fill=fillcolor)
                
    def check_row_complete(self, row): # 检查第row行是否满了
        return (self.cell_table[row].count('') == 0)
        
    def check_and_clear(self):
        score = 0
        for ri in range(Rows):
            if self.check_row_complete(ri):
                score += 10
                for cur_ri in range(ri, 1, -1):
                    self.cell_table[cur_ri] = self.cell_table[cur_ri-1][:]
                self.cell_table[0] = ['' for j in range(Columns)]
                self.update_board()
        return score    # 返回得分，总分应该加上此次得分
        
    def clearboard(self):  # 清空板子
        for r in range(Rows):
            for c in range(Columns):
                self.cell_table[r][c] = ''
        self.update_board()

class TetrisBlock():
    def __init__(self, canvas, board):
        # 随机生成俄罗斯方块
        self.canvas = canvas
        self.board = board
        self.type = random.choice(list(SHAPES.keys()))
        self.color = SHAPESCOLOR[self.type]
        self.block_cell = SHAPES[self.type]
        self.cr = [Columns//2,0]
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
    
    def show_block(self, c, r):
        """
        绘制指定形状指定颜色的俄罗斯方块
        :param r: 该形状设定的原点所在的行
        :param c: 该形状设定的原点所在的列
        :return:
        """
        for cell in self.block_cell:
            cell_c, cell_r = cell
            cc = cell_c + c
            cr = cell_r + r
            # 判断该位置方格在画板内部(画板外部的方格不再绘制)
            if 0 <= cc < Columns and 0 <= cr < Rows:
                self.canvas.itemconfigure(self.board.cellID_table[cr][cc],
                                          fill=self.color)
                
    # 绘制向指定方向移动后的俄罗斯方块
    def move(self, direction=[0, 0]):
        """
        绘制向指定方向移动后的俄罗斯方块
        :param direction: 俄罗斯方块移动方向
        :return:
        """
        for cell in self.block_cell:  # 在原地把对应cell填充色改成背景色
            cell_c, cell_r = cell
            cc = cell_c + self.cr[0]
            cr = cell_r + self.cr[1]
            if 0 <= cc < Columns and 0 <= cr < Rows:
                self.canvas.itemconfigure(self.board.cellID_table[cr][cc],
                                      fill="#CCCCCC")

        self.cr[0] += direction[0]
        self.cr[1] += direction[1]
        for cell in self.block_cell:    #在新位置重新填充颜色
            cell_c, cell_r = cell
            cc = cell_c + self.cr[0]
            cr = cell_r + self.cr[1]
            if 0 <= cc < Columns and 0 <= cr < Rows:
                self.canvas.itemconfigure(self.board.cellID_table[cr][cc],
                                      fill=self.color)

    #判断俄罗斯方块是否可以朝指定方向移动
    def check_move(self, direction=[0, 0]):
        """
            判断俄罗斯方块是否可以朝指定方向移动
            :param direction: 俄罗斯方块移动方向
            :return: boolean 是否可以朝指定方向移动
            """
        c1, r1 = self.cr
        dc, dr = direction
        
        for cell in self.block_cell:
            cell_c, cell_r = cell
            c = cell_c + c1 + dc
            r = cell_r + r1 + dr
            # 判断该位置是否超出左右边界，以及下边界
            # 一般不判断上边界，因为俄罗斯方块生成的时候，可能有一部分在上边界之上还没有出来
            if c < 0 or c >= Columns or r >= Rows:
                return False

            # 必须要判断r不小于0才行，具体原因你可以不加这个判断，试试会出现什么效果
            if r >= 0 and (self.board.cell_table[r][c] != ''):
                return False

        return True
    
    def save_block_to_table(self):
        for cell in self.block_cell:
            c0,r0 = cell
            self.board.cell_table[self.cr[1]+r0][self.cr[0]+c0] = self.type
    
    def rotate(self):
        old_block = self.block_cell
        self.block_cell = self.rotate_angle(old_block, 1)

        if self.check_move([0,0]) is False:  # 如果不能转动
            self.block_cell = old_block
            return
        else:
            for i in range(len(self.block_cell)):  # 把每一cell填充背景色
                cell_c,cell_r = old_block[i]
                cc = cell_c + self.cr[0]
                cr = cell_r + self.cr[1]
                self.canvas.itemconfigure(self.board.cellID_table[cr][cc],
                                      fill="#CCCCCC")
                
            for i in range(len(self.block_cell)):  # 在旋转后的cell重新填色
                rotate_c,rotate_r = self.block_cell[i]
                cc = rotate_c + self.cr[0]
                cr = rotate_r + self.cr[1]
                self.canvas.itemconfigure(self.board.cellID_table[cr][cc],
                                      fill=self.color)    
        
    def land(self):
        max_down = 0
        for i in range(Rows):
            if self.check_move([0,i]) is True:
                max_down = i
            else:
                break
        self.move([0,max_down])
        
    def draw_buf(self, bufCanvas):
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
                                       outline='#dcdcdc' )

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        
        self.width = Columns * cell_size
        self.height = Rows * cell_size
        self.master = master
        self.score = 0
        self.SVar = tk.StringVar()
        self.SVar.set("得分：%s"%self.score) 
        self.current_block = None
        self.next_block = None
        self.FPS = 200
        
        self.p_s = False    # pause_start

        self.create_widgets()

    def create_widgets(self):
        self.frame0 = tk.Frame(self,width=self.width, height=self.height) #左边框架，放置canvas
        self.frame0.pack(side='left')
        self.canvas = tk.Canvas(self.frame0, width=self.width, height=self.height) # 俄罗斯方块板
        self.canvas.pack()

        self.frame1 = tk.Frame(self,width=160, height=self.height,bg="#cccccc") # 右边框架，防止标签等
        self.frame1.pack(side='right')

        self.label1 = tk.Label(self.frame1,textvariable=self.SVar, font=("黑体", 20),bg="#cccccc")
        self.label1.place(x=2, y=30)   # 显示得分，textvariable=SVar 可以根据SVar自动改变显示

        self.bufCanvas = tk.Canvas(self.frame1,width=160,height=160,bg="#cccccc",relief="flat")
        self.bufCanvas.place(x=0,y=200)  # 缓冲区，显示下一个待用的俄罗斯方块

        self.label2 = tk.Label(self.frame1,text="← 左移\n→ 右移\n↑ 旋转\n空格 暂停/继续\n by 岳慧", \
                                font=("黑体", 16),bg="#cccccc")
        self.label2.place(x=2, y=400)  # 提示
        
        self.board = Board(self.canvas)
        
    def game_loop(self):
        if self.p_s is True:
            return
    
        self.master.update()
    
        if self.next_block is None:
            self.next_block = TetrisBlock(self.canvas, self.board)
        
        if self.current_block is None:
            self.current_block = self.next_block
            self.next_block = TetrisBlock(self.canvas, self.board)
            # 新生成的俄罗斯方块需要先在生成位置绘制出来
            self.current_block.show_block(Columns//2, 0)
            self.next_block.draw_buf(self.bufCanvas)
            if not self.current_block.check_move([0, 0]):
                if messagebox.askretrycancel("Game Over! Your Score is %s" % self.score,"Try again?"):
                    self.current_block = None 
                    self.next_block = None 
                    self.score = 0
                    self.board.clearboard()
                    self.game_loop()
                else:
                    self.master.destroy()
                    return
        else:  #如果能够向下移动，就移动一格
            if self.current_block.check_move([0, 1]):
                self.current_block.move([0, 1])
            else:   # 无法移动，记入 board 中
                self.current_block.save_block_to_table()
                self.score += self.board.check_and_clear()
                self.board.update_board()
                self.current_block = None
                self.SVar.set('得分:%s'%self.score)

        self.after(self.FPS, self.game_loop)

    def left(self, event):
        if self.current_block is not None:
            if self.current_block.check_move([-1,0]):
                self.current_block.move([-1,0])

    def right(self, event):
        if self.current_block is not None:
            if self.current_block.check_move([1,0]):
                self.current_block.move([1,0])

    def rotate(self, event):
        if self.current_block is not None:
            self.current_block.rotate()

    def land(self, event):
        if self.current_block is not None:
            self.current_block.land()

    def pause_start(self, event):
        self.p_s = not(self.p_s) 
        self.game_loop()
    
    def run(self):
        self.canvas.focus_set() # 聚焦到canvas画板对象上
        self.canvas.bind("<KeyPress-Left>", self.left)
        self.canvas.bind("<KeyPress-Right>", self.right)
        self.canvas.bind("<KeyPress-Up>", self.rotate)
        self.canvas.bind("<KeyPress-Down>", self.land)
        self.canvas.bind("<space>", self.pause_start)

        self.master.update()
        self.master.after(self.FPS, self.game_loop) # 在FPS 毫秒后调用 game_loop方法


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.master.title("俄罗斯方块  岳慧练习作品")
    app.run()
    app.mainloop()