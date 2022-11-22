import json
import requests
from PIL import Image
import webuiapi
import urllib.request
import demjson
import time
import os
import random
import threading
import sys
sys.path.append("/content/stable-diffusion-webui/")


def web_api():
    os.system("python /content/stable-diffusion-webui/webui.py|tee /content/api.log")


def generate_img(rendering_params, task_id):
    print(rendering_params)
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
    print('saved in dir')

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
            print(image_info['id'])
            image_info["url"] = json_o['data'].get('url')
            print(image_info['url'])
            image_info["style"] = style
            print(image_info['style'])
            saveOutputAlbum.append(image_info)

    print('已获取图片id与url')
    requestData = {
        "painting_id": task_id,
        "images": saveOutputAlbum
    }
    print(requestData)
    respon = requests.post(saved_url, data=json.dumps(
        requestData), headers=header1)
    print(respon.text)
    print("渲染图片已上传")


def downloadModel(models):
    for ckpt_Path in models:
        cos_path = "sd/models/" + \
            ckpt_Path if ckpt_Path[:3] != "sd/" else ckpt_Path
        cos_path = cos_path + \
            ".ckpt" if cos_path.rstrip()[-5] != ".ckpt" else cos_path
        if cos_path.lstrip("sd/models/") in os.listdir("/content/models/"):
            print(ckpt_Path, "已经存在")
        else:
            os.system("""coscmd download {} {}""".format(
                cos_path, "/content/models/"))


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
        models.add(rendering_param.get("CKPT"))
    print(models)
    downloadModel(models)

    rendering_params_list = (param.get("rendering_params"))

    for rendering_params in rendering_params_list:
        # 开始执行渲染任务
        thread1 = threading.Thread(name='t1', target=web_api, args=())

        ckptname = rendering_params["CKPT"].split(
            "/")[-1].rstrip(".ckpt")+".ckpt"
        os.system("""echo "准备开始渲染" |tee /content/api.log""")

        with open('/content/api.log', encoding='utf-8') as file:
            content1 = file.read()
            if ckptname not in content1:
                sleep_time = 150
                print("加载模型{}，等待{}s ".format(ckptname, str(sleep_time)))
                os.system(
                    "rm -rf /content/stable-diffusion-webui/models/Stable-diffusion/*")
                os.system("""sudo chmod -R 777 /content""")
                os.system(
                    "cp /content/models/{} /content/stable-diffusion-webui/models/Stable-diffusion/".format(ckptname))
                thread1.start()
                time.sleep(sleep_time)
            else:
                pass
        print("开始渲染")
        generate_img(rendering_params, param["id"])
    exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])
