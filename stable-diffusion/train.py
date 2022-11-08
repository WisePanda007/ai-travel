import os
import time
from IPython.display import clear_output
from IPython.utils import capture

#@markdown - Skip this cell if you are loading a previous session

#@markdown ---

with capture.capture_output() as cap: 
  os.system("cd /content/")

Huggingface_Token = "" #@param {type:"string"}
token=Huggingface_Token

#@markdown - Download the original v1.5 model.

#@markdown (Make sure you've accepted the terms in https://huggingface.co/runwayml/stable-diffusion-v1-5)

#@markdown ---

Path_to_HuggingFace= "nitrosocke/redshift-diffusion" #@param {type:"string"}

#@markdown - Load and finetune a model from Hugging Face, use the format "profile/model" like : runwayml/stable-diffusion-v1-5

#@markdown Or

CKPT_Path = "" #@param {type:"string"}

#@markdown Or

CKPT_Link = "" #@param {type:"string"}

#@markdown - A CKPT direct link, huggingface CKPT link or a shared CKPT from gdrive.
#@markdown ---

Compatiblity_Mode="" #@param {type:"boolean"}
#@markdown - Enable only if you're getting conversion errors.


def downloadmodel():
  token=Huggingface_Token
  if token=="":
      token=input("Insert your huggingface token :")
  if os.path.exists('/content/stable-diffusion-v1-5'):
    !rm -r /content/stable-diffusion-v1-5
  clear_output()

  %cd /content/
  clear_output()
  !mkdir /content/stable-diffusion-v1-5
  %cd /content/stable-diffusion-v1-5
  !git init
  !git lfs install --system --skip-repo
  !git remote add -f origin  "https://USER:{token}@huggingface.co/runwayml/stable-diffusion-v1-5"
  !git config core.sparsecheckout true
  !echo -e "feature_extractor\nsafety_checker\nscheduler\ntext_encoder\ntokenizer\nunet\nmodel_index.json" > .git/info/sparse-checkout
  !git pull origin main
  if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
    !git clone "https://USER:{token}@huggingface.co/stabilityai/sd-vae-ft-mse"
    !mv /content/stable-diffusion-v1-5/sd-vae-ft-mse /content/stable-diffusion-v1-5/vae
    !rm -r /content/stable-diffusion-v1-5/.git
    !sed -i 's@"clip_sample": false@@g' /content/stable-diffusion-v1-5/scheduler/scheduler_config.json
    !sed -i 's@"trained_betas": null,@"trained_betas": null@g' /content/stable-diffusion-v1-5/scheduler/scheduler_config.json
    !sed -i 's@"sample_size": 256,@"sample_size": 512,@g' /content/stable-diffusion-v1-5/vae/config.json    
    %cd /content/    
    clear_output()
    print('[1;32mDONE !')
  else:
    while not os.path.exists('/content/stable-diffusion-v1-5'):
         print('[1;31mMake sure you accepted the terms in https://huggingface.co/runwayml/stable-diffusion-v1-5')
         time.sleep(5)

def downloadmodel_hf():
  if os.path.exists('/content/stable-diffusion-v1-5'):
    !rm -r /content/stable-diffusion-v1-5
  clear_output()

  %cd /content/
  clear_output()
  !mkdir /content/stable-diffusion-v1-5
  %cd /content/stable-diffusion-v1-5
  !git init
  !git lfs install --system --skip-repo
  !git remote add -f origin  "https://USER:{token}@huggingface.co/{Path_to_HuggingFace}"
  !git config core.sparsecheckout true
  !echo -e "feature_extractor\nsafety_checker\nscheduler\ntext_encoder\ntokenizer\nunet\nmodel_index.json" > .git/info/sparse-checkout
  !git pull origin main
  if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
    !git clone "https://USER:{token}@huggingface.co/stabilityai/sd-vae-ft-mse"
    !mv /content/stable-diffusion-v1-5/sd-vae-ft-mse /content/stable-diffusion-v1-5/vae
    !rm -r /content/stable-diffusion-v1-5/.git
    !sed -i 's@"clip_sample": false@@g' /content/stable-diffusion-v1-5/scheduler/scheduler_config.json
    !sed -i 's@"trained_betas": null,@"trained_betas": null@g' /content/stable-diffusion-v1-5/scheduler/scheduler_config.json
    !sed -i 's@"sample_size": 256,@"sample_size": 512,@g' /content/stable-diffusion-v1-5/vae/config.json    
    %cd /content/    
    clear_output()
    print('[1;32mDONE !')
  else:
    while not os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
         print('[1;31mCheck the link you provided')
         time.sleep(5)

