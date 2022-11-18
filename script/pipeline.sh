param_url="https://www.mafengwo.cn/community/api/ai/painting?id=$1"

echo "开始渲染"
echo $param_url
rm -rf /content/stable-diffusion-webui/models/Stable-diffusion/*
rm -rf /content/stable-diffusion-webui/result_image/*
mkdir -p /content/stable-diffusion-webui/result_image/
find /content/Fast-Dreambooth/Sessions -name "*.ckpt" | xargs -i cp -r {} /content/stable-diffusion-webui/models/Stable-diffusion/
# param_id
cp -r /content/ai-travel/web-ui/webuiapi.py /content/stable-diffusion-webui/
cp -r /content/ai-travel/web-ui/webuiapi_test.py /content/stable-diffusion-webui/
cp -r /content/ai-travel/web-ui/running_api.py /content/stable-diffusion-webui/
cp -rf /content/ai-travel/web-ui/webui.py /content/stable-diffusion-webui/webui.py

chmod 777 -R /content/stable-diffusion-webui
cd /content/stable-diffusion-webui/
echo "完成渲染基本环境搭建"
python running_api.py $param_url