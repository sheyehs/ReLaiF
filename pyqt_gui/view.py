import sys
from functools import partial
import logging

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel
)
from PyQt6.QtGui import QPixmap, QMouseEvent

WINDOW_X = 100
WINDOW_Y = 100
WINDOW_W = 600
WINDOW_H = 600
IMAGE_PATH = "./assets/soyo.png"

class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        # self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_W, WINDOW_H)
        self.setFixedSize(WINDOW_W, WINDOW_H)
        label = QLabel("content", parent=self)    
        image = QPixmap(IMAGE_PATH)
        image = image.scaled(WINDOW_W, WINDOW_H, Qt.AspectRatioMode.KeepAspectRatio)
        label.setPixmap(image)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)   
        
        self.prev_mouse_pos: QPoint = None
 
        
    def mousePressEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.prev_mouse_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.prev_mouse_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.prev_mouse_pos = event.globalPosition().toPoint()
        

def main():
    pycalcApp = QApplication([])
    pycalcWindow = Window()
    pycalcWindow.show()
    sys.exit(pycalcApp.exec())

if __name__ == "__main__":
    main()