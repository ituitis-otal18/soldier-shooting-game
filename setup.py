import os
import sys
from cx_Freeze import setup, Executable


os.environ['TCL_LIBRARY'] = r'D:\Program Files\Python37-32\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'D:\Program Files\Python37-32\tcl\tk8.6'

executables = [Executable("main.py")]

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Apocalypse",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["music.mp3",
                                            "die.wav",
                                            "shoot.wav",
                                            "bg.jpg",
                                            "soldierR.png",
                                            "zombieR.png",
                                            'run1.png',
                                            'run2.png',
                                            'run3.png',
                                            'run4.png',
                                            'medkit.png']}},
    executables=[Executable("main.py", base=base)])

