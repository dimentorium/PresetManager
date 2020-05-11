# -*- coding: utf-8 -*-
"""pycmd_SendCommand.

Base Script for sending commands to the Preset Manager Server

@author:         Philipp Noertersheuser
@GIT Repository: https://github.com/dimentorium/PresetManager
@License
"""
import re
import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def send_command(command: bytes):
    """Send commad via Socket to Preset Manager

    Arguments:
        command {bytes} -- bytes string that is sended to the Preset Manager
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as pm_socket:
        pm_socket.connect((HOST, PORT))
        pm_socket.sendall(command)
