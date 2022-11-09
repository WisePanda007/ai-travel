#@markdown ---
#@markdown #Start DreamBooth
#@markdown ---
import os
from subprocess import getoutput
from IPython.display import HTML
from IPython.display import clear_output
import random

Resume_Training = False #@param {type:"boolean"}

if not Resume_Training and not os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
  if os.path.exists('/content/stable-diffusion-v1-5'):
    os.system("""rm -r '/content/stable-diffusion-v1-5'""")
  print('[1;31mOriginal model not found, downloading....[0m')
  fdownloadmodel()
  if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
     print('[1;32mModel downloaded, proceeding to training...')
  else:
     print('[1;31mError downloading the model, make sure you have accepted the terms at https://huggingface.co/runwayml/stable-diffusion-v1-5')  

#@markdown  - If you're not satisfied with the result, check this box, run again the cell and it will continue training the current model.

MODELT_NAME=MODEL_NAME

Training_Steps=1000 #@param{type: 'number'}
#@markdown - Total Steps = Number of Instance images * 200, if you use 30 images, use 6000 steps, if you're not satisfied with the result, resume training for another 500 steps, and so on ...

Seed='' #@param{type: 'string'}

if Seed =='' or Seed=='0':
  Seed=random.randint(1, 999999)
else:
  Seed=int(Seed)

#@markdown - Leave empty for a random seed.

fp16 = True
if fp16:
  prec="fp16"
else:
  prec="no"

s = getoutput('nvidia-smi')
if 'A100' in s:
  precision="no"
else:
  precision=prec

try:
   resume
   if resume and not Resume_Training:
     print('[1;31mOverwrite your previously trained model ?, answering "yes" will train a new model, answering "no" will resume the training of the previous model?  yes or no ?[0m')
     while True:
        ansres=input('')
        if ansres=='no':
          Resume_Training = True
          del ansres
          break
        elif ansres=='yes':
          Resume_Training = False
          resume= False
          break
except:
  pass

if Resume_Training and os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
  MODELT_NAME=OUTPUT_DIR
  print('[1;32mResuming Training...[0m')
elif Resume_Training and not os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
  print('[1;31mPrevious model not found, training a new model...[0m') 
  MODELT_NAME=MODEL_NAME

#@markdown ---------------------------

try:
   Contain_f
   pass
except:
   Contain_f=Contains_faces

Enable_text_encoder_training= True #@param{type: 'boolean'}

#@markdown - At least 10% of the total training steps are needed, it doesn't matter if they are at the beginning or in the middle or the end, in case you're training the model multiple times.
#@markdown - For example you can devide 5%, 5%, 5% on 3 training runs on the model, or 0%, 0%, 15%, given that 15% will cover the total training steps count (15% of 200 steps is not enough).

#@markdown - Enter the % of the total steps for which to train the text_encoder
Train_text_encoder_for=35 #@param{type: 'number'}

#@markdown - Keep the % low for better style transfer, more training steps will be necessary for good results.
#@markdown - Higher % will give more weight to the instance, it gives stronger results at lower steps count, but harder to stylize, 

if Train_text_encoder_for>=100:
  stptxt=Training_Steps
elif Train_text_encoder_for==0:
  Enable_text_encoder_training= False
  stptxt=10
else:
  stptxt=int((Training_Steps*Train_text_encoder_for)/100)

if not Enable_text_encoder_training:
  Contains_faces="No"
else:
   Contains_faces=Contain_f

if Enable_text_encoder_training:
  Textenc="--train_text_encoder"
else:
  Textenc=""

#@markdown ---------------------------
Save_Checkpoint_Every_n_Steps = False #@param {type:"boolean"}
Save_Checkpoint_Every=500 #@param{type: 'number'}
if Save_Checkpoint_Every==None:
  Save_Checkpoint_Every=1
#@markdown - Minimum 200 steps between each save.
stp=0
Start_saving_from_the_step=500 #@param{type: 'number'}
if Start_saving_from_the_step==None:
  Start_saving_from_the_step=0
if (Start_saving_from_the_step < 200):
  Start_saving_from_the_step=Save_Checkpoint_Every
stpsv=Start_saving_from_the_step
if Save_Checkpoint_Every_n_Steps:
  stp=Save_Checkpoint_Every
#@markdown - Start saving intermediary checkpoints from this step.

Caption=''
if Captionned_instance_images:
  Caption='--image_captions_filename'


def txtenc_train(Caption, stpsv, stp, MODELT_NAME, INSTANCE_DIR, CLASS_DIR, OUTPUT_DIR, PT, Seed, precision, Training_Steps):
  print('[1;33mTraining the text encoder with regularization...[0m')
  os.system("""accelerate launch /content/diffusers/examples/dreambooth/train_dreambooth.py \
    $Caption \
    --train_text_encoder \
    --dump_only_text_encoder \
    --pretrained_model_name_or_path="$MODEL_NAME" \
    --instance_data_dir="$INSTANCE_DIR" \
    --class_data_dir="$CLASS_DIR" \
    --output_dir="$OUTPUT_DIR" \
    --with_prior_preservation --prior_loss_weight=1.0 \
    --instance_prompt="$PT"\
    --seed=$Seed \
    --resolution=512 \
    --mixed_precision=$precision \
    --train_batch_size=1 \
    --gradient_accumulation_steps=1 --gradient_checkpointing \
    --use_8bit_adam \
    --learning_rate=2e-6 \
    --lr_scheduler="polynomial" \
    --lr_warmup_steps=0 \
    --max_train_steps=$Training_Steps \
    --num_class_images=200""")

def unet_train(Caption, SESSION_DIR, stpsv, stp, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, precision, Training_Steps):
  clear_output()
  print('[1;33mTraining the unet...[0m')
  os.system("""accelerate launch /content/diffusers/examples/dreambooth/train_dreambooth.py \
    $Caption \
    --train_only_unet \
    --Session_dir=$SESSION_DIR \
    --save_starting_step=$stpsv \
    --save_n_steps=$stp \
    --pretrained_model_name_or_path="$MODELT_NAME" \
    --instance_data_dir="$INSTANCE_DIR" \
    --output_dir="$OUTPUT_DIR" \
    --instance_prompt="$PT" \
    --seed=$Seed \
    --resolution=512 \
    --mixed_precision=$precision \
    --train_batch_size=1 \
    --gradient_accumulation_steps=1 \
    --use_8bit_adam \
    --learning_rate=2e-6 \
    --lr_scheduler="polynomial" \
    --lr_warmup_steps=0 \
    --max_train_steps=$Training_Steps""")

if Contains_faces!="No":
  
  txtenc_train(Caption, stpsv, stp, MODELT_NAME, INSTANCE_DIR, CLASS_DIR, OUTPUT_DIR, PT, Seed, precision, Training_Steps=stptxt)
  unet_train(Caption, SESSION_DIR, stpsv, stp, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, precision, Training_Steps)

else:
  os.system("""accelerate launch /content/diffusers/examples/dreambooth/train_dreambooth.py \
    $Caption \
    $Textenc \
    --save_starting_step=$stpsv \
    --stop_text_encoder_training=$stptxt \
    --save_n_steps=$stp \
    --Session_dir=$SESSION_DIR \
    --pretrained_model_name_or_path="$MODELT_NAME" \
    --instance_data_dir="$INSTANCE_DIR" \
    --output_dir="$OUTPUT_DIR" \
    --instance_prompt="$PT" \
    --seed=$Seed \
    --resolution=512 \
    --mixed_precision=$precision \
    --train_batch_size=1 \
    --gradient_accumulation_steps=1 \
    --use_8bit_adam \
    --learning_rate=2e-6 \
    --lr_scheduler="polynomial" \
    --lr_warmup_steps=0 \
    --max_train_steps=$Training_Steps""")


if os.path.exists('/content/models/'+INSTANCE_NAME+'/unet/diffusion_pytorch_model.bin'):
  print("Almost done ...")
  %cd /content    
  !wget -O convertosd.py https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dreambooth/convertosd.py
  clear_output()
  if precision=="no":
    !sed -i '226s@.*@@' /content/convertosd.py
  !sed -i '201s@.*@    model_path = "{OUTPUT_DIR}"@' /content/convertosd.py
  !sed -i '202s@.*@    checkpoint_path= "{SESSION_DIR}/{Session_Name}.ckpt"@' /content/convertosd.py
  !python /content/convertosd.py
  clear_output()
  if os.path.exists(SESSION_DIR+"/"+INSTANCE_NAME+'.ckpt'):
    if not os.path.exists(str(SESSION_DIR+'/tokenizer')):
      !cp -R '/content/models/'$INSTANCE_NAME'/tokenizer' "$SESSION_DIR"
    print("[1;32mDONE, the CKPT model is in your Gdrive in the sessions folder")
  else:
    print("[1;31mSomething went wrong")
    
else:
  print("[1;31mSomething went wrong")