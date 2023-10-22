import sys
import os
from functools import partial

from view import Window

from PyQt6.QtWidgets import QApplication, QLineEdit

sys.path.append("C:\\Users\\sheye\\repos\\ReLaiF")
from openai_model.chatgpt import ChatGPT


class Controller:
    """PyCalc's controller class."""

    def __init__(self, view: Window):
        self.view = view
        self.chat_model = ChatGPT()
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
        response = self.chat_model.chat_once(edit.toPlainText())
        edit.setPlainText(response)
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