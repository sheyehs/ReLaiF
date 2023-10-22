import sys
from functools import partial
import logging
import typing
from PyQt6 import QtCore, QtGui

from PyQt6.QtCore import Qt, QPoint, QEvent
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QTextEdit,
    QLineEdit,
    QPlainTextEdit,
    QVBoxLayout,
)
from PyQt6.QtGui import QPixmap, QMouseEvent, QEnterEvent, QKeyEvent

WINDOW_X = 100
WINDOW_Y = 100
WINDOW_W = 640
WINDOW_H = 640
IMAGE_PATH = "./assets/soyo.png"

class TextEdit(QPlainTextEdit):
    def __init__(self, parent: QWidget | None = ...):
        super().__init__(parent=parent)
        self.key_pressed_slot: callable = None
        
    def keyPressEvent(self, e: QKeyEvent | None) -> None:
        """because QTextEdit does not has returnPressed handler"""
        super().keyPressEvent(e)  # otherwise other hot keys will be abandoned
        if e.key() == Qt.Key.Key_Return and e.modifiers() == Qt.KeyboardModifier.ShiftModifier and self.hasFocus():
            # TODO: test Key_Return value on Linux
            # print("enter")
            self.key_pressed_slot()

            
    def setKeyPressedSlot(self, slot: callable):
        self.key_pressed_slot = slot 
    
class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        # self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_W, WINDOW_H)
        self.setFixedSize(WINDOW_W, WINDOW_H)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)  
                
        self.figure = QLabel("figure", self)  
        self.figure.setFixedSize(WINDOW_W, WINDOW_H)  # must set size to enble AlignCenter
        image = QPixmap(IMAGE_PATH)
        image = image.scaled(WINDOW_W, WINDOW_H, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.figure.setPixmap(image)
        # self.figure.setStyleSheet("background-color: cyan")
        self.figure.setAlignment(Qt.AlignmentFlag.AlignCenter)  # algin the image to the center
        
        self.chat = QVBoxLayout()
        self.chatbox = TextEdit(self)
        self.chatbox.setFixedSize(WINDOW_W, WINDOW_H // 2)
        self.chatbox.setStyleSheet("background-color: rgba(255, 255, 255, 0.8)")
        # self.chatbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chatbox.setPlaceholderText("长久未见。")
        self.chatbox.hide()
        self.chat.addWidget(self.chatbox)
        self.chat.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.setLayout(self.chat)
    
        
        self.prev_mouse_pos: QPoint = None
 
    # drag and move
    def mousePressEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.prev_mouse_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            delta = event.globalPosition().toPoint() - self.prev_mouse_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.prev_mouse_pos = event.globalPosition().toPoint()
    
    # show text box
    def enterEvent(self, event: QEnterEvent | None) -> None:
        self.chatbox.show()
        self.chatbox.setFocus()

        
    def leaveEvent(self, a0: QEvent | None) -> None:
        self.chatbox.hide()
        

