"""Compatibility entry point; current browser checks include every title surface."""
from pathlib import Path
import subprocess,sys
if __name__=='__main__':
 raise SystemExit(subprocess.call([sys.executable,str(Path(__file__).with_name('browser-check.py')),*sys.argv[1:]]))
