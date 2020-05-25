# PresetManager
Preset Manager for REAPER for loading and saving VSTi Presets with tagging and search.
![Demo Video](/documentation/200422_demo.gif)



# Installation (Windows)
1. Install Python (currently working with 3.7.6) https://www.python.org/downloads/release/python-376/
1. Select Python Environment in Reaper (Options => Preferences => Reascript)
    Folder: C:\Users\<USER>\AppData\Local\Programs\Python\Python37
    DLL: python37.dll
    
![Reaper Python Preferences](/documentation/reaper_setting.png)
1. Install reapy => pip install python-reapy https://python-reapy.readthedocs.io/en/latest/install_guide.html
1. Install RPP => pip install rpp https://github.com/Perlence/rpp
1. Install playsound => pip install playsound
1. install xmltodict => pip install xmltodict
1. install pyogg => pip install pyogg
1. install pyopenal => pip install pyopenal
1. install Messagepack => pip install msgpack
1. Enable reapy Distant API in Reaper
    Script Path: C:\Users\<USER>\AppData\Local\Programs\Python\Python37\Lib\site-packages\reapy\reascripts
    
Run PresetManager.py
   
Alternative, use requirements.txt file in repository by executing the following command in the folder:
pip install -r requirements.txt
    
