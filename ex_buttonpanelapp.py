#--------------------------------------------------------------------------------------------------
# タイトル：ボタンパネルを配置する
# 内容：縦一列、横一列、縦横７ｘ７に配列したボタンのサンプル
#--------------------------------------------------------------------------------------------------
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
import sys
from kivy.clock import Clock
import lib.buttonpanel as ButtonPanel
import os

#--------------------------------------------------------------------------------------
# プログラムの終了ダイアログ
#--------------------------------------------------------------------------------------
class PopupExitDialog(Popup):
    pass
    # プログラム終了
    def exec_exit(self):
       sys.exit()
#--------------------------------------------------------------------------------------
# メインウィジット
#--------------------------------------------------------------------------------------
class Ex_ButtonPanel(Widget):
    # 初期処理
    def __init__(self, **kwargs):
        # ウィンドウサイズの指定
        Window.size=(640,480)
        Window.bind(size = self.on_resize)
        super(Ex_ButtonPanel, self).__init__(**kwargs)
        Clock.schedule_once(self.init_callback,1)
    # 起動時の初回だけ実行
    def init_callback(self,dt):
        # ボタンの数を指定
        self.ids.id_bp_vertical.set_dims(6,1)
        self.ids.id_bp_horizontal.set_dims(1,8)
        self.ids.id_bp_7x7.set_dims(7,7)
        # 色の指定
        self.ids.id_bp_vertical.set_color(Color(1,1,1),Color(.5,.5,.2),Color(.3,.3,.1))
        self.ids.id_bp_horizontal.set_color(Color(.6,1,1),Color(.2,.5,.4),Color(.1,.3,.1))
        self.ids.id_bp_7x7.set_color(Color(1,1,.6),Color(.5,.2,.2),Color(.3,.1,.1))
        self.set_text()
    
    def set_text(self):
        # ボタンラベルの設定
        self.ids.id_bp_vertical.set_text(0,"経済ニュース")
        self.ids.id_bp_vertical.set_text(1,"社会ニュース")
        self.ids.id_bp_vertical.set_text(2,"国際ニュース")
        self.ids.id_bp_vertical.set_text(3,"政治ニュース")
        self.ids.id_bp_vertical.set_text(4,"地域ニュース")
        self.ids.id_bp_vertical.set_text(5,"スポーツニュース")

        self.ids.id_bp_horizontal.set_text(0,"日")
        self.ids.id_bp_horizontal.set_text(1,"月")
        self.ids.id_bp_horizontal.set_text(2,"火")
        self.ids.id_bp_horizontal.set_text(3,"水")
        self.ids.id_bp_horizontal.set_text(4,"木")
        self.ids.id_bp_horizontal.set_text(5,"金")
        self.ids.id_bp_horizontal.set_text(6,"土")
        self.ids.id_bp_horizontal.set_text(7,"祝")

        for x in range(0,49):
            self.ids.id_bp_7x7.set_text(x,str(x+1))
        self.display()

    # タッチした時の処理
    def on_touch_down(self, touch):
        # 縦ボタン
        self.ids.id_bp_vertical.touch_down(touch.pos)
        # 横ボタン
        self.ids.id_bp_horizontal.touch_down(touch.pos)
        # 7x7のボタン
        self.ids.id_bp_7x7.touch_down(touch.pos)
        touch.grab(self)
        super(Ex_ButtonPanel, self).on_touch_down(touch)
        return True
    # タッチしたまま移動した時の処理
    def on_touch_move(self, touch):
        if touch.grab_current is self:
            return True
        return super(Ex_ButtonPanel, self).on_touch_move(touch)
    # タッチした状態から離れた時の処理
    def on_touch_up(self, touch):
        """ どのボタンが押されたかを判別 """
        if touch.grab_current is self:
            touch.ungrab(self)
            ret = self.ids.id_bp_vertical.touch_up(touch.pos)
            print("vertical = " + str(ret))
            ret = self.ids.id_bp_horizontal.touch_up(touch.pos)
            print("horizontal = " + str(ret))
            ret = self.ids.id_bp_7x7.touch_up(touch.pos)
            print("7x7 = " + str(ret))
            return True
        return super(Ex_ButtonPanel, self).on_touch_up(touch)
    # サイズ変更
    def on_resize(self,width,height):
        Window.size=(self.size)   # サイズ固定する場合に設定
    # 画面の描画
    def display(self):
        self.ids.id_bp_vertical.display()        
        self.ids.id_bp_horizontal.display()   
        self.ids.id_bp_7x7.display()   
    # 終了ダイアログ
    def exit_dialog(self):
        popup = PopupExitDialog()
        popup.open()
# アプリの定義
class Ex_ButtonPanelApp(App):
    def __init__(self, **kwargs):
        super(Ex_ButtonPanelApp,self).__init__(**kwargs)
        self.title="ボタンパネルデモ"              # ウィンドウタイトル名

    def build(self):
        kv_file = os.path.join(os.path.dirname(__file__), 'kv', 'ex_buttonpanelapp.kv') 
        Builder.load_file(kv_file)         # kvファイル名
        return Ex_ButtonPanel()

# メインの定義
if __name__ == '__main__':
    Ex_ButtonPanelApp().run()                                # クラスを指定

