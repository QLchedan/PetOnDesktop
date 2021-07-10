import PyQt5
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import PyQt5.QtCore
import sys
import time
import _thread
import json
import random


SayingList = []


with open('Image\\Config.json','r',encoding='utf-8') as con:
    SayingList = json.load(con)["Sayings"]


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.UIinit()
    
    def UIinit(self):
        l = QLabel("简易桌面宠物(V1.00) By千里扯淡 2021.7")
        self.setWindowTitle('关于')
        self.setWindowIcon(QIcon('icon.png'))
        grid = QGridLayout()
        grid.addWidget(l, 0, 0)
        self.setLayout(grid) 
        self.setGeometry(300, 300, 450, 300)


class TaryIcon(object):
    
    ap = QApplication(sys.argv)
    a_w = AboutWindow()
    
    def __init__(self, w):
        super().__init__()
        self.w = w
        self.app = app
        self.tp = QSystemTrayIcon(self.w)
        self.init()
        self.run(0,0)
    
    def init(self):
        self.tp.setToolTip(SayingList[random.randint(0,len(SayingList) - 1)])
        self.tp.setIcon(QIcon('icon.png'))
        self.tp.show()
        
    def act(self, reason):
        #print(reason)
        if reason == 2 or reason == 3:
            self.w.show()
        else:
            pass
            
    def run(self,a,b):
        a1 = QAction('&显示',triggered=self.w.show)
        a2 = QAction('&退出',triggered=QCoreApplication.instance().quit)
        a3 = QAction('&关于',triggered=self.a_w.show)
        tpMenu = QMenu()
        tpMenu.addAction(a1)
        tpMenu.addAction(a2)
        tpMenu.addAction(a3)
        self.tp.setContextMenu(tpMenu)
        self.tp.show()
        self.tp.activated.connect(self.act)
        sys.exit(self.app.exec_())


class Zc_MainWindow(QWidget):
    
    ImgLabel = None
    
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.rightMenuShow)
        self.UIinit()
        
    def UIinit(self):
        global ImgLabel
        
        FirstFrame = QPixmap('Image\\00000.png')
        
        ImgLabel = QLabel(self)
        ImgLabel.setPixmap(FirstFrame)
        ImgLabel.setScaledContents(True)
        
        self.setToolTip(SayingList[random.randint(0,len(SayingList) - 1)])
        
        grid = QGridLayout()
        grid.addWidget(ImgLabel, 0, 0)
        #grid.addWidget(btn, 5, 0)
        self.setLayout(grid) 
        self.setGeometry(300, 300, 450, 300)    
        self.show()
        _thread.start_new_thread(self.Play, (633,0.03))
        self.tray(1,2)
        
    def Play(self, count, fps):
        while True:
            for i in range(count):
                Frame = QPixmap('Image\\' + str(i).zfill(5))
                ImgLabel.setPixmap(Frame)
                ImgLabel.setScaledContents(True)
                QApplication.processEvents()
                time.sleep(fps)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            
    def mouseMoveEvent(self, event):
        if Qt.LeftButton and self.m_flag:  
            self.move(event.globalPos() - self.m_Position)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))
        
    def rightMenuShow(self):
        menu = QMenu(self)
        action = menu.addAction('隐藏至托盘')
        action.triggered.connect(self.hide)
        menu.exec_(QCursor.pos())
        
    def tray(self ,a ,b):
        tr = TaryIcon(self)

       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    ex = Zc_MainWindow()
    sys.exit(app.exec_())
