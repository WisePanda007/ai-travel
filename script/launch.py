import sys
sys.path.append("/content/ai-travel/")
import demjson
import os
from utils.xformers import Xformers
from utils.download_model import DownloadModel


def main(argv):
    print("开始运行")

    param = demjson.decode_file(argv[0] if len(
        argv) >= 1 else "ai-travel/config/config_demo.json")

    print(param)

    # 搭建环境
    x = Xformers(param)

    # 图片格式转换

    # 选择/下载模型
    d=DownloadModel(param)

    # # 设置DreamBooth
    # dreamBooth(param["dream_config"]["Session_Name"], param["dream_config"]["Session_Link_optional"],
    #            param["dream_config"]["Contains_faces"], param["Huggingface_Token"],
    #            param["dream_config"]["Remove_existing_instance_images"], param["dream_config"]["IMAGES_FOLDER_OPTIONAL"],
    #            param["dream_config"]["Crop_images"], param["dream_config"]["Crop_size"])

    # 模型训练

    # 生成图片

    # web页面
    print("\n成功运行\n")


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(1)
