"""Compatibility entry point for the current Notes browser audit."""
from pathlib import Path
import subprocess,sys
if __name__=='__main__':
 raise SystemExit(subprocess.call([sys.executable,str(Path(__file__).with_name('browser-check.py')),'--section','notes',*sys.argv[1:]]))
