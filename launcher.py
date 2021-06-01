from os import chdir
from pathlib import Path
from sys import path

# PyShare dependencies
import flask

root = Path(__file__).parent.absolute()
chdir(root)

rootstr = str(root)
if not rootstr in path:
    path.append(rootstr)

from PyShare import launch

try: launch()
except KeyboardInterrupt: pass