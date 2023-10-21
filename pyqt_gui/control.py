import sys
from functools import partial

from view import Window

from PyQt6.QtWidgets import QApplication, QLineEdit


class Controller:
    """PyCalc's controller class."""

    def __init__(self, view: Window):
        self.view = view
        self._connect()

    def _connect(self):
        self.view.chatbox.returnPressed.connect(partial(self._hello, self.view.chatbox))
        
        
    def _hello(self, edit: QLineEdit):
        edit.setText("一如初见。")
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