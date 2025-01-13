#--------------------------------------------------------------------------
# レベルメーター
#--------------------------------------------------------------------------
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.clock import Clock
import psutil
import random
import sys
import os

import lib.levelmeter  as levelmeter # レベルメーターモジュールを読み込む

#--------------------------------------------------------------------------
# 終了コマンド
#--------------------------------------------------------------------------
class PopupExitDialog(Popup):
    pass
    # プログラム終了
    def exec_exit(self):
       sys.exit()
#--------------------------------------------------------------------------
# メインウィジット
#--------------------------------------------------------------------------
class Ex_LevelMeter(Widget):
    clk=''
    # 初期処理
    def __init__(self, **kwargs):
        super(Ex_LevelMeter, self).__init__(**kwargs)
        Clock.schedule_once(self.levelmeter_callback,1)         # 一回だけ実行
        self.clk=Clock.schedule_interval(self.levelmeter_callback,5)
        # ウィンドウサイズの指定
        Window.size = (320,240)
    # 更新処理
    def levelmeter_callback(self,dt):
        # CPU使用率取得
        cpu_per= psutil.cpu_percent()
        self.ids.cpu_info.text=str(cpu_per) + "%"
        self.ids.cpu_info_meter.value=int(cpu_per/5)

        # メモリ使用率取得
        mem_info=psutil.virtual_memory()
        self.ids.mem_info.text="メモリ使用率:"+ str(mem_info.percent) + "%"
        # レベルメーターに値をセット
        self.ids.mem_info_meter.value=int(mem_info.percent/5)
        
        # ディスク使用率取得
        disk_info=psutil.disk_usage('/')
        self.ids.disk_info.text="ディスク使用率:"+ str(disk_info.percent) + "%"
        # レベルメーターに値をセット
        self.ids.disk_info_meter.value=int(disk_info.percent/5)

        # 更新間隔設定スライダー
        self.ids.interval_info.text="更新間隔:"+ format(self.ids.slider_interval.value,".1f") + "秒"
        # レベルメーターに値をセット（10個のランダム値）
        self.ids.multilevelmeter.multivalue=(random.randint(0,20),random.randint(0,20),random.randint(0,20),random.randint(0,20),random.randint(0,20),\
                                           random.randint(0,20),random.randint(0,20),random.randint(0,20),random.randint(0,20),random.randint(0,20),)
    # スライダー値変更
    def on_touch_up(self, touch):
        # 更新間隔の再設定
        self.set_interval(self.ids.slider_interval.value)
        self.ids.multilevelmeter.set_interval(self.ids.slider_interval.value)
        self.ids.cpu_info_meter.set_interval(self.ids.slider_interval.value)
        self.ids.mem_info_meter.set_interval(self.ids.slider_interval.value)
        return super().on_touch_up(touch)

    # 更新間隔の変更（インターバルの再設定）
    def set_interval(self,sec):
        # 一度描画を更新する
        Clock.schedule_once(self.levelmeter_callback,1)
        # 現在設定されているスケジュールをキャンセル
        try:
            self.clk.cancel()
        except:
            print("failed to cancel")
        # 新しい更新間隔でスケジュールを設定
        try:            
            self.clk=Clock.schedule_interval(self.levelmeter_callback,sec)
        except:
            print("failed to set interval")
    # 終了ダイアログ
    def exit_dialog(self):
        popup = PopupExitDialog()
        popup.open()

# アプリの定義
class Ex_LevelMeterApp(App):  
    def __init__(self, **kwargs):
        super(Ex_LevelMeterApp,self).__init__(**kwargs)
        self.title="レベルメーター"                          # ウィンドウタイトル名

    def build(self):
        kv_file = os.path.join(os.path.dirname(__file__), 'kv', 'ex_levelmeterapp.kv') 
        Builder.load_file(kv_file)         # kvファイル名
        return Ex_LevelMeter()

# メインの定義
if __name__ == '__main__':
    Ex_LevelMeterApp().run()                                # クラスを指定

