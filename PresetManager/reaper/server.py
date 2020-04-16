import socket
import threading
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class server_Signals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data
    
    error
        `tuple` (exctype, value, traceback.format_exc() )
    
    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress 

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    message = pyqtSignal(str)

class reaper_server(QRunnable):
    def __init__(self, *args, **kwargs):
        super(reaper_server, self).__init__()
        self.args = args
        self.kwargs = kwargs

        self.__host = '127.0.0.1'  # Standard loopback interface address (localhost)
        self.__port = 65432        # Port to listen on (non-privileged ports are > 1023)
        self.signals = server_Signals()
        # Add the callback to our kwargs
        self.kwargs['message_callback'] = self.signals.message   

    @pyqtSlot()
    def run(self):
        print("Starting Reaper Com Server")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.__host, self.__port))
            while True:
                #print("Waiting")
                s.listen()
                conn, addr = s.accept()
                with conn:
                    self.__connected = True
                    #print('Connected by', addr)
                    while self.__connected:
                        data = conn.recv(1024)
                        #print(data)
                        if not data:
                            print('Disconnected')
                            self.__connected = False
                        message = data.decode("utf-8")
                        self.signals.message.emit(message)
