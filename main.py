import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QPoint, QUrl, QSize
from PyQt5.QtGui import QIcon, QPainter, QColor
from PyQt5.QtWebEngineWidgets import QWebEngineView

# These will be replaced by the GitHub Action during build
TARGET_URL = "https://google.com"
APP_NAME = "WebToEXE App"

class TitleBar(QWidget):
    def __init__(self, parent=None, browser=None):
        super(TitleBar, self).__init__(parent)
        self.parent = parent
        self.browser = browser
        self.start = QPoint(0, 0)
        self.pressing = False
        
        self.setFixedHeight(40)
        self.setStyleSheet("background-color: rgba(25, 25, 25, 0.98);")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 15, 0)
        layout.setSpacing(15)
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(15)
        
        self.btn_back = self.create_nav_button("←", self.browser.back if self.browser else None)
        self.btn_forward = self.create_nav_button("→", self.browser.forward if self.browser else None)
        self.btn_reload = self.create_nav_button("↻", self.browser.reload if self.browser else None)
        
        nav_layout.addWidget(self.btn_back)
        nav_layout.addWidget(self.btn_forward)
        nav_layout.addWidget(self.btn_reload)
        
        # Title
        self.title_label = QLabel(APP_NAME)
        self.title_label.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-weight: 600; font-size: 13px; font-family: -apple-system, sans-serif;")
        self.title_label.setAlignment(Qt.AlignCenter)
        
        # Window controls
        win_layout = QHBoxLayout()
        win_layout.setSpacing(12)
        
        self.btn_min = self.create_win_button("#ffbd2e", self.parent.showMinimized)
        self.btn_max = self.create_win_button("#27c93f", self.toggle_maximize)
        self.btn_close = self.create_win_button("#ff5f56", self.parent.close)
        
        win_layout.addWidget(self.btn_min)
        win_layout.addWidget(self.btn_max)
        win_layout.addWidget(self.btn_close)
        
        layout.addLayout(nav_layout)
        layout.addWidget(self.title_label, 1)
        layout.addLayout(win_layout)

    def create_nav_button(self, text, callback):
        btn = QPushButton(text)
        btn.setFixedSize(24, 24)
        btn.setStyleSheet("""
            QPushButton { 
                color: white; 
                background: transparent; 
                border: none; 
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { opacity: 0.7; }
        """)
        if callback:
            btn.clicked.connect(callback)
        return btn

    def create_win_button(self, color, callback):
        btn = QPushButton()
        btn.setFixedSize(12, 12)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 6px;
                border: none;
            }}
            QPushButton:hover {{
                border: 1px solid rgba(0,0,0,0.2);
            }}
        """)
        btn.clicked.connect(callback)
        return btn

    def toggle_maximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.start = self.mapToGlobal(event.pos())
            self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing and not self.parent.isMaximized():
            end = self.mapToGlobal(event.pos())
            movement = end - self.start
            self.parent.setGeometry(self.parent.mapToGlobal(movement).x(),
                                    self.parent.mapToGlobal(movement).y(),
                                    self.parent.width(),
                                    self.parent.height())
            self.start = end

    def mouseReleaseEvent(self, event):
        self.pressing = False


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(1280, 720)
        
        # Central widget
        central_widget = QWidget(self)
        central_widget.setStyleSheet("background-color: #ffffff;")
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Browser
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(TARGET_URL))
        
        # Title bar
        self.title_bar = TitleBar(self, self.browser)
        
        layout.addWidget(self.title_bar)
        layout.addWidget(self.browser)


if __name__ == '__main__':
    # Fix scaling on high DPI displays
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
