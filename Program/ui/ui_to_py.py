import os
name = input()
os.system("pyuic5 -o {0}.py ./{0}.ui".format(name))