import serial
import time
from PyQt5.QtCore import pyqtSignal,QThread

class SerialThreadClass(QThread):
    s_msg=pyqtSignal(str)

    def __init__(self,set_point,parent=None):
        super(SerialThreadClass,self).__init__(parent)

        self.serialPort=serial.Serial()
        self.serialPort.baudrate=9600
        self.serialPort.port='/dev/ttyACM0'
        self.serialPort.open()

        self.set_point = set_point
        if self.serialPort.isOpen():
            time.sleep(2)
            self.send_serial(self.set_point)

        #TODO: agregar un ciclo por si no esta el puerto ttyACM0 abierto
        #print("the status of the port opened is: " + str(self.serialPort.isOpen()))

    def set_r_temp(self, reference):
        self.set_point = reference

    def send_upd_reference(self, r_temp):
        self.set_point = r_temp
        self.send_serial(self.set_point)


    def run(self):
        while True:
            serial_data=self.serialPort.readline()
            #print(serial_data.decode('utf-8'))
            self.s_msg.emit(serial_data.decode('utf-8'))

    def stop_serial(self):
        #print('stoping serial thread class')
        self.terminate()

    def send_serial(self,set_point):
        self.serialPort.write(bytes('<' + str(set_point) + '>','utf-8'))
