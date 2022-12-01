import os
import sys
import requests
import json
import time
import urllib.request
import demjson
sys.path.append("/content/ai-travel/")
from utils.Logger import get_local_logger,get_eth0_ip
from utils.alarm import sendMail
from utils.git_timeout import update_git_ai_travel
logger=get_local_logger()

def run_task(task_id):

    flag=0 #标记任务成功/失败,flag=0成功

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
        logger.info("启动训练任务")
        logger.info(param_url)
        flag=os.system("""python ./ai-travel/script/train_model.py  {} 2>&1|tee -a -i /content/logs/train_log/train_{}_task{}.log""".format(
            param_url, task_time, task_id))
        if flag==0:
            logger.info("模型训练完成")
        else:
            logger.error("模型训练失败")
            return flag

    if "RENDER" in task_type:
        logger.info("启动txt2img任务")
        logger.info(param_url)
        os.chdir("""/content/""")

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
        flag=os.system("""python running_api.py {} 2>&1|tee -a -i /content/logs/txt2img_log/txt2img_{}_task{}.log""".format(
            param_url, task_time, task_id))
        if flag==0:
            logger.info("txt2img任务完成")
        else:
            logger.error("txt2img任务失败")
            return flag
    logger.info("任务完成,任务id: "+str(task_id))
    return flag


def mian():
    flag=0 #标记任务成功/失败,flag=0成功
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
        return flag
    curr_queue_id = queue_id[0]  # 当前id
    logger.info("当前队列id:"+str(curr_queue_id))
    # 根据队列id占有任务id
    # time.sleep(1)
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
    try:
        flag=run_task(work_id)
    except Exception as e:
        logger.error(e)
        flag=-1

    # 释放一个工作ID
    time.sleep(1)
    url_finish_workid = 'https://www.mafengwo.cn/community/api/ai/finishWorkById'
    respon = requests.post(url=url_finish_workid,
                           data=json.dumps(body), headers=header)
    logger.info(respon.text)
    logger.info("已释放队列ID:"+str(curr_queue_id)+",等待下一个任务")
    return flag


if __name__ == "__main__":
    logger.info("启动pipeline")
    os.chdir("/content/")
    #下载依赖
    os.system("""pip install func_timeout""")
    os.system("""mkdir -p /content/Fast-Dreambooth/Regularization_images""")
    os.system("""coscmd download -r sd/repository/Regularization_images/ /content/Fast-Dreambooth/Regularization_images/  >/dev/null 2>&1""")
    os.system("""mkdir -p /content/diffusers""")
    os.system("""coscmd download -r sd/repository/diffusers/ /content/diffusers/ >/dev/null 2>&1""")

    #下载基础模型v1.5
    os.system("""rm -rf /content/stable-diffusion-v1-5*""")
    os.system("""coscmd download -f sd/models/stable-diffusion-v1-5.zip /content/stable-diffusion-v1-5.zip""")
    os.system("""unzip /content/stable-diffusion-v1-5.zip > /dev/null 2>&1""")
    os.system("""mv -f /content/content/stable-diffusion-v1-5 /content/stable-diffusion-v1-5""")
    os.system("""rm -rf /content/content""")

    #下载webui代码
    os.system("""rm -rf /content/stable-diffusion-webui*""")
    os.system(
        """coscmd download -f sd/repository/stable-diffusion-webui.zip /content/stable-diffusion-webui.zip""")
    os.system("""unzip stable-diffusion-webui.zip >/dev/null 2>&1""")
    os.system(
        """mv /content/content/stable-diffusion-webui /content/stable-diffusion-webui""")
    os.system("""rm -rf /content/content""")

    while True: 
        #更新git代码
        try:
            update_git_ai_travel()
        except Exception as e:
            logger.warning(str(get_eth0_ip())+"无法连接git")

        try:
            os.chdir("/content/")
            flag=mian()
            if flag!=0:
                sendMail([get_eth0_ip(),"check task"])
        except Exception as e:
            logger.error(e)
            sendMail([get_eth0_ip(),e])
        time.sleep(60)

        #run_task(6)
# nohup python -u /content/ai-travel/script/pipeline.py >logs/task.log 2>&1 &
