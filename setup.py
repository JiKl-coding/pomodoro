import sys

from cx_Freeze import setup, Executable
import os

# Get the path of the current script
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Include the image file
included_files = [os.path.abspath("tomato.png"),os.path.abspath("bell sound.wav"), os.path.abspath("settings.txt")]

setup(
    name="Pomodoro App by AkriY",
    version="1.1",
    description="Boost productivity",
    executables=[Executable("pomodoro.py", base=base)],
    options={
        'build_exe': {
            'include_files': included_files
        }
    }
)