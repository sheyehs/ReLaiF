import sys
from functools import partial
import time
from threading import Thread
from view import Window

from PyQt6.QtWidgets import QApplication, QLineEdit
from PyQt6.QtCore import QTimer
import numpy as np

sys.path.append("C:\\Users\\sheye\\repos\\ReLaiF")
from openai_model.chatgpt import ChatGPT
from tts_model.genshinvoice import VoicePlayer
from asr_model.wav2vec2 import Wav2Vec2
from asr_model.microphone_recorder import MicrophoneRecorder
from sa_model.sentiment_analyzer import SentimentAnalyzer


LISTEN_PERIOD = 100  # in ms

class Controller:
    """PyCalc's controller class."""

    def __init__(self, view: Window):
        self.view = view
        self.chat_model = ChatGPT()
        self.tts_model = VoicePlayer("刻晴", 1, 1.5)
        
        self.asr_model = Wav2Vec2()
        self.recorder = MicrophoneRecorder(250, 1, LISTEN_PERIOD, self.asr_model.sampling_rate)
        timer = QTimer()
        timer.timeout.connect(self._listen)
        self.timer = timer
        
        self.sa_model = SentimentAnalyzer()
        
        self._connect()
        
        # start
        self.recorder.start()  
        self.timer.start(LISTEN_PERIOD)
        
    def _connect(self):
        self.view.chatbox.setKeyPressSlot(partial(self._chat, self.view.chatbox))
        self.view.windowIconTextChanged.connect(self._stop_timer)
        self.view.windowTitleChanged.connect(self._restart_timer)
        
        
    def _hello(self, edit: QLineEdit):
        edit.setText("一如初见。")
        edit.setFocus()
        
    def _chat(self, edit):
        # disable any input
        self.view.windowIconTextChanged.emit("yahu")  #  just used to stop QTimer for asr listening
        edit.setReadOnly(True)  # text
        print("all inputs were disabled")
        
        send_text = edit.toPlainText()
        edit.setPlainText("（少女思索中~~~）")
        
        response = self.chat_model.chat_once(send_text)
        # response = "！！只能合成中文字符和部分标点符号！不能合成英语字符和数字。     。对于这些字符会直接跳过。？请转换为发音接近的汉字！！！！"
        
        sa_thread = Thread(target=self._show_feeling, args=[response])
        sa_thread.start()
        # self._show_feeling(response)
        
        self.tts_model.request_and_play(response, edit)
        edit.appendPlainText("（少女解释完毕。。。）")
        
        # enable input
        print("enabling all input...")
        edit.setReadOnly(False)
        self.view.windowTitleChanged.emit("haha")  #  just used to restart QTimer for asr listening
        
        # edit.setFocus()
        
    def _listen(self):
        # get audio frames from recorder pool
        frames = self.recorder.listen()
        
        if len(self.view.chatbox.toPlainText()) == 0 and frames is not None:            
            # pass to asr model
            text = self.asr_model.regonize_once([frames])
            
            # display text TextEdit
            self.view.chatbox.setPlainText(text)
    
    def _stop_timer(self):
        self.timer.stop()
        
    def _restart_timer(self):
        self.timer.start(LISTEN_PERIOD)
        
    def _show_feeling(self, text):
        feeling = self.sa_model.analyze_once(text)
        # decouple the control and view by calling a function defined in view
        self.view.show_feeling(feeling)
        
    def show(self):
        self.view.show()
        
        
def main():
    pycalcApp = QApplication([])
    view = Window()
    controller = Controller(view)
    controller.show()
    sys.exit(pycalcApp.exec())

if __name__ == "__main__":
    main()