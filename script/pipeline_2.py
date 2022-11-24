import os
import sys
import requests
import json

# 获取workid
header = {'content-type': 'application/json', 'User-agent':'Chrome/76.0.3809.132'}
url_get_workid = 'https://www.mafengwo.cn/community/api/ai/listNextWorkIds'
respon = requests.get(headers = header, url = url_get_workid)
print(respon.text)
json_respon = json.loads(respon.text)
word_id = json_respon.get("data")
curr_id = word_id[0]# 当前id 
print("当前id:"+str(curr_id))

# 占有workiid
url_use_workid = 'https://www.mafengwo.cn/community/api/ai/occupyWorkById'
body = {
    "work_id": curr_id
}
respon = requests.post(url = url_use_workid, data=json.dumps(body), headers=header)
print(respon.text)
print("已占用id:"+str(curr_id))

# param_url="https://www.mafengwo.cn/community/api/ai/painting?id={}".format(sys.argv[1])
param_url="https://www.mafengwo.cn/community/api/ai/painting?id="+str(curr_id)

Task_Type="train,txt2img"

os.system("""mkdir -p /content""")
os.system("""sudo chmod -R 777 /content""")

if "train" in Task_Type:
    os.chdir("""/content/""")
    print("\n启动训练任务\n")
    print(param_url)
    os.system("""python ./ai-travel/script/train_model.py {}""".format(param_url))
    print("\n模型训练完成\n")

if "txt2img" in Task_Type:
    print("\n启动txt2img任务\n")
    print(param_url)
    os.chdir("""/content/""")
    os.system("""rm -rf /content/stable-diffusion-webui*""")
    os.system("""coscmd download -f sd/repository/stable-diffusion-webui.zip /content/stable-diffusion-webui.zip""")
    os.system("""unzip stable-diffusion-webui.zip >/dev/null 2>&1""")
    os.system("""mv /content/content/stable-diffusion-webui /content/stable-diffusion-webui""")
    os.system("""rm -rf /content/content""")
    os.system("""mkdir -p /content/stable-diffusion-webui/result_image/""")
    os.system("""find /content/Fast-Dreambooth/Sessions -name "*.ckpt" | xargs -i cp -r {} /content/models/""")
    os.system("""cp -r /content/ai-travel/web-ui/webuiapi.py /content/stable-diffusion-webui/""")
    os.system("""cp -r /content/ai-travel/web-ui/webuiapi_test.py /content/stable-diffusion-webui/""")
    os.system("""cp -r /content/ai-travel/web-ui/running_api.py /content/stable-diffusion-webui/""")
    os.system("""cp -rf /content/ai-travel/web-ui/webui.py /content/stable-diffusion-webui/webui.py""")
    os.system("""chmod 777 -R /content/stable-diffusion-webui""")
    os.chdir("""/content/stable-diffusion-webui/""")
    os.system("""python running_api.py {}""".format(param_url))

    print("\ntxt2img任务完成\n")

# 释放一个工作ID
url_finish_workid = 'https://www.mafengwo.cn/community/api/ai/finishWorkById'
respon = requests.post(url = url_finish_workid, data=json.dumps(body), headers=header)
print(respon.text)
print("已释放id:"+str(curr_id))