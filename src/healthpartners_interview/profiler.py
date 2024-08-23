import subprocess
import sys
import os

def run_profiler():
    pyinstrument_path = r"C:\Users\edmun\AppData\Local\Programs\Python\Python313\Scripts\pyinstrument.exe"
    script_path = os.path.join(os.path.dirname(__file__), "__init__.py")

    cmd = [
        pyinstrument_path,
        "-r", "speedscope",
        "-o", "OUTFILE",
        script_path
    ]

    subprocess.run(cmd, check=True)