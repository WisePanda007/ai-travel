mkdir -p /content/
cd /content/
mkdir -p /content/Fast-Dreambooth/Regularization_images
coscmd download -r sd/repository/Regularization_images/ /content/Fast-Dreambooth/Regularization_images/  >/dev/null 2>&1
mkdir -p /content/diffusers
coscmd download -r sd/repository/diffusers/ /content/diffusers/ >/dev/null 2>&1

conda activate sd
chmod -R 777 /content/
rm -rf ai-travel
git clone -b tencent https://github.com/WisePanda007/ai-travel.git
nohup python -u /content/ai-travel/script/pipeline.py >>logs/task.log 2>&1 &