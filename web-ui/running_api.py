import json
import multiprocessing
import subprocess
import requests
import socket
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
from utils.Logger import logger,post_log



def fun1():
    os.system("python /content/stable-diffusion-webui/webui.py")

def generate_img(rendering_params, painting_id,task_id):
    api = webuiapi.WebUIApi(host='127.0.0.1', port=7861)
    result1 = ()
    if rendering_params["Prompts"] != "":
        result1 = api.txt2img(
            # sd_model=rendering_params["Model_Name"],
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
        image.save(image_dir + str(painting_id)+'_'+str(count)+'.jpg')
        count += 1
    logger.info('saved in dir')
    post_log(task_id,"准备上传图片")

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
        "painting_id": painting_id,
        "images": saveOutputAlbum
    }
    # logger.info(requestData)
    respon = requests.post(saved_url, data=json.dumps(
        requestData), headers=header1)
    logger.info(respon.text)
    logger.info("渲染图片已上传")
    post_log(task_id,"图片上传完成")
    os.system("""rm -f /content/stable-diffusion-webui/result_image/*""")


def downloadModel(models):
    #下载所有需要的模型
    for ckpt_path in models:
        os.system("""mkdir -p /content/models/""")

        cos_path = "sd/models/" + ckpt_path +".ckpt"
        os.system("""coscmd download {} {}""".format(cos_path, "/content/models/"))

def main(argv):
    os.system('echo "0" > /content/ai-travel/web-ui/flag.log')

    param = demjson.decode_file(
        "/content/ai-travel/config/config_demo.json")["data"]
    if len(argv) >= 1:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = urllib.request.Request(url=argv[0], headers=headers)
        param = demjson.decode(urllib.request.urlopen(req).read())["data"]
    task_id=argv[1] if len(argv) >= 2 else "160"


    # 下载需要的模型
    post_log(task_id,"下载需要的模型")
    models = set()
    for rendering_param in param.get("rendering_params"):
        models.add(rendering_param.get("Model_Name"))
    logger.info("Model_Name: "+str(models))
    downloadModel(models)
    post_log(task_id,"模型下载完成")
    rendering_params_list = (param.get("rendering_params"))

    for rendering_params in rendering_params_list:
        # 开始执行渲染任务
        # rendering_params["Model_Name"]=rendering_params["Model_Name"] if rendering_params["Model_Name"] !="" else param["training_params"]["Model_Name"]
        ckptname = rendering_params["Model_Name"]+".ckpt"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1',7861))
        if ckptname not in os.listdir("/content/stable-diffusion-webui/models/Stable-diffusion/") or result!=0:
            pids=subprocess.getstatusoutput("""ps -ef | grep "/content/stable-diffusion-webui/webui.py" | grep -v grep | awk '{print $2}'""")[1].split("\n")
            for pid in pids:
                os.system("kill {}".format(pid))
            os.system("rm -rf /content/stable-diffusion-webui/models/Stable-diffusion/*")
            os.system("""sudo chmod -R 777 /content""")
            os.system("cp /content/models/{} /content/stable-diffusion-webui/models/Stable-diffusion/".format(ckptname))

            logger.info("启动渲染服务，预计{}s ".format(str(30)))
            post_log(task_id,"启动渲染服务")
            process = multiprocessing.Process(target=fun1, args=())
            process.start()
            # time.sleep(sleep_time)
            result,count=1,1
            while result!=0 and count<=60:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('127.0.0.1',7861))
                time.sleep(1)
                count+=1
                logger.info(str(count))
            post_log(task_id,"渲染服务已启动")
        else:
            pass
        logger.info("渲染参数: "+str(rendering_params))
        times=2*int(rendering_params.get("Sampling_Steps"))*int(rendering_params.get("Batch_Count"))*int(rendering_params.get("Width"))*int(rendering_params.get("Height"))/(512*512)
        logger.info("相册id {} 开始渲染，预计{}s".format(rendering_params.get("id"),times))
        post_log(task_id,"相册id {} 开始渲染".format(rendering_params.get("id")))
        process2 = multiprocessing.Process(target=generate_img, args=(rendering_params, param["id"],task_id))
        process2.start()
        process2.join()
        process2.terminate()
        post_log(task_id,"相册id {} 渲染完成".format(rendering_params.get("id")))
        time.sleep(1)
        if process2.exitcode != None and process2.exitcode >0:
            os.system('echo "1" > /content/ai-travel/web-ui/flag.log')
            logger.info("相册id {} 渲染发生错误".format(rendering_params.get("id")))
            post_log(task_id,"相册id {} 渲染发生错误".format(rendering_params.get("id")))
            
        # generate_img(rendering_params, param["id"])

    process.terminate() #经常无法关闭进程
    process2.terminate()
    #所有渲染结束后关闭web-api进程
    pids=subprocess.getstatusoutput("""ps -ef | grep "/content/stable-diffusion-webui/webui.py" | grep -v grep | awk '{print $2}'""")[1].split("\n")
    for pid in pids:
        os.system("kill {}".format(pid))

if __name__ == "__main__":
    main(sys.argv[1:])
