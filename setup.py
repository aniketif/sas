import sys
from cx_Freeze import setup,Executable

setup(
    name="Any name",
    version="3.1",
    description="Any you like",
    executables =[Executable("set.py",base="Win32GUI")])
