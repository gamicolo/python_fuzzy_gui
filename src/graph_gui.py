#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSignal
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
from serial_reading import SerialThreadClass

class GraphClass(QtWidgets.QMainWindow):

    msg=pyqtSignal(str)

    def __init__(self, set_point, parent=None):
        super(GraphClass, self).__init__(parent)

        uic.loadUi('fuzzy.ui', self)
        self.setWindowTitle('Fuzzy Controller Status Interface')

        self.r_temp = set_point
        self.current_temp = [0]
        self.ref_temp = [0]
        self.samples = [0]
        self.inc = 0

        styles = {'color':'#939393','font-size':'25px'}
        self.graphWidget.setLabel('left', 'Temperature (°C)', **styles)
        self.graphWidget.setLabel('bottom', 'Samples', **styles)
        self.graphWidget.addLegend()
        self.graphWidget.showGrid(x=True,y=True)

        self.data_rtemp_line = self.graphWidget.plot(self.samples,self.ref_temp, name='ref_temp')
        self.data_ctemp_line = self.graphWidget.plot(self.samples,self.current_temp, name='current_temp')

        self.thr_serial=SerialThreadClass(self.r_temp)
        self.thr_serial.s_msg.connect(self.print_arduino_data)
        self.thr_serial.start()

    def update_reference(self, r_temp):

        self.r_temp = r_temp
        self.thr_serial.send_upd_reference(self.r_temp)

    def print_arduino_data(self, arduinoTemp):

        self.inc = self.inc + 1
        data = arduinoTemp.split(',')
        data_len = len(data)
        if len(data)==14:
            self.lcd_err_neg.display(float(data[0]))
            self.lcd_err_zero.display(float(data[1]))
            self.lcd_err_pos.display(float(data[2]))
            self.lcd_derr_neg.display(float(data[3]))
            self.lcd_derr_zero.display(float(data[4]))
            self.lcd_derr_pos.display(float(data[5]))
            self.lcd_out_neg.display(float(data[6]))
            self.lcd_out_zero.display(float(data[7]))
            self.lcd_out_pos.display(float(data[8]))

            self.lcd_integral_out.display(float(data[9]))
            self.lcd_out.display(float(data[10]))
            self.lcd_err.display(float(data[13]))

            self.ref_temp.append(float(data[11]))
            self.current_temp.append(float(data[12]))
            self.samples.append(self.inc)

        self.update_plot_data()

    def update_plot_data(self):

        ref_len = len(self.ref_temp)
        cur_len = len(self.current_temp)
        samples_len = len(self.samples)

        if (ref_len != cur_len != samples_len):
            min_data_len = min(ref_len, cur_len, samples_len)

            self.ref_temp = self.ref_temp[:min_data_len]
            self.current_temp = self.current_temp[:min_data_len]
            self.samples = self.samples[:min_data_len]

        self.data_rtemp_line.setData(self.samples,self.ref_temp)
        self.data_ctemp_line.setData(self.samples,self.current_temp, pen = pg.mkPen(color='r'))

    def closeEvent(self, event):
        self.thr_serial.stop_serial()
        #self.msg.emit('closed')-->not working

