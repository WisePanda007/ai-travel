import webuiapi
from PIL import Image
import os
import requests
import json

# id_name = (os.listdir('/data/ai-test/session/'))[0]
# create API client
api = webuiapi.WebUIApi()

# set host, port
api = webuiapi.WebUIApi(host='127.0.0.1', port=7861)

# # # set default sampler, steps.
api = webuiapi.WebUIApi(sampler='Euler a', steps=20)

result1 = api.txt2img(prompt="cute Sumiyao",
                    negative_prompt="ugly, out of frame",
                    seed=1003,
                    styles=["anime"],
                    cfg_scale=7,
#                      sampler_index='DDIM',
#                      steps=30,
                    )
# images contains the returned images (PIL images)
result1.images
test_path = "/content/stable-diffusion-webui/result_image/"
count = 0
for image in result1.images:
    image.save(test_path + str(count)+ '.jpg')
    count += 1            
print('saved in dir')

# 调用上传接口
# 图片服务器地址
image_dir = '/content/stable-diffusion-webui/result_image/'
image_list = os.listdir(image_dir)

# # 上传接口
header0 = {'User-agent':'Chrome/76.0.3809.132'}
upload_url = 'https://www.mafengwo.cn/community/api/ai/upload'

# 保存图片信息接口
header1 = {'content-type': 'application/json','User-agent': 'Mozilla/5.0'}
style = 'test_style'
saved_url = 'https://www.mafengwo.cn/community/api/ai/saveOutputAlbum'
painting_id = 2
saveOutputAlbum = []

for _image in image_list:
       image_info = dict()
       image_name = os.path.splitext(_image)[0]
       f = open(image_dir+_image,'rb')
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

requestData={
    "painting_id":2,
    "images":saveOutputAlbum
}
print(requestData)
respon = requests.post(saved_url, data=json.dumps(requestData), headers= header1)
print(respon.text)


# result1.info

# info contains paramteres of the api call
# result1.parameters

# result1.imagepython 


