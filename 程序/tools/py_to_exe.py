import os
name = input()
os.system("pyinstaller -F .\{}.py -w".format(name))