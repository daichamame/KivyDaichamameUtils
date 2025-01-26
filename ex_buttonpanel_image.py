#--------------------------------------------------------------------------------------------------
# タイトル：ボタンパネルを配置する
# 内容：ボタンに画像を張り付ける
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
        self.ids.id_a.set_dims(6,1)
        self.ids.id_b.set_dims(6,1)
        self.ids.id_main.set_dims(5,5)
        # 色の指定
        self.ids.id_a.set_color(Color(1,1,1,1),Color(.5,.3,.1,1),Color(.4,.3,.1,1))
        self.ids.id_b.set_color(Color(1,1,1,1),Color(.5,.3,.1,1),Color(.4,.3,.1,1))
        self.ids.id_main.set_color(Color(1,1,1,1),Color(.9,.8,.4,1),Color(.8,.7,.3,1))
        self.set_text()
    
    # 画像を配置
    def set_text(self):
        # 駒の配置
        self.ids.id_main.set_image(4,"img/mame.png",0)
        self.ids.id_main.set_image(5,"img/cha.png",180) # 画像を反転
        self.ids.id_main.set_image(6,"img/cha.png",180) # 画像を反転
        self.ids.id_main.set_image(7,"img/mame.png",0)
        self.ids.id_main.set_image(18,"img/mame.png",0)
        self.ids.id_main.set_image(21,"img/cha.png",180) # 画像を反転
        self.ids.id_main.set_image(22,"img/mame.png",0)
        self.ids.id_main.set_image(24,"img/cha.png",180) # 画像を反転
        self.ids.id_b.set_image(0,"img/mame.png",180)    # 画像を反転
        self.ids.id_a.set_image(5,"img/cha.png",0)
        self.display()

    # タッチした時の処理
    def on_touch_down(self, touch):
        print("pos:"+str(touch.pos))
        x = touch.pos[0]
        y = touch.pos[1]
        self.ids.id_a.touch_down(touch.pos)
        self.ids.id_main.touch_down(touch.pos)
        self.ids.id_b.touch_down(touch.pos)
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
            self.ids.id_a.touch_up(touch.pos)
            self.ids.id_b.touch_up(touch.pos)
            ret = self.ids.id_main.touch_up(touch.pos)
            if(ret is not None):
                image_path=self.ids.id_main.get_image(ret)
                print(image_path)
            return True
        return super(Ex_ButtonPanel, self).on_touch_up(touch)
    # サイズ変更
    def on_resize(self,width,height):
        self.display()
    # 画面の描画
    def display(self):
        self.ids.id_a.display()        
        self.ids.id_b.display()   
        self.ids.id_main.display()   
    # 終了ダイアログ
    def exit_dialog(self):
        popup = PopupExitDialog()
        popup.open()
# アプリの定義
class Ex_ButtonPanelApp(App):
    def __init__(self, **kwargs):
        super(Ex_ButtonPanelApp,self).__init__(**kwargs)
        self.title="ボタンに画像"              # ウィンドウタイトル名

    def build(self):
        kv_file = os.path.join(os.path.dirname(__file__), 'kv', 'ex_buttonpanel_image.kv') 
        Builder.load_file(kv_file)         # kvファイル名
        return Ex_ButtonPanel()

# メインの定義
if __name__ == '__main__':
    Ex_ButtonPanelApp().run()                                # クラスを指定

