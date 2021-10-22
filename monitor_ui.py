# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'monitor.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import QPropertyAnimation, QRect, Qt, QCoreApplication, QMetaObject
from PySide2.QtGui import QMouseEvent, QFont
from PySide2.QtWidgets import QWidget, QApplication, QMenu, QLabel
from PySide2 import QtWidgets
import CurrencyEditUi


class Ui_Form(QWidget, object):

    def __init__(self):
        super().__init__()
        self._startPos = None
        self._wmGap = None
        self.hidden = False

        dsk = QApplication.primaryScreen()
        self.screen_width = dsk.geometry().width()
        self.screen_height = dsk.geometry().height()
        self.window_width = 140
        self.window_height = 60 #20 basic + 40*數量
        self.label_size = 'font: 13px'
        self.cpu_gui_x = 75
        # Inform threading.Timer
        self.ui_alive = True


    def enterEvent(self, event):
        self.hide_or_show('show', event)

    def leaveEvent(self, event):
        self.hide_or_show('hide', event)

    def hide_or_show(self, mode, event):
        # 获取窗口左上角x,y
        pos = self.frameGeometry().topLeft()
        if mode == 'show' and self.hidden:
            # 窗口左上角x + 窗口宽度 大于屏幕宽度，从右侧滑出
            if pos.x() + self.window_width >= self.screen_width:
                # 需要留10在里边，否则边界跳动
                self.startAnimation(self.screen_width - self.window_width, pos.y())
                event.accept()
                self.hidden = False
            # 窗口左上角x 小于0, 从左侧滑出
            elif pos.x() <= 0:
                self.startAnimation(0, pos.y())
                event.accept()
                self.hidden = False
            # 窗口左上角y 小于0, 从上方滑出
            elif pos.y() <= 0:
                self.startAnimation(pos.x(), 0)
                event.accept()
                self.hidden = False
        elif mode == 'hide' and (not self.hidden):
            if pos.x() + self.window_width >= self.screen_width:
                # 留10在外面
                self.startAnimation(self.screen_width - 10, pos.y(), mode, 'right')
                event.accept()
                self.hidden = True
            elif pos.x() <= 0:
                # 留10在外面
                self.startAnimation(10 - self.window_width, pos.y(), mode, 'left')
                event.accept()
                self.hidden = True
            elif pos.y() <= 0:
                # 留10在外面
                self.startAnimation(pos.x(), 10 - self.window_height, mode, 'up')
                event.accept()
                self.hidden = True

    def startAnimation(self, x, y, mode='show', direction=None):
        animation = QPropertyAnimation(self, b"geometry", self)
        # 滑出动画时长
        animation.setDuration(200)
        # 隐藏时，只留10在外边，防止跨屏
        # QRect限制其大小，防止跨屏
        num = QApplication.desktop().screenCount()
        if mode == 'hide':
            if direction == 'right':
                animation.setEndValue(QRect(x, y, 10, self.window_height))
            elif direction == 'left':
                # 多屏时采用不同的隐藏方法，防止跨屏
                if num < 2:
                    animation.setEndValue(QRect(x, y, self.window_width, self.window_height))
                else:
                    animation.setEndValue(QRect(0, y, 10, self.window_height))
            else:
                if num < 2:
                    animation.setEndValue(QRect(x, y, self.window_width, self.window_height))
                else:
                    animation.setEndValue(QRect(x, 0, self.window_width, 10))
        else:
            animation.setEndValue(QRect(x, y, self.window_width, self.window_height))
        animation.start()

    def mouseMoveEvent(self, event: QMouseEvent):
        # event.pos()减去最初相对窗口位置，获得移动距离(x,y)
        self._wmGap = event.pos() - self._startPos
        # 移动窗口，保持鼠标与窗口的相对位置不变
        # 检查是否移除了当前主屏幕
        # 左方界限
        final_pos = self.pos() + self._wmGap
        if self.frameGeometry().topLeft().x() + self._wmGap.x() <= 0:
            final_pos.setX(0)
        # 上方界限
        if self.frameGeometry().topLeft().y() + self._wmGap.y() <= 0:
            final_pos.setY(0)
        # 右方界限
        if self.frameGeometry().bottomRight().x() + self._wmGap.x() >= self.screen_width:
            final_pos.setX(self.screen_width - self.window_width)
        # 下方界限
        if self.frameGeometry().bottomRight().y() + self._wmGap.y() >= self.screen_height:
            final_pos.setY(self.screen_height - self.window_height)
        self.move(final_pos)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            # event.pos() 鼠标相对窗口的位置
            # event.globalPos() 鼠标在屏幕的绝对位置
            self._startPos = event.pos()
        if event.button() == Qt.RightButton:
            # 创建右键菜单
            menu = QMenu(self)
            menu.setStyleSheet(u"background-color: white;\n"
                               "selection-color: rgb(0, 255, 127);\n"
                               "selection-background-color: gray;\n"
                               "font: 8pt;")
            # 二级菜单
            size_menu = menu.addMenu('BackGroundColor')
            light_gray = size_menu.addAction('Light-Gray')
            gray = size_menu.addAction('Gray')
            black = size_menu.addAction('Black')

            #幣種菜單
            currency_menu = menu.addAction('EDIT')

            #show_menu = menu.addMenu('Show')
            #show_all = show_menu.addAction('show_all')
            #speed_only = show_menu.addAction('speed_only')
            # 普通菜单
            about_action = menu.addAction('About')
            quit_action = menu.addAction('Exit')

            # 窗口定位到鼠标处
            action = menu.exec_(self.mapToGlobal(event.pos()))

            # 改变背景色
            if action == light_gray:
                self.setStyleSheet(u"background-color: rgb(100, 100, 100)")
            if action == gray:
                self.setStyleSheet(u"background-color: rgb(50, 50, 50)")
            if action == black:
                self.setStyleSheet(u"background-color: black")

            if action == quit_action:
                self.ui_alive = False
                QCoreApplication.quit()
            if action == about_action:
                # 新建MessageBox
                msg_box = QtWidgets.QMessageBox()
                # 支持HTML输入
                msg_box.about(self, "About", "<font size='3' color='white'>"
                                             "--------------------------"
                                             "<p>"
                                             "<i><b>Author: </b>MuMuLin</i>"
                                             "</p>"
                                             "<p>"
                                             "<i><b>Version: </b>1.0.0</i>"
                                             "</p>"
                                             "<p>"
                                             "<i><b>More: </b><a href='https://github.com/MuMuShy'>"
                                             "<span style='color:white'>Visit Me</span></a></i>"
                                             "</p>"
                                             "</font>")
            if action == currency_menu:
                self.currencyWindow.show()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._startPos = None
            self._wmGap = None
        if event.button() == Qt.RightButton:
            self._startPos = None
            self._wmGap = None

    def setupUi(self, Form):
        self.loadSetting()
        self.window_height = 20+23*len(self.currencyList)
        if not Form.objectName():
            Form.setObjectName(u"Form")
        # 设置gui的font，获得小号字体
        font = QFont()
        font.setFamily(u"Agency FB")
        font.setPointSize(1)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(False)

        Form.resize(self.window_width, self.window_height)
        Form.setStyleSheet(u"background-color: rgb(50, 50, 50)")

        self.priceLabels=[]
        maxNumofCurrecny = 300
        for i in range(maxNumofCurrecny):
            self.upspeed = QLabel(Form)
            self.upspeed.setObjectName(u"upspeed")
            self.upspeed.setGeometry(QRect(0, 5+i*22, 150, 16))
            index = i+146
            while index >= len(self.colorList):
                index-=len(self.colorList)
            color = self.colorList[index]
            color = "yellow"
            _styleSheet = u"color:"+color

            self.upspeed.setStyleSheet(_styleSheet)
            self.upspeed.setText("")
            self.priceLabels.append(self.upspeed)
        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def getCurrencyList(self):
        return self.currencyList


    def retranslateUi(self, Form):
        Form.setWindowTitle("")


    def loadSetting(self):
        self.currencyList = []
        self.colorList=[]
        f = open('currencyList.txt', 'r')
        for line in f.readlines():
            self.currencyList.append(line.strip())
        f.close()
        print(self.currencyList)

        f = open('colors.txt', 'r')
        for line in f.readlines():
            self.colorList.append(line.strip())
        f.close()
