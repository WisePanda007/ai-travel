import sys
sys.path.append("/content/ai-travel/")
from utils import install_xformers
import demjson
import os



def main(argv):
    print("\n0\n")

    param = demjson.decode_file(argv[0] if len(argv) >= 1 else "config/config_demo.json")

    print("\n1\n")

    #搭建环境
    install_xformers()

    #图片格式转换

    #模型训练

    #生成图片

    #web页面
    print("\n成功运行\n")
if __name__=="__main__":
    try:
        main(sys.argv[1:])
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)
