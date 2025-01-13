#--------------------------------------------------------------------------
# レベルメーター
# 
# LevelMeterV     :縦型メーター（20段階)
# MultiLevelMeterV:縦型マルチメーター（20段階)
# LevelMeterH     :横型メーター(20段階)
# 
#--------------------------------------------------------------------------
from kivy.uix.widget import Widget
from kivy.clock import Clock
from math import floor
from kivy.graphics import Color,Rectangle

# 縦型メーター(20段階)
class LevelMeterV(Widget):
    value=0  # 表示する値
    clk=''
    def __init__(self, **kwargs):
        super(LevelMeterV, self).__init__(**kwargs)
        Clock.schedule_once(self.update,1)         # 一回だけ実行
        self.clk=Clock.schedule_interval(self.update, 5)     #　定期的に描画更新
    # 描画処理
    def update(self,ct):
        self.canvas.clear()
        dh = floor(self.height/20)  # メモリ1つの高さ
        # valueの数までメモリを描く
        for i in range(self.value):
            #　色の計算
            self.canvas.add(Color((i>7)*(i<12)*0.3+(i>=12), 0.5+(i>=4)*(i<9) \
                *0.3+(i>=9)*(i<12)*0.5+(i>=12)*(i<18)*0.2+0.1, 0))
            # 四角形の描画
            self.canvas.add(Rectangle(pos=(self.x,self.y+i*dh),size=(self.width, dh-2)))
    # 更新間隔の設定
    def set_interval(self,sec):
        # 一度描画を更新する
        Clock.schedule_once(self.update,1)         # 一回だけ実行
        # 現在設定されているスケジュールをキャンセル
        try:
            self.clk.cancel()
        except:
            print("not get interval")
        # 新しい更新間隔でスケジュールを設定
        try:
            self.clk=Clock.schedule_interval(self.update,sec)
        except:
            print("failed to set interval")
# 縦型マルチメーター(20段階)
class MultiLevelMeterV(Widget):
    multivalue = ()  # 表示する値リスト
    clk=''
    def __init__(self, **kwargs):
        super(MultiLevelMeterV, self).__init__(**kwargs)
        Clock.schedule_once(self.update,1)         # 一回だけ実行
        self.clk=Clock.schedule_interval(self.update, 5)     #　定期的に描画更新
   
    # 描画処理
    def update(self,ct):
        cnt=len(self.multivalue)
        if(cnt==0):
            return
        self.canvas.clear()
        dw = floor(self.width/cnt)
        dh = floor(self.height/20)  # メモリ1つの高さ
        for c in range(cnt):
            # valueの数までメモリを描く
            for i in range(self.multivalue[c]):
                #　色の計算
                self.canvas.add(Color((i>7)*(i<12)*0.3+(i>=12), 0.5+(i>=4)*(i<9) \
                    *0.3+(i>=9)*(i<12)*0.5+(i>=12)*(i<18)*0.2+0.1, 0))
                # 四角形の描画
                self.canvas.add(Rectangle(pos=(self.x+c*dw,self.y+i*dh),size=(dw-1, dh-2)))
    # 更新間隔の設定
    def set_interval(self,sec):
        # 一度描画を更新する
        Clock.schedule_once(self.update,1)         # 一回だけ実行
        # 現在設定されているスケジュールをキャンセル
        try:
            self.clk.cancel()
        except:
            print("not get interval")            
        # 新しい更新間隔でスケジュールを設定
        try:
            self.clk=Clock.schedule_interval(self.update,sec)
        except:
            print("failed to set interval")            
# 横型メーター(20段階)
class LevelMeterH(Widget):
    value=0 # 表示する値
    clk=''
    def __init__(self, **kwargs):
        super(LevelMeterH, self).__init__(**kwargs)
        Clock.schedule_once(self.update,1)         # 一回だけ実行
        self.clk=Clock.schedule_interval(self.update, 5)     # 定期的に描画更新

    # 描画処理
    def update(self,ct):
        self.canvas.clear()
        dw = floor(self.width/20) # メモリ1つの幅
        # valueの数までメモリを描く
        for i in range(self.value):
            #　色の計算
            self.canvas.add(Color((i>7)*(i<12)*0.3+(i>=12), 0.5+(i>=4)*(i<9) \
                *0.3+(i>=9)*(i<12)*0.5+(i>=12)*(i<18)*0.2+0.1, 0))
            # 四角形の描画
            self.canvas.add(Rectangle(pos=(self.x+i*dw,self.y),size=(dw-2, self.height)))
    # 更新間隔の設定
    def set_interval(self,sec):
        # 一度描画を更新する
        self.update(0)
        # 現在設定されているスケジュールをキャンセル
        try:
            self.clk.cancel()
        except:
            print("not get interval")            
        # 新しい更新間隔でスケジュールを設定
        try:
            self.clk=Clock.schedule_interval(self.update,sec)
        except:
            print("failed to set interval")