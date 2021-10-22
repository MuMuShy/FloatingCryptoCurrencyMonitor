import sys
from PySide2.QtWidgets import (
    QWidget, QLineEdit, QLabel, QPushButton, QScrollArea, QMainWindow,
    QApplication, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QCompleter
)
from PySide2.QtCore import Qt

import MyBinanceApi
import DataController

class CurrencyUi_Form(QMainWindow):
    def instance(self):
        return self
    def __init__(self,mainProgram):
        super(CurrencyUi_Form, self).__init__()
        self.mainprogram = mainProgram
        self.controls = QWidget()  # Controls container widget.
        self.controlsLayout = QVBoxLayout()  # Controls container layout.
        self.userChoosedList = DataController.getUserChooseCurrency()
        # List of names, widgets are stored in a dictionary by these keys.
        widget_names = MyBinanceApi.getAll()
        self.widgets = []

        # Iterate the names, creating a new OnOffWidget for
        # each one, adding it to the layout and
        # and storing a reference in the self.widgets dict
        for name in widget_names:

            item = OnOffWidget(name)
            if self.userChoosedList.count(name) >= 1:
                item.updateState(True)
            else:
                item.updateState(False)
            self.controlsLayout.addWidget(item)
            self.widgets.append(item)

        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.controlsLayout.addItem(spacer)
        self.controls.setLayout(self.controlsLayout)

        # Scroll Area Properties.
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.controls)

        # Search bar.
        self.searchbar = QLineEdit()
        self.searchbar.textChanged.connect(self.update_display)

        # Adding Completer.
        self.completer = QCompleter(widget_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)

        self.setStyleSheet("{background-color:red;}")


        # Add the items to VBoxLayout (applied to container widget)
        # which encompasses the whole window.
        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.searchbar)
        containerLayout.addWidget(self.scroll)

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        self.setGeometry(600, 100, 800, 600)
        self.setWindowTitle('Currency Setting')
        self.currencyList = []
        self._want_to_close = False



    def update_display(self, text):

        for widget in self.widgets:
            if text.lower() in widget.name.lower():
                widget.show()
            else:
                widget.hide()

    def closeEvent(self, evnt):
        if self._want_to_close:
            super(CurrencyUi_Form, self).closeEvent(evnt)
        else:
            evnt.ignore()
            self.hide()
            self.mainprogram.updateData()



    def chooseCurrency(self,data):
        print(data)
        self.currencyList = []
        f = open('currencyList.txt', 'r')
        for line in f.readlines():
            self.currencyList.append(line.strip())
        f.close()
        if self.currencyList.count(data) <1:
            self.currencyList.append(data)
        self.currencyList = sorted(self.currencyList,key = str.lower)
        f = open('currencyList.txt', 'w')
        for line in self.currencyList:
            f.write(line+"\n")
        f.close()


    def unChooseCurrency(self,data):
        print(data)
        self.currencyList = []
        f = open('currencyList.txt', 'r')
        for line in f.readlines():
            self.currencyList.append(line.strip())
        f.close()
        if self.currencyList.count(data) >= 1:
            self.currencyList.remove(data)
        self.currencyList = sorted(self.currencyList, key=str.lower)
        f = open('currencyList.txt', 'w')
        for line in self.currencyList:
            f.write(line + "\n")
        f.close()


class OnOffWidget(QWidget):
    def __init__(self, name):
        super(OnOffWidget, self).__init__()

        self.name = name
        self.is_on = False

        self.lbl = QLabel(self.name)
        self.btn_on = QPushButton("Follow")
        self.btn_off = QPushButton("UnFollow")

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.lbl)
        self.hbox.addWidget(self.btn_on)
        self.hbox.addWidget(self.btn_off)

        self.btn_on.clicked.connect(self.on)
        self.btn_off.clicked.connect(self.off)

        self.setLayout(self.hbox)

        self.update_button_state()

    def show(self):
        """
        Show this widget, and all child widgets.
        """
        for w in [self, self.lbl, self.btn_on, self.btn_off]:
            w.setVisible(True)

    def hide(self):
        """
        Hide this widget, and all child widgets.
        """
        for w in [self, self.lbl, self.btn_on, self.btn_off]:
            w.setVisible(False)

    def off(self):
        self.is_on = False
        self.sendUpdate()

    def on(self):
        self.is_on = True
        self.sendUpdate()


    def updateState(self,state):
        self.is_on = state
        self.update_button_state()


    def update_button_state(self):
        """
        Update the appearance of the control buttons (On/Off)
        depending on the current state.
        """
        if self.is_on == True:
            self.btn_on.setStyleSheet("background-color: #4CAF50; color: #fff;")
            self.btn_off.setStyleSheet("background-color: none; color: none;")
        else:
            self.btn_on.setStyleSheet("background-color: none; color: none;")
            self.btn_off.setStyleSheet("background-color: #D32F2F; color: #fff;")



    def sendUpdate(self):
        if self.is_on == True:
            self.btn_on.setStyleSheet("background-color: #4CAF50; color: #fff;")
            self.btn_off.setStyleSheet("background-color: none; color: none;")
            CurrencyUi_Form.chooseCurrency(CurrencyUi_Form,data=self.name)
        else:
            self.btn_on.setStyleSheet("background-color: none; color: none;")
            self.btn_off.setStyleSheet("background-color: #D32F2F; color: #fff;")
            CurrencyUi_Form.unChooseCurrency(CurrencyUi_Form,data=self.name)

