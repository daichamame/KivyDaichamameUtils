#--------------------------------------------------------------------------------------------------
# タイトル：カレンダー（ボタンパネル利用版）
# 内容：カルーセルにボタンパネルと入力画面をはりつけて
#      連携できるようにしてみました
#      
#--------------------------------------------------------------------------------------------------
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from datetime import datetime,timedelta
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
class Ex_Carousel(Widget):
    # 表示しているカレンダーの年月
    year  = 0
    month = 0
    select_row = 0
    # 初期処理
    def __init__(self, **kwargs):
        # ウィンドウサイズの指定
        Window.size=(640,480)
        Window.bind(size = self.on_resize)
        super(Ex_Carousel, self).__init__(**kwargs)
        Clock.schedule_once(self.init_callback,1)
    # 起動時の初回だけ実行
    def init_callback(self,dt):
        self.ids.id_calendar_head.set_dims(1,7)
        self.ids.id_calendar.set_dims(6,7)
        self.ids.id_schedule.set_dims(10,1)
        self.ids.id_calendar_head.set_color(Color(1,1,1),Color(.3,.4,.5),Color(.1,.1,.1))
        self.ids.id_calendar.set_color(Color(1,1,1),Color(.2,.3,.4),Color(.1,.1,.1))
        self.ids.id_schedule.set_color(Color(.6,1,1),Color(.2,.4,.3),Color(.1,.1,.1))
        self.ids.id_schedule.set_align("middle","left")
        self.initial_screen()
    # ボタンのラベル設定
    def initial_screen(self):
        self.ids.id_calendar_head.set_text(0,"月")
        self.ids.id_calendar_head.set_text(1,"火")
        self.ids.id_calendar_head.set_text(2,"水")
        self.ids.id_calendar_head.set_text(3,"木")
        self.ids.id_calendar_head.set_text(4,"金")
        self.ids.id_calendar_head.set_text(5,"土")
        self.ids.id_calendar_head.set_text(6,"日")

        for i in range(0,10):
            self.ids.id_schedule.set_text(i,"予定"+str(i+1))

        # 現在日付でカレンダーを表示
        now_date = datetime.now()      # 現在の日付取得
        self.year = now_date.year               # 表示用の年に初期値設定
        self.month = now_date.month             # 表示用の月に初期値設定
        self.set_calendar()             # カレンダーの設定
        self.back_to_calendar()
    # カレンダー表示
    def set_calendar(self):
        first_day_weekday = datetime(self.year,self.month,1).weekday()  # 1日の曜日を取得
        # 
        last_day = datetime(self.year+(self.month == 12),(self.month + 1)*(self.month < 12)+(self.month == 12),1)-timedelta(days=1)
        # カレンダーの配列を初期化
        self.ids.id_calendar.clear_text()
        for i in range(first_day_weekday,first_day_weekday+last_day.day):
            self.ids.id_calendar.set_text(i,str(i-first_day_weekday+1))
        self.display()
    
    # タッチした時の処理
    def on_touch_down(self, touch):
        # 現在のカルーセルのインデックス取得
        current = self.ids.id_carousel.index
        # 表示されている画面毎に処理するイベントを分岐
        if current == 0:
            # カレンダーボタン
            self.ids.id_calendar.touch_down(touch.pos)
        elif current == 1:
            # タイムスケジュール
            self.ids.id_schedule.touch_down(touch.pos)
        touch.grab(self)
        super(Ex_Carousel, self).on_touch_down(touch)
        return True
    # タッチした状態から離れた時の処理
    def on_touch_up(self, touch):
        """ どのボタンが押されたかを判別 """
        if touch.grab_current is self:
            touch.ungrab(self)
            current = self.ids.id_carousel.index
            # 表示されている画面毎に処理するイベントを分岐
            if current == 0:    # 表示されている画面がカレンダーの場合
                ret = self.ids.id_calendar.touch_up(touch.pos)
                if(ret != -1):
                    val = self.ids.id_calendar.get_text(ret)  
                    if(val != ""):  # 日付を押した場合
                        self.ids.id_carousel.index = 1
                        self.ids.id_day_label.text = val + "日の予定"
            elif current == 1:  # 表示されている画面がスケジュールの場合
                ret = self.ids.id_schedule.touch_up(touch.pos)
                if(ret != -1):
                    self.select_row = ret
                    self.ids.id_carousel.index = 2
                    self.ids.id_textinput.text = str(ret+1) + "行目を選択しました。"
            self.display() 
            return True
        return super(Ex_Carousel, self).on_touch_up(touch)
    # サイズ変更
    def on_resize(self,width,height):
        Window.size=(self.size)     # ウィンドウサイズ固定する場合に設定
        # self.display()            # ウィンドウサイズを可変にする場合に設定
    # 画面の描画
    def display(self):
        current = self.ids.id_carousel.index
        if current == 0:
            self.ids.id_calendar_head.display()    
            self.ids.id_calendar.display()
        elif current == 1: 
            self.ids.id_schedule.display() 
        self.ids.id_year_month.text=str(self.year)+"年"+str(self.month)+"月"
    # 下部メニューボタン押下時の処理
    def menu_sw(self,cmd):
        if cmd == 'prev':               # < ボタン 1月前
            self.month = (self.month - 1)*(self.month > 1) + (self.month == 1)*12
            self.year = self.year*(self.month < 12) + (self.year - 1)*(self.month == 12)
        elif cmd == 'next':             # > ボタン 1月後
            self.month = (self.month + 1)*(self.month < 12) + (self.month == 12)
            self.year = self.year*(self.month > 1) + (self.year + 1)*(self.month == 1)
        elif cmd == 'down':             # - ボタン 1年前
            self.year = self.year - 1
        elif cmd == 'up':               # + ボタン 1年後
            self.year = self.year + 1
        else:
            print("nothing")
        self.set_calendar() # カレンダーを表示

    # カレンダーに戻る
    def back_to_calendar(self):
        self.ids.id_carousel.index = 0              
    # スケジュールに戻る
    def back_to_schedule(self):
        self.ids.id_carousel.index = 1
        input_text = self.ids.id_textinput.text
        self.ids.id_schedule.set_text(self.select_row,input_text) 
        self.display()
    # 終了ダイアログ
    def exit_dialog(self):
        popup = PopupExitDialog()
        popup.open()
# アプリの定義
class Ex_CarouselApp(App):
    def __init__(self, **kwargs):
        super(Ex_CarouselApp,self).__init__(**kwargs)
        self.title="カレンダー"              # ウィンドウタイトル名

    def build(self):
        kv_file = os.path.join(os.path.dirname(__file__), 'kv', 'ex_carousel.kv') 
        Builder.load_file(kv_file)         # kvファイル名
        return Ex_Carousel()

# メインの定義
if __name__ == '__main__':
    Ex_CarouselApp().run()                                # クラスを指定

