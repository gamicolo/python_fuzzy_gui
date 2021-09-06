#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
from graph_gui import GraphClass

class MainClass(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainClass, self).__init__(*args, **kwargs)

        uic.loadUi('fuzzy_gui_main.ui', self)
        self.setWindowTitle('Fuzzy Controller User Interface')
        self.status_graph_window = None
        self.ui_components()

    def ui_components(self):

        self.dial_set_point.setRange(25,60)
        self.set_point = 25
        self.lcd_set_point.display(25)
        self.dial_set_point.valueChanged.connect(self.update_display)
        self.btn_start.clicked.connect(self.update_reference)

    def update_reference(self):

        if self.status_graph_window is None:
            self.status_graph_window = GraphClass(self.set_point)
            right_side = QtWidgets.QApplication.desktop().availableGeometry().topRight()
            self.status_graph_window.move(right_side)
            self.status_graph_window.show()
            #self.status_graph_window.msg.connect(self.close_graph_window) --> not working
        else:
            self.status_graph_window.update_reference(self.set_point)
        self.btn_start.setText('Update')

    def update_display(self):
        
        self.set_point = self.dial_set_point.value()
        self.lcd_set_point.display(self.set_point)

    #def close_graph_window(self,data):
    #    
    #    self.status_graph_window = None --> working but a core dumped is generated

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainClass()
    main.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    main()
