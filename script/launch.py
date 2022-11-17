import sys
import os
os.environ['MKL_THREADING_LAYER'] = 'GNU'
sys.path.append("/content/ai-travel/")
import demjson
import torch
from utils.xformers import Xformers
from utils.download_model import DownloadModel
from fast_stable_diffusion.dreambooth import DreamBooth
import urllib.request


def main(argv):
    print("开始运行")
    param = demjson.decode_file("ai-travel/config/config_demo.json")

    if len(argv) >= 1:
        param = demjson.decode(urllib.request.urlopen(argv[0]).read())

    print("打印参数: ",param)
    training_param = param["data"]["training_params"]
    original_album_param=param["data"]["original_album"]

    # 删除旧模型及数据
    os.system("""rm -rf /content/Fast-Dreambooth/Sessions""")
    os.system("""rm -rf /content/models""")
    os.system("""rm -rf /content/original_album""")

    # 模型训练
    db = DreamBooth(training_param, original_album_param)

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
