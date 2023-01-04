import sys
sys.path.append('E:\\CMU\\thesis\\1127\\scriptsEnv')
import subprocess
from UTool.dirLocation import DirUsr

cmd = 'C:/Users/zxin1/anaconda3/python.exe -i e:/CMU/thesis/1127/scriptsEnv/USimulation/glareRenderer.py'

subprocess.call(cmd,
                shell = True,
                executable = DirUsr.CMD
                )