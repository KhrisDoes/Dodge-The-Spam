#!/usr/bin/env python
import sys
from cx_Freeze import setup, Executable
import os




core_path = os.path.dirname(os.path.realpath(__file__))


folders_path = os.path.normpath(core_path + os.sep + os.pardir )
resources_dir = os.path.join(folders_path, "resources")



# Dependencies are automatically detected, but it might need fine tuning.
packages = ["os", "pygame", "random"]
excludes = ["tkinter"]
includes = []
#include_files = ["../resources/player_icon.png", "../resources/spam.png"]

# build_exe_options = {'includes':includes,'excludes':excludes,'packages':packages,'include_files':include_files}

build_exe_options = {'includes':includes,'excludes':excludes,'packages':packages}


# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Dodge The Spam",
        version = "0.1",
        description = "Mini arcade game!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])



def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        # Change this bit to match where you store your data files:
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)
