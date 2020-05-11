# -*- coding: utf-8 -*-
"""pycmd_Show.

Script to use in Reaper for showing Preset Manager UI

@author:         Philipp Noertersheuser
@GIT Repository: https://github.com/dimentorium/PresetManager
@License
"""
import re
import socket
import pycmd_SendCommand

pycmd_SendCommand.send_command(b'show')
