# -*- coding: utf-8 -*-
"""Server module.

Small TCP IP server to receive commands from Reaper

Classes:
    reaper_server: simple TCP/IP server

Functions

Todo:
    * implement functions

@author:         Philipp Noertersheuser
@GIT Repository: https://github.com/dimentorium/PresetManager
@License
"""
from reaper.preset import reaper_preset_chunk
import socket
import threading
import logging
import queue
from core import actions

rs = None

def start(command_queue: queue.Queue):
    global rs
    rs = reaper_server(command_queue)


class reaper_server():
    """reaper_server.

    TCP/IP server waiting for commands from Reaper

    Methods
    -------
        init: init class
        run: start server and wait for messages

    Properties
    ----------
        host: host address
        port: TCP port to listen
    """

    def __init__(self, command_queue: queue.Queue):
        """Init.

        Set TCP settings in class
        """
        logging.debug("Server started")
        # Standard loopback interface address (localhost)
        self.__host = '127.0.0.1' 
        # Port to listen on (non-privileged ports are > 1023) 
        self.__port = 65432 
        self.__command_queue = command_queue

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        """Run.

        Run server
        """
        logging.debug("Starting Reaper Com Server")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.__host, self.__port))
            while True:
                logging.debug("Waiting")
                s.listen()
                conn, addr = s.accept()
                with conn:
                    self.__connected = True
                    logging.debug('Connected by' + str(addr))
                    while self.__connected:
                        data = conn.recv(1024)
                        logging.debug("Received Command: " + str(data))
                        if not data:
                            logging.debug('Disconnected')
                            self.__connected = False
                        message = data.decode("utf-8")
                        #implement function calls
                        self.__command_queue.put(message)
