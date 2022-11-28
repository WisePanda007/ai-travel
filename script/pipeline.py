import os
import sys
import requests
import json
import time
import urllib.request
import demjson

import logging
logger = logging.getLogger("pipeline") 
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

def run_task(task_id):
    task_time = time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime(time.time()))
    param_url = "https://www.mafengwo.cn/community/api/ai/painting?id={}".format(
        task_id)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=param_url, headers=headers)
    task_type = demjson.decode(urllib.request.urlopen(req).read()).get(
        "data").get("task_type")
    logger.info("任务类型: "+ str(task_type))

    os.system("""mkdir -p /content/logs/train_log/""")
    os.system("""mkdir -p /content/logs/txt2img_log/""")
    os.system("""sudo chmod -R 777 /content""")

    if "TRAIN" in task_type:
        os.chdir("""/content/""")
        logger.info("\n启动训练任务\n")
        logger.info(param_url)
        os.system("""python ./ai-travel/script/train_model.py  {} 2>&1|tee -a -i /content/logs/train_log/train_{}_task{}.log""".format(
            param_url, task_time, task_id))
        logger.info("\n模型训练完成\n")

    if "RENDER" in task_type:
        logger.info("\n启动txt2img任务\n")
        logger.info(param_url)
        os.chdir("""/content/""")
        os.system("""rm -rf /content/stable-diffusion-webui*""")
        os.system(
            """coscmd download -f sd/repository/stable-diffusion-webui.zip /content/stable-diffusion-webui.zip""")
        os.system("""unzip stable-diffusion-webui.zip >/dev/null 2>&1""")
        os.system(
            """mv /content/content/stable-diffusion-webui /content/stable-diffusion-webui""")
        os.system("""rm -rf /content/content""")
        os.system("""mkdir -p /content/stable-diffusion-webui/result_image/""")
        os.system(
            """find /content/Fast-Dreambooth/Sessions -name "*.ckpt" | xargs -i cp -r {} /content/models/""")
        os.system(
            """cp -r /content/ai-travel/web-ui/webuiapi.py /content/stable-diffusion-webui/""")
        os.system(
            """cp -r /content/ai-travel/web-ui/webuiapi_test.py /content/stable-diffusion-webui/""")
        os.system(
            """cp -r /content/ai-travel/web-ui/running_api.py /content/stable-diffusion-webui/""")
        os.system(
            """cp -rf /content/ai-travel/web-ui/webui.py /content/stable-diffusion-webui/webui.py""")
        os.system("""chmod 777 -R /content/stable-diffusion-webui""")
        os.chdir("""/content/stable-diffusion-webui/""")
        os.system("""python running_api.py {} 2>&1|tee -a -i /content/logs/txt2img_log/txt2img_{}_task{}.log""".format(
            param_url, task_time, task_id))

        logger.info("\ntxt2img任务完成\n")
    logger.info("任务完成,任务id: "+str(task_id))


def mian():
    # 获取队列id
    header = {'content-type': 'application/json',
              'User-agent': 'Chrome/76.0.3809.132'}
    url_get_workid = 'https://www.mafengwo.cn/community/api/ai/listNextWorkIds'
    respon = requests.get(headers=header, url=url_get_workid)
    logger.info(respon.text)
    json_respon = json.loads(respon.text)
    queue_id = json_respon.get("data")

    if len(queue_id) == 0:
        logger.info("当前队列无任务,等待下一次查询")
        return 0
    curr_queue_id = queue_id[0]  # 当前id
    logger.info("当前队列id:"+str(curr_queue_id))
    # 根据队列id占有任务id
    time.sleep(1)
    url_use_workid = 'https://www.mafengwo.cn/community/api/ai/occupyWorkById'
    body = {
        "work_id": curr_queue_id
    }
    respon = requests.post(
        url=url_use_workid, data=json.dumps(body), headers=header)
    json_respon = json.loads(respon.text)
    work_id = json_respon.get("data")
    logger.info("根据队列id占有任务id,已占用word_id:"+str(work_id))

    # 开始任务
    run_task(work_id)
    # run_task(6)

    # 释放一个工作ID
    time.sleep(1)
    url_finish_workid = 'https://www.mafengwo.cn/community/api/ai/finishWorkById'
    respon = requests.post(url=url_finish_workid,
                           data=json.dumps(body), headers=header)
    logger.info(respon.text)
    logger.info("已释放队列ID:"+str(curr_queue_id)+",等待下一个任务")


if __name__ == "__main__":
    while True:
        os.chdir("/content/ai-travel/")
        os.system("""git pull origin tencent""")
        os.chdir("/content/")
        mian()
        time.sleep(60)
