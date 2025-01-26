#--------------------------------------------------------------------------
# ボタンパネル
# 
# 縦(row),横(col)を指定した複数のボタンを１つのクラスにまとめたモジュール
# ボタンは、フォント、背景、枠 の色を指定できます。
# 文字、画像の大きさは、ボタンの大きさに併せて変わります。
# 画像は回転させることができます。
#--------------------------------------------------------------------------
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle,Line,Rotate
from kivy.core.text import Label as CoreLabel
from kivy.core.image import Image as CoreImage
#--------------------------------------------------------------------------------------
# ボタンパネルウィジット
#--------------------------------------------------------------------------------------
class ButtonPanel(Widget):

    # 初期処理
    def __init__(self, **kwargs):
        super(ButtonPanel, self).__init__(**kwargs)
        # 変数の初期化
        self.btn_no = 0                          # 押したボタンの番号
        self.btn_array = []             # ボタンのラベルの値を管理する配列
        self.btn_image_array = []       # ボタンの画像を管理する配列
        self.font_color = Color(1,.5,1)           # フォントの色
        self.btn_color  = Color(.3,.3,.3,0)       # ボタンの色
        self.btn_line_color = Color(.1,.1,.1)    # ボタン枠の色
        self.btn_acolor  = Color(1-self.btn_color.r,1-self.btn_color.b,1-self.btn_color.g)  # ボタンが押されたときの色(反転)
        self.rows = 1                            # ボタンの縦の個数
        self.cols = 1                            # ボタンの横の個数
        self.btn_width = 0                       # ボタン1つの幅
        self.btn_height = 0                      # ボタン1つの高さ
        self.border = 1                          # 枠の太さ
        self.btn_valign = "middle"               # 文字の縦位置
        self.btn_halign = "center"               # 文字の横位置
        self.btn_image_valign = 1                # 画像の縦位置(0:top,1:middle,2:bottom)
        self.btn_image_halign = 1                # 画像の横位置(0:left,1:center,2:right)
        self.image_rotate = [1, 0, 0, 0, 0, 1, 1, 1] # 画像の回転(0,90,180,270)

    # ボタンの縦横の数を指定
    def set_dims(self,rows,cols):
        self.rows = rows
        self.cols = cols
        self.btn_array= [''] * (rows * cols)    # ラベル用配列作成
        for _ in range(rows * cols):
            self.btn_image_array.append({"path": "", "rotate":0})   # 画像用配列
                                       
        self.display()      # 画面更新
    # ボタンを表示
    def display(self):
        self.canvas.clear()                        # キャンバスを初期化
        self.btn_width = self.width/self.cols      # ボタンの幅
        self.btn_height = self.height/self.rows    # ボタンの高さ
        for i in range(self.cols):
            for j in range(self.rows):
                # ボタン背景
                self.canvas.add(self.btn_color)
                self.canvas.add(Rectangle(pos=(self.x+i*self.btn_width,self.y+j*self.btn_height),size=(self.btn_width,self.btn_height)))
                self.canvas.add(self.btn_line_color)       
                self.canvas.add(Line(rectangle=(self.x+i*self.btn_width+self.border,self.y+j*self.btn_height+self.border,self.btn_width-2*self.border,self.btn_height-2*self.border),width=self.border))
                # 画像の設定
                try:
                    image = CoreImage(self.btn_image_array[(self.rows * self.cols)-(self.cols-i-1)-self.cols*j-1]['path']).texture
                    image_scale = min(self.btn_width/image.size[0],self.btn_height/image.size[1])
                    self.canvas.add(Color(1,1,1,1))
                    dx = ((self.btn_width - image.size[0]*image_scale)/2)*self.btn_image_halign
                    dy = ((self.btn_height - image.size[1]*image_scale)/2)*self.btn_image_valign
                    rot = self.get_image_rotate(self.btn_image_array[(self.rows * self.cols)-(self.cols-i-1)-self.cols*j-1]['rotate'])
                    self.canvas.add(Rectangle(texture=image,pos=(self.x+i*self.btn_width+dx,self.y+j*self.btn_height+dy),size=(image.size[0]*image_scale,image.size[1]*image_scale),tex_coords=rot))
                except:
                    pass
                # ラベルの設定
                str_len = len(self.btn_array[(self.rows * self.cols)-(self.cols-i-1)-self.cols*j-1]) # ラベルの文字数を取得
                if (str_len != 0):
                    # ラベルのフォントサイズを計算
                    labelfont_size = int(min(self.btn_width/str_len,self.btn_height)*0.8)
                    # ラベルの設定
                    label = CoreLabel(text=self.btn_array[(self.rows * self.cols)-(self.cols-i-1)-self.cols*j-1],font_size=labelfont_size,valign=self.btn_valign,halign=self.btn_halign)
                    label.text_size=(self.width/self.cols,self.height/self.rows)
                    label.refresh()
                    labeltext = label.texture    
                    self.canvas.add(self.font_color)
                    self.canvas.add(Rectangle(texture=labeltext,pos=(self.x+i*self.btn_width,self.y+j*self.btn_height),size=(self.btn_width,self.btn_height)))
  
    # 押された位置のボタンの色を反転
    def touch_down(self,pos_s):
        # キャンバス内であれば、描く
        if self.collide_point(*pos_s):  # 
            dx=int((pos_s[0]-self.x)/self.btn_width)
            dy=int((pos_s[1]-self.y)/self.btn_height)
            self.btn_no = (self.rows*self.cols)-(self.cols-dx-1)-self.cols*dy-1
            self.canvas.add(self.btn_acolor)
            self.canvas.add(Rectangle(pos=(self.x+dx*self.btn_width,self.y+dy*self.btn_height),size=(self.btn_width,self.btn_height)))
            return True
        return super(ButtonPanel,self).on_touch_down(pos_s)
    # 押されたボタンの値を返す
    def touch_up(self,pos_s):
        # キャンバス内であれば、描く
        self.display()
        if self.collide_point(*pos_s):  #
            # touch_downイベントで選ばれたボタンを値を返す
            return self.btn_no
        return super(ButtonPanel,self).on_touch_up(pos_s)
    # ボタンラベルの設定
    def set_text(self,num,btn_str):
        """ ボタンにラベルを設定 """
        if(num < (self.rows*self.cols)):
            self.btn_array[num]=btn_str
    # ボタン画像の設定
    def set_image(self,num,btn_str,rot):
        """ ボタンに画像を設定 （ファイルのパス）"""
        if(num < (self.rows*self.cols) and (rot == 0 or rot == 90 or rot == 180 or rot == 270)):
            self.btn_image_array[num]['path']=btn_str
            self.btn_image_array[num]['rotate']=rot
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
    # 文字の位置設定
    def set_image_align(self,valign,halign):
        """ 画像の位置は、1パネルで1種類
        画像の位置指定は標準ではない、計算して配置
        """
        if (valign == "top"):
            self.btn_image_valign = 0
        elif(valign == "middle"):
            self.btn_image_valign = 1
        elif(valign == "bottom"):
            self.btn_image_valign = 2
        if (halign == "left"):
            self.btn_image_halign = 0
        elif(halign == "center"):
            self.btn_image_halign = 1
        elif(halign == "right"):
            self.btn_image_halign = 2
    # 画像の回転
    def get_image_rotate(self,rot):
        """ tex_coordsの値に変換 """
        if(rot == 90):
            val = [1, 1, 1, 0, 0, 0, 0, 1]
        elif(rot == 180):
            val = [1, 0, 0, 0, 0, 1, 1, 1]
        elif(rot == 270):
            val = [0, 0, 0, 1, 1, 1, 1, 0]
        else:
            val = [0, 1, 1, 1, 1, 0, 0, 0]
        return val
    # 配列を初期化
    def clear_text(self):
        self.btn_array= [''] * (self.rows * self.cols)
    # ラベルの値を取得
    def get_text(self,num):
        """ ラベルの値を取得"""
        return self.btn_array[num]
    # 画像パスと回転を取得
    def get_image(self,num):
        """ 画像配列の情報を取得,path,rotのリストで返す """
        return self.btn_image_array[num]
    