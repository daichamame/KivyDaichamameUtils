#--------------------------------------------------------------------------
# ボタンパネル
# 
# 縦(row),横(col)を指定した複数のボタンを１つのクラスにまとめたモジュール
# ボタンは、フォント、背景、枠 の色を指定できます。
# 文字の大きさは、ボタンの大きさに併せて変わります。
#--------------------------------------------------------------------------
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle,Line
from kivy.core.text import Label as CoreLabel

#--------------------------------------------------------------------------------------
# ボタンパネルウィジット
#--------------------------------------------------------------------------------------
class ButtonPanel(Widget):
    # 変数の初期化
    rows = 1                            # ボタンの縦の個数
    cols = 1                            # ボタンの横の個数
    btn_width = 0                       # ボタン1つの幅
    btn_height = 0                      # ボタン1つの高さ
    border = 1                          # 枠の太さ
    btn_valign = "middle"               # 文字の縦位置
    btn_halign = "center"               # 文字の横位置

    # 色
    font_color = Color(1,1,1)           # フォントの色
    btn_color  = Color(.3,.3,.3)        # ボタンの色
    btn_line_color = Color(.1,.1,.1)    # ボタン枠の色
    btn_acolor  = Color(1-btn_color.r,1-btn_color.b,1-btn_color.g)  # ボタンが押されたときの色(反転)
    btn_array = []                      # ボタンのラベルの値を管理する配列
    btn_no = 0                          # 押したボタンの番号

    # 初期処理
    def __init__(self, **kwargs):
        super(ButtonPanel, self).__init__(**kwargs)

    # ボタンの縦横の数を指定
    def set_dims(self,rows,cols):
        self.rows = rows
        self.cols = cols
        self.btn_array= [''] * (rows * cols)
        self.display()      # 画面更新
    # ボタンを表示
    def display(self):
        self.canvas.clear()                         # キャンバスを初期化
        self.btn_width = self.width/self.cols      # ボタンの幅
        self.btn_height = self.height/self.rows    # ボタンの高さ
        self.canvas.add(Color(1,1,1))   #白
        for i in range(self.cols):
            for j in range(self.rows):
                # ラベルの文字数を取得
                str_len = len(self.btn_array[(self.rows * self.cols)-(self.cols-i-1)-self.cols*j-1])
                if (str_len == 0):
                    str_len = 1
                # ラベルのフォントサイズを計算
                labelfont_size = int(min(self.btn_width/str_len,self.btn_height)*0.8)
                # ラベルの設定
                label = CoreLabel(text=self.btn_array[(self.rows * self.cols)-(self.cols-i-1)-self.cols*j-1],font_size=labelfont_size,valign=self.btn_valign,halign=self.btn_halign)
                label.text_size=(self.width/self.cols,self.height/self.rows)
                label.refresh()
                labeltext = label.texture
                # ボタン背景
                self.canvas.add(self.btn_color)
                self.canvas.add(Rectangle(pos=(self.x+i*self.btn_width,self.y+j*self.btn_height),size=(self.btn_width,self.btn_height)))
                # ボタンラベル
                self.canvas.add(self.font_color)
                self.canvas.add(Rectangle(texture=labeltext,pos=(self.x+i*self.btn_width,self.y+j*self.btn_height),size=(self.btn_width,self.btn_height)))
                # ボタン枠
                self.canvas.add(self.btn_line_color)       
                self.canvas.add(Line(rectangle=(self.x+i*self.btn_width+self.border,self.y+j*self.btn_height+self.border,self.btn_width-2*self.border,self.btn_height-2*self.border),width=self.border))

    # 押された位置のボタンの色を反転
    def touch_down(self,pos_s):
        # キャンバス内であれば、描く
        if((pos_s[1] > self.y)*(pos_s[1] < self.y + self.height)*(pos_s[0] > self.x)*(pos_s[0] < self.x + self.width)):
            x=int((pos_s[0]-self.x)/self.btn_width)
            y=int((pos_s[1]-self.y)/self.btn_height)
            self.btn_no = (self.rows*self.cols)-(self.cols-x-1)-self.cols*y-1
            self.canvas.add(self.btn_acolor)
            self.canvas.add(Rectangle(pos=(x*self.btn_width+self.x,y*self.btn_height+self.y),size=(self.btn_width,self.btn_height)))
            self.canvas.add(self.btn_line_color)        
            self.canvas.add(Line(rectangle=(x*self.btn_width+self.x+1,y*self.btn_height+self.y+1,self.btn_width-2,self.btn_height-2)))
    # 押されたボタンの値を返す
    def touch_up(self,pos_s):
        # キャンバス内であれば、描く
        self.display()
        if((pos_s[1] > self.y)*(pos_s[1] < self.y + self.height)*(pos_s[0] > self.x)*(pos_s[0] < self.x + self.width)):
            # touch_downイベントで選ばれたボタンを値を返す
            return self.btn_no
        return -1
    # ボタンラベルの設定
    def set_text(self,num,btn_str):
        """ ボタンにラベルを設定 """
        if(num < (self.rows*self.cols)):
            self.btn_array[num]=btn_str
    # 色の設定
    def set_color(self,font_color,btn_color,line_color):
        """ font_color ... フォントの色
            btn_color ... ボタンの背景
            line_color ... ボタンの枠の色 """
        self.font_color=font_color
        self.btn_color=btn_color
        self.btn_line_color=line_color
        self.btn_acolor  = Color(1-self.btn_color.r,1-self.btn_color.b,1-self.btn_color.g)
    # 文字の位置設定
    def set_align(self,valign,halign):
        """ 文字の位置は、1パネルで1種類"""
        if (valign == "top" or valign == "middle" or valign == "bottom"):
            self.btn_valign = valign
        if (halign == "left" or halign == "center" or halign == "rightt"):
            self.btn_halign = halign
    # 配列を初期化
    def clear_text(self):
        self.btn_array= [''] * (self.rows * self.cols)
    # ラベルの値を取得
    def get_text(self,num):
        return self.btn_array[num]
    