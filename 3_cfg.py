import subprocess
import os

def generate_cfg_flowchart(input_path: str, output_path: str):
    subprocess.run(["pycfg", input_path, "-o", output_path], check=True)