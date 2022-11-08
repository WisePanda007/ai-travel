import sys
sys.path.append("/content/ai-travel/")
from utils import install_xformers
import demjson
import os



def main(argv):
    print("0")

    param = demjson.decode_file(argv[0] if len(argv) >= 1 else "config/config_demo.json")

    print("1")

    #搭建环境
    install_xformers()

    #图片格式转换

    #模型训练

    #生成图片

    #web页面
    print("成功运行")
if __name__=="__main__":
    main()
