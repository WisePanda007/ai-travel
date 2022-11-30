import json
import multiprocessing
import subprocess
import requests
from PIL import Image
import webuiapi
import urllib.request
import demjson
import time
import os
import random
import sys
sys.path.append("/content/stable-diffusion-webui/")

sys.path.append("/content/ai-travel/")
from utils.Logger import get_local_logger
logger=get_local_logger()


def fun1():
    os.system("python /content/stable-diffusion-webui/webui.py 2>&1|tee -a -i /content/api.log")



def generate_img(rendering_params, task_id):
    api = webuiapi.WebUIApi(host='127.0.0.1', port=7861)
    result1 = ()
    if rendering_params["Prompts"] != "":
        result1 = api.txt2img(
            steps=int(rendering_params["Sampling_Steps"]),
            prompt=rendering_params["Prompts"],
            negative_prompt=rendering_params["NegativePrompts"],
            sampler_index=rendering_params["Sampling_Method"],
            restore_faces=True if str(
                rendering_params['Restore_Faces']).upper() == "TRUE" else False,
            width=int(rendering_params['Width']),
            height=int(rendering_params['Height']),
            n_iter=int(rendering_params['Batch_Count']),
            batch_size=int(rendering_params['Batch_Size']),
            cfg_scale=int(rendering_params['CFG_Scale']),
            seed=random.randint(1, 999999) if int(
                rendering_params['Seed']) == -1 else int(rendering_params['Seed'])
            # styles = rendering_params['Style']
        )
    else:
        pass
    image_dir = "/content/stable-diffusion-webui/result_image/"
    count = 0
    for image in result1.images:
        image.save(image_dir + str(task_id)+'_'+str(count)+'.jpg')
        count += 1
    logger.info('saved in dir')

    image_list = os.listdir(image_dir)
    # # 上传接口
    header0 = {'User-agent': 'Chrome/76.0.3809.132'}
    upload_url = 'https://www.mafengwo.cn/community/api/ai/upload'

    # 保存图片信息接口
    header1 = {'content-type': 'application/json',
               'User-agent': 'Chrome/76.0.3809.132'}
    style = 'test_style'
    saved_url = 'https://www.mafengwo.cn/community/api/ai/saveOutputAlbum'
    saveOutputAlbum = []

    image_info = dict()
    for _image in image_list:
        if '.jpg' in _image:
            image_info = dict()
            files = {"file": (_image, open(
                image_dir+_image, 'rb'), "image/jpg")}
            respon = requests.post(
                upload_url, files=files, headers=header0)
            json_o = json.loads(respon.text)
            # print(json_o)
            image_info["id"] = json_o['data'].get('id')
            # logger.info(image_info['id'])
            image_info["url"] = json_o['data'].get('url')
            logger.info(image_info['url'])
            image_info["style"] = style
            # logger.info(image_info['style'])
            saveOutputAlbum.append(image_info)

    logger.info('已获取图片id与url')
    requestData = {
        "render_id":rendering_params["id"],
        "painting_id": task_id,
        "images": saveOutputAlbum
    }
    # logger.info(requestData)
    respon = requests.post(saved_url, data=json.dumps(
        requestData), headers=header1)
    logger.info(respon.text)
    logger.info("渲染图片已上传")
    os.system("""rm -f /content/stable-diffusion-webui/result_image/*""")


def downloadModel(models):
    #下载所有需要的模型
    for ckpt_path in models:
        os.system("""mkdir -p /content/models/""")
        if ckpt_path in os.listdir("/content/models/"):
            logger.info(ckpt_path, "已经存在")
        else:
            cos_path = "sd/models/" + ckpt_path +".ckpt"
            os.system("""coscmd download {} {}""".format(cos_path, "/content/models/"))


def main(argv):
    param = demjson.decode_file(
        "/content/ai-travel/config/config_demo.json")["data"]
    if len(argv) >= 1:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = urllib.request.Request(url=argv[0], headers=headers)
        param = demjson.decode(urllib.request.urlopen(req).read())["data"]

    # 下载需要的模型
    models = set()
    for rendering_param in param.get("rendering_params"):
        models.add(rendering_param.get("Model_Name"))
    logger.info("Model_Name: "+str(models))
    downloadModel(models)

    rendering_params_list = (param.get("rendering_params"))

    os.system("""echo "准备开始渲染" |tee /content/api.log""")
    flag = True
    with open('/content/api.log', encoding='utf-8') as file:
        content = file.read()
        for rendering_params in rendering_params_list:
            # 开始执行渲染任务
            # rendering_params["Model_Name"]=rendering_params["Model_Name"] if rendering_params["Model_Name"] !="" else param["training_params"]["Model_Name"]
            ckptname = rendering_params["Model_Name"]+".ckpt"
            sleep_time = 150
            if ckptname not in content and flag:
                flag = False
                #输入ckpt的情况下，如果该模型没有被加载，加载该模型
                logger.info("加载模型{}，预计{}s ".format(ckptname, str(sleep_time)))
                os.system(
                    "rm -rf /content/stable-diffusion-webui/models/Stable-diffusion/*")
                os.system("""sudo chmod -R 777 /content""")
                os.system(
                    "cp /content/models/{} /content/stable-diffusion-webui/models/Stable-diffusion/".format(ckptname))
                process = multiprocessing.Process(target=fun1, args=())
                process.start()
                time.sleep(sleep_time)
            else:
                pass
            logger.info("渲染参数: "+str(rendering_params))
            time1=2*int(rendering_param.get("Sampling_Steps"))*int(rendering_param.get("Batch_Count"))*int(rendering_param.get("Width"))*int(rendering_param.get("Height"))/(512*512)
            logger.info("相册id {} 开始渲染，预计{}s".format(rendering_params.get("id"),time1))
            process2 = multiprocessing.Process(target=generate_img, args=(rendering_params, param["id"]))
            process2.start()
            process2.join()
            process2.terminate()
            time.sleep(2)
            # generate_img(rendering_params, param["id"])
        
    process.terminate() #经常无法关闭进程
    process2.terminate()
    #所有渲染结束后关闭web-api进程
    pids=subprocess.getstatusoutput("""ps -ef | grep "/content/stable-diffusion-webui/webui.py" | grep -v grep | awk '{print $2}'""")[1].split("\n")
    for pid in pids:
        os.system("kill {}".format(pid))

if __name__ == "__main__":
    main(sys.argv[1:])
