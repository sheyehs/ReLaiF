import sys
import os
from functools import partial

from view import Window

from PyQt6.QtWidgets import QApplication, QLineEdit

sys.path.append("C:\\Users\\sheye\\repos\\ReLaiF")
from openai_model.chatgpt import ChatGPT
from tts_model.genshinvoice import VoicePlayer


class Controller:
    """PyCalc's controller class."""

    def __init__(self, view: Window):
        self.view = view
        self.chat_model = ChatGPT()
        self.tts_model = VoicePlayer("艾丝妲", 1, 1.5)
        self._add_slots()
        # self._connect()
        
    def _add_slots(self):
        self.view.chatbox.setKeyPressSlot(partial(self._chat, self.view.chatbox))

    def _connect(self):
        self.view.chatbox.connect(partial(self._chat, self.view.chatbox))
        
        
    def _hello(self, edit: QLineEdit):
        edit.setText("一如初见。")
        edit.setFocus()
        
    def _chat(self, edit):
        edit.temp_text = edit.toPlainText()
        edit.setPlainText("（少女思索中~~~）")
        edit.setReadOnly(True)
        
        response = self.chat_model.chat_once(edit.temp_text)
        # response = "！！只能合成中文字符和部分标点符号！不能合成英语字符和数字。     。对于这些字符会直接跳过。？请转换为发音接近的汉字！！！！"
        
        self.tts_model.request_and_play(response, edit)
        edit.appendPlainText("（少女解释完毕。。。）")
        
        edit.setReadOnly(False)
        edit.setFocus()
        
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