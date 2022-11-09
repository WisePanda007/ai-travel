from subprocess import getoutput
from IPython.display import clear_output
import time
import os

def install_xformers():
    s = getoutput('nvidia-smi')
    if 'T4' in s:
        gpu = 'T4'
    elif 'P100' in s:
        gpu = 'P100'
    elif 'V100' in s:
        gpu = 'V100'
    print("GPU版本:"+gpu)

    while True:
        try:
            gpu == 'T4' or gpu == 'P100' or gpu == 'V100' or gpu == 'A100'
            break
        except:
            pass
        print('[1;31mit seems that your GPU is not supported at the moment')
        time.sleep(5)

    if (gpu == 'T4'):
        os.system(
            """pip install -q https://github.com/TheLastBen/fast-stable-diffusion/raw/main/precompiled/T4/xformers-0.0.13.dev0-py3-none-any.whl""")

    elif (gpu == 'P100'):
        os.system(
            """pip install -q https://github.com/TheLastBen/fast-stable-diffusion/raw/main/precompiled/P100/xformers-0.0.13.dev0-py3-none-any.whl""")

    elif (gpu == 'V100'):
        os.system(
            """pip install -q https://github.com/TheLastBen/fast-stable-diffusion/raw/main/precompiled/V100/xformers-0.0.13.dev0-py3-none-any.whl""")

    print('[1;32mDONE !')
