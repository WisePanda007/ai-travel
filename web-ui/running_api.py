import random
import threading
import sys
sys.path.append("/content/stable-diffusion-webui/")
import os
import time
import demjson
import urllib.request
import webuiapi
from PIL import Image
import requests
import json

def fun1():
  os.system('python /content/stable-diffusion-webui/webui.py')
  # print('qwe')

def getParamRunningApi():
  argv = sys.argv[1:]
  _id = 0

  _prompt="a red apple"
  _negative_prompt="ugly"
  _styles=[]
  _seed = -1
  _batch_size=1
  _n_iter=1
  _cfg_scale=7
  _width=512
  _height=512
  _restore_faces=False,
  _sampler_index=None,
  _steps=20,
  _sampler_index='DDIM'


  # param = demjson.decode_file("/content/ai-travel/config/config_demo.json")
  if len(argv) >= 1:
    param = demjson.decode(urllib.request.urlopen(argv[0]).read())
    param_data = param.get("data")
    _id = param_data.get("id")

    rendering_params_list = (param_data.get("rendering_params"))
    print("rendering_params")
    for rendering_params in rendering_params_list:
      api = webuiapi.WebUIApi(host='127.0.0.1', port=7861)
      result1 = ()
      if rendering_params["Prompts"] !="":
        result1 = api.txt2img(
          steps = int(rendering_params["Sampling_Steps"]),
          prompt = rendering_params["Prompts"],
          negative_prompt = rendering_params["NegativePrompts"],
          sampler_index = rendering_params["Sampling_Method"],
          restore_faces = True if str(rendering_params['Restore_Faces']).upper()=="TRUE" else False,
          width = int(rendering_params['Width']),
          height = int(rendering_params['Height']),
          n_iter = int(rendering_params['Batch_Count']),
          batch_size = int(rendering_params['Batch_Size']),
          cfg_scale = int(rendering_params['CFG_Scale']),
          seed = random.randint(1,999999) if int(rendering_params['Seed'])==-1 else int(rendering_params['Seed'])
          # styles = rendering_params['Style']
        )
      else:
        print("原Prompts为空使用默认参数:")
        result1 = api.txt2img(prompt="Musk eats an apple",
                      negative_prompt="ugly, out of frame",
                      seed=1003,
                      styles=["anime"],
                      cfg_scale=7,
        )
      image_dir = "/content/stable-diffusion-webui/result_image/"
      count = 0
      for image in result1.images:
        image.save(image_dir + str(_id)+'_'+str(count)+'.jpg')
        count += 1 
      print('saved in dir')

      image_list = os.listdir(image_dir)
      # # 上传接口
      header0 = {'User-agent':'Chrome/76.0.3809.132'}
      upload_url = 'https://www.mafengwo.cn/community/api/ai/upload'

      # 保存图片信息接口
      header1 = {'content-type': 'application/json','User-agent':'Chrome/76.0.3809.132'}
      style = 'test_style'
      saved_url = 'https://www.mafengwo.cn/community/api/ai/saveOutputAlbum'
      painting_id = 2
      saveOutputAlbum = []

      image_info = dict()
      for _image in image_list:
        if '.jpg' in _image:
          image_info = dict()
          files={"file":(_image, open(image_dir+_image,'rb'), "image/jpg")}
          respon = requests.post(upload_url, files=files, headers= header0) 
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
      requestData={
          "painting_id":painting_id,
          "images":saveOutputAlbum
      }
      print(requestData)
      respon = requests.post(saved_url, data=json.dumps(requestData), headers= header1)
      print(respon.text)
      print("渲染图片已上传")

thread1 = threading.Thread(name='t1',target=fun1,args=())
thread2 = threading.Thread(name='t2',target=getParamRunningApi,args=())
thread1.start()   #启动线程1
print("启动中，等待3min ")
time.sleep(180)
thread2.start()   #启动线程2

