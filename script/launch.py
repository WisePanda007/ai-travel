import sys

sys.path.append("/content/ai-travel/")
import demjson
import os
from utils.xformers import Xformers
from utils.download_model import DownloadModel
from fast_stable_diffusion.dreambooth import DreamBooth
import urllib.request


def main(argv):
    print("开始运行")
    param = demjson.decode_file("ai-travel/config/config_demo.json")

    if len(argv) >= 1:
        param = demjson.decode(urllib.request.urlopen(argv[0]).read())

    print(param)
    training_param = param["data"]["training_params"]
    original_album_param = param["data"]["original_album"]
    original_album_param = [{'url': 'https://community.mafengwo.net/mfs/s19/M00/A1/08/CoNCfmNqCGNX91KiAAAOpAKr1LE.jpeg',
                             'name': 'elonmuskmfwailab'},
                            {'url': 'https://community.mafengwo.net/mfs/s19/M00/FD/07/CoNE4WNqCGNLs833AAATie9uH0I.jpeg',
                             'name': 'elonmuskmfwailab'},
                            {'url': 'https://community.mafengwo.net/mfs/s19/M00/A5/EC/CoNBHGNqCGMC1-f8AAAerrl_Opg.jpeg',
                             'name': 'elonmuskmfwailab'},
                            {'url': 'https://community.mafengwo.net/mfs/s19/M00/F3/FB/CoNBdGNqCGN7sBpeAAAWupoKt_I.jpeg',
                             'name': 'elonmuskmfwailab'},
                            {'url': 'https://community.mafengwo.net/mfs/s19/M00/B0/29/CoNJ72NqCGMxcxtVAAAQ7s0KY-Q.jpeg',
                             'name': 'elonmuskmfwailab'}]


    # 搭建环境
    x = Xformers(training_param)

    # 图片格式转换

    # 选择/下载模型
    d = DownloadModel(training_param)

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
