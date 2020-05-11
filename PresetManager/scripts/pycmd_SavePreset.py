# -*- coding: utf-8 -*-
"""pycmd_SavePreset.

Script to use in Reaper for Saving the preset of the currently selected track

@author:         Philipp Noertersheuser
@GIT Repository: https://github.com/dimentorium/PresetManager
@License
"""
import re
import socket
import pycmd_SendCommand

pycmd_SendCommand.send_command(b'save_preset')
