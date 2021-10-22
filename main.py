from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
from monitor_ui import Ui_Form
from PySide2 import QtCore
import psutil
import threading
import sys
import MyBinanceApi as binanceapi
from PySide2 import QtWidgets
from PySide2.QtCore import Qt, Signal, Slot
import CurrencyEditUi
import sys
import os

class Stats(Ui_Form):

    valueChanged = Signal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.currencyWindow = CurrencyEditUi.CurrencyUi_Form(self)
        # 设置窗口无边框； 设置窗口置顶；
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        # 设置窗口背景透明
        # self.setAttribute(Qt.WA_TranslucentBackground)
        # 设置透明度(0~1)
        self.setWindowOpacity(0.9)
        # 设置鼠标为手状
        self.setCursor(Qt.PointingHandCursor)
        # 设置初始值
        self.speed = 0
        self.cpu = 0
        self.receive_pre = -1
        self.sent_pre = -1
        self.one_line = ''.join(['*' for i in range(40)])
        self.valueChanged.connect(self.updateTextLayOut)
        self.timer = threading.Timer(1, self.update_ui_label)
        self.timer.start()

        self.tempValue={}
    #獲取資料線程
    def update_ui_label(self):
        # 开启独立线程
        update_threading = threading.Thread(target=self.set_labels, daemon=True)
        update_threading.start()
        update_threading.join()
        self.timer = threading.Timer(1, self.update_ui_label)
        if self.ui_alive:
            self.timer.start()

    def set_labels(self):
        #self.set_net_speed()
        self.set_price()


    def updateData(self):
        self.timer.cancel()
        binanceapi.updateList()
        self.loadSetting()
        self.timer = threading.Timer(0.5, self.update_ui_label)
        self.timer.start()
        self.UpdateAll()

    def getCurrencyList(self):
        return self.currencyList


    def UpdateAll(self):
        for item in self.priceLabels:
            item.setText("")
        print("now len:"+str(len(self.currencyList)))
        self.window_height = 20 + 23 * len(self.currencyList)
        self.resize(self.window_width,self.window_height)

    @Slot(int)    # 1漲 0跌 -1fps index-status eg: 1-1 (1號漲)
    def updateTextLayOut(self,status):
        index = int(status.split("-")[0])
        status =  status.split("-")[1]
        if status == "0":
            self.priceLabels[index].setStyleSheet('color: red;')
        elif status=="1":
            self.priceLabels[index].setStyleSheet('color: green;')
        else:
            self.priceLabels[index].setStyleSheet('color: green;')


    def set_price(self):
        _priceList = binanceapi.getPrice()
        index = 0
        for price in _priceList:
            if index < len(self.priceLabels):
                if str(price).split(":")[0] in self.tempValue.keys():  # 本地有該價格資料
                    if self.tempValue[str(price).split(":")[0]] > float(str(price).split(":")[1]):  # 跌
                        self.valueChanged.emit(str(index)+"-0")
                        self.priceLabels[index].setText(str(price) + u" ↘")
                    else:  # 漲
                        self.priceLabels[index].setText(str(price) + u" ↗")
                        self.valueChanged.emit(str(index) + "-1")
                else:
                    self.priceLabels[index].setText(str(price))
                self.tempValue[str(price).split(":")[0]] = float(str(price).split(":")[1])
            index += 1
        self.valueChanged.emit(str(index) + "-1")
        self.priceLabels[index].setText("                    Ping:" + str(binanceapi.getAvgResponseTime()))


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication([])
    screen_width = app.primaryScreen().geometry().width()
    screen_height = app.primaryScreen().geometry().height()

    stats = Stats()
    window_width = stats.geometry().width()
    window_height = stats.geometry().height()
    stats.setGeometry(screen_width - window_width - 10, screen_height//2 - 150, window_width, window_height)
    stats.setStyleSheet(u"background-color: black")
    stats.show()

    sys.exit(app.exec_())

