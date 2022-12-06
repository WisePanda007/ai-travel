import sys
import os
sys.path.append("/content/ai-travel/")
import urllib.request
from fast_stable_diffusion.dreambooth import DreamBooth
from utils.download_model import DownloadModel
from utils.xformers import Xformers
import demjson
os.environ['MKL_THREADING_LAYER'] = 'GNU'

from utils.Logger import logger

def main(argv):
    # 加载参数
    param = demjson.decode_file("ai-travel/config/config_demo.json")

    if len(argv) >= 1:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = urllib.request.Request(url=argv[0], headers=headers)
        param = demjson.decode(urllib.request.urlopen(req).read())
    task_id=argv[1] if len(argv) >= 2 else 1 

    training_param = param["data"]["training_params"]
    original_album_param = param["data"]["original_album"]
    logger.info("任务id: "+str(param["data"]["id"]))
    logger.info("训练参数: "+ str(training_param))

    # 删除旧模型及数据
    os.system("""sudo chmod -R 777 /content""")
    os.system("""rm -rf /content/Fast-Dreambooth/Sessions""")
    os.system("""rm -rf /content/models""")
    os.system("""rm -rf /content/original_album""")

    # 下载模型
    down=DownloadModel(training_param)

    # 模型训练
    db = DreamBooth(training_param, original_album_param,task_id)


if __name__ == "__main__":
    main(sys.argv[1:])
