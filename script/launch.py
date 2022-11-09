from utils import install_xformers, downloadModel
import os
import demjson
from stable_diffusion import dreamBooth
import sys
sys.path.append("/content/ai-travel/")


def main(argv):
    print("\n0\n")

    param = demjson.decode_file(argv[0] if len(
        argv) >= 1 else "config/config_demo.json")

    print(param)

    # 搭建环境
    install_xformers()

    # 图片格式转换

    # 选择/下载模型
    downloadModel()

    # 设置DreamBooth
    dreamBooth(param["dream_config"]["Session_Name"], param["dream_config"]["Session_Link_optional"],
               param["dream_config"]["Contains_faces"], param["Huggingface_Token"],
               param["dream_config"]["Remove_existing_instance_images"], param["dream_config"]["IMAGES_FOLDER_OPTIONAL"],
               param["dream_config"]["Crop_images"], param["dream_config"]["Crop_size"])

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
