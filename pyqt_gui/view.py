import sys
from functools import partial
from threading import Thread
from PyQt6 import QtGui
import os

from PyQt6.QtCore import Qt, QPoint, QEvent, QThread
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QTextEdit,
    QLineEdit,
    QPlainTextEdit,
    QVBoxLayout,
    QSystemTrayIcon,
    QMenu,
)
from PyQt6.QtGui import QPixmap, QMouseEvent, QEnterEvent, QKeyEvent, QIcon

WINDOW_X = 100
WINDOW_Y = 100
WINDOW_W = 640
WINDOW_H = 640
ASSETS_PATH = "./assets"
IMAGE_PATH = "./assets/Sunaookami Shiroko"

class TextEdit(QPlainTextEdit):
    def __init__(self, parent: QWidget | None = ...):
        super().__init__(parent=parent)
        self.key_press_slot: callable = None
        self.temp_text: str = None
        
    def keyPressEvent(self, e: QKeyEvent | None) -> None:
        """because QTextEdit does not has returnPressed handler"""
        super().keyPressEvent(e)  # otherwise other hot keys will be abandoned
        if e.key() == Qt.Key.Key_Return and e.modifiers() == Qt.KeyboardModifier.ShiftModifier and self.hasFocus():
            # TODO: test Key_Return value on Linux
            print("shift+return pressed.")
            # TODO: find a better async method. Now it will create warnings.
            kp_thread = Thread(target=self.key_press_slot)
            kp_thread.start()
            print("thread started.")
            
    def setKeyPressSlot(self, slot: callable):
        self.key_press_slot = slot 
    
class Window(QWidget):
    
    def __init__(self):
        super().__init__()
        # self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_W, WINDOW_H)
        self.setFixedSize(WINDOW_W, WINDOW_H)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)  
                
        self.figure = QLabel("figure", self)  
        self.figure.setFixedSize(WINDOW_W, WINDOW_H)  # must set size to enble AlignCenter
        self._init_images()
        self.figure.setPixmap(self.images["normal"])
        # self.figure.setStyleSheet("background-color: cyan")
        self.figure.setAlignment(Qt.AlignmentFlag.AlignCenter)  # algin the image to the center
        
        self.chat = QVBoxLayout()
        self.chatbox = TextEdit(self)
        self.chatbox.setFixedSize(WINDOW_W, WINDOW_H // 2)
        self.chatbox.setStyleSheet("background-color: rgba(255, 255, 255, 0.8)")
        # self.chatbox.setAlignment(Qt.AlignmentFlag.AlignTop)  # control text layout in the editor
        # self.chatbox.setPlaceholderText("长久未见。")
        self.chatbox.hide()
        self.chat.addWidget(self.chatbox)
        self.chat.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.setLayout(self.chat)  
                
        self._set_system_tray_icon()
                
        # mouse dragging
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
        
    def _init_images(self):
        d = {}
        for t in ["normal", "happy", "sad"]:
            image = QPixmap(os.path.join(IMAGE_PATH, f"{t}.png"))
            image = image.scaled(WINDOW_W, WINDOW_H, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            d[t] = image
        self.images = d
    
    def show_feeling(self, feeling):
        feeling = feeling.value
        if feeling == -1:
            self.figure.setPixmap(self.images["sad"])
        elif feeling == 0:
            self.figure.setPixmap(self.images["normal"])
        elif feeling == 1 or feeling == 2:
            self.figure.setPixmap(self.images["happy"])
        
    def _set_system_tray_icon(self):
        icon = QSystemTrayIcon(QIcon(os.path.join(ASSETS_PATH, "system_tray_icon.png")), self)
        
        menu = QMenu(self)
        topAction = menu.addAction("Stays On Top")
        topAction.setCheckable(True)
        topAction.setChecked(True)
        topAction.toggled.connect(partial(self._toggle_stays_on_top, topAction, self))
        
        icon.setContextMenu(menu)
        icon.show()
        
    @staticmethod
    def _toggle_stays_on_top(action, window):
        if action.isChecked():
            window.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)  
        else:
            window.setWindowFlags(Qt.WindowType.FramelessWindowHint)  
        window.show()  # the widget needs to be shown again