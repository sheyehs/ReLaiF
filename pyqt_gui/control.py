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
        self.tts_model = VoicePlayer("芭芭拉")
        self._add_slots()
        # self._connect()
        
    def _add_slots(self):
        self.view.chatbox.setKeyPressedSlot(partial(self._chat, self.view.chatbox))

    def _connect(self):
        self.view.chatbox.connect(partial(self._chat, self.view.chatbox))
        
        
    def _hello(self, edit: QLineEdit):
        edit.setText("一如初见。")
        edit.setFocus()
        
    def _chat(self, edit):
        edit.setFocus()
        question = edit.toPlainText()
        edit.setPlainText("(少女思索中~~~)")
        edit.show()
        edit.setReadOnly(True)
        response = self.chat_model.chat_once(question)
        edit.setPlainText(response)
        edit.show()
        edit.setFocus()
        
        self.tts_model.request_and_play(response)
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