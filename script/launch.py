import os
import sys
sys.path.append("/content/ai-travel/")
import demjson
from utils import install_xformers


def main(argv):
    param = demjson.decode_file(argv[0] if len(argv) >= 1 else "config/config_demo.json")

    #搭建环境
    os.system("sh utils/env/environment.sh")
    install_xformers()

    #图片格式转换

    #模型训练

    #生成图片

    #web页面

if name=="__main__":
    main()