if Path_to_HuggingFace != "":
  downloadmodel_hf()

elif CKPT_Path !="":
  if os.path.exists('/content/stable-diffusion-v1-5'):
    !rm -r /content/stable-diffusion-v1-5
  if os.path.exists(str(CKPT_Path)):
    !mkdir /content/stable-diffusion-v1-5
    with capture.capture_output() as cap:
      if Compatiblity_Mode:
        !wget https://raw.githubusercontent.com/huggingface/diffusers/039958eae55ff0700cfb42a7e72739575ab341f1/scripts/convert_original_stable_diffusion_to_diffusers.py
        !python /content/convert_original_stable_diffusion_to_diffusers.py --checkpoint_path "$CKPT_Path" --dump_path /content/stable-diffusion-v1-5
        !rm /content/convert_original_stable_diffusion_to_diffusers.py
      else:           
        !python /content/diffusers/scripts/convert_original_stable_diffusion_to_diffusers.py --checkpoint_path "$CKPT_Path" --dump_path /content/stable-diffusion-v1-5        
    if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
      !rm /content/v1-inference.yaml
      clear_output()
      print('[1;32mDONE !')
    else:
      !rm /content/convert_original_stable_diffusion_to_diffusers.py
      !rm /content/v1-inference.yaml
      !rm -r /content/stable-diffusion-v1-5
      while not os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
        print('[1;31mConversion error, Insufficient RAM or corrupt CKPT, use a 4.7GB CKPT instead of 7GB')
        time.sleep(5)
  else:
    while not os.path.exists(str(CKPT_Path)):
       print('[1;31mWrong path, use the colab file explorer to copy the path')
       time.sleep(5)


elif CKPT_Link !="":   
    if os.path.exists('/content/stable-diffusion-v1-5'):
      !rm -r /content/stable-diffusion-v1-5     
    !gdown --fuzzy $CKPT_Link -O model.ckpt    
    if os.path.exists('/content/model.ckpt'):
      if os.path.getsize("/content/model.ckpt") > 1810671599:
        !mkdir /content/stable-diffusion-v1-5
        with capture.capture_output() as cap: 
          if Compatiblity_Mode:
            !wget https://raw.githubusercontent.com/huggingface/diffusers/039958eae55ff0700cfb42a7e72739575ab341f1/scripts/convert_original_stable_diffusion_to_diffusers.py
            !python /content/convert_original_stable_diffusion_to_diffusers.py --checkpoint_path /content/model.ckpt --dump_path /content/stable-diffusion-v1-5
            !rm /content/convert_original_stable_diffusion_to_diffusers.py            
          else:           
            !python /content/diffusers/scripts/convert_original_stable_diffusion_to_diffusers.py --checkpoint_path /content/model.ckpt --dump_path /content/stable-diffusion-v1-5
        if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
          clear_output()
          print('[1;32mDONE !')
          !rm /content/v1-inference.yaml
          !rm /content/model.ckpt
        else:
          if os.path.exists('/content/v1-inference.yaml'):
            !rm /content/v1-inference.yaml
          !rm /content/convert_original_stable_diffusion_to_diffusers.py
          !rm -r /content/stable-diffusion-v1-5
          !rm /content/model.ckpt
          while not os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
            print('[1;31mConversion error, Insufficient RAM or corrupt CKPT, use a 4.7GB CKPT instead of 7GB')
            time.sleep(5)
      else:
        while os.path.getsize('/content/model.ckpt') < 1810671599:
           print('[1;31mWrong link, check that the link is valid')
           time.sleep(5)
else:
  downloadmodel()