import sys
sys.path.append("/content/ai-travel/")
import os
from IPython.utils import capture
import time
from face_recognition import recoFace
from PIL import Image
from subprocess import getoutput
from IPython.display import clear_output
import random
import transformers
from tqdm import tqdm

transformers.logging.set_verbosity_error()
from utils.Logger import get_local_logger
logger=get_local_logger()

# 更新至11.22
class DreamBooth():
    def __init__(self, param, original_album_param):


        Session_Name = param["Model_Name"]  # @param{type: 'string'}
        # @param ["No", "Female", "Male", "Both"]
        Contains_faces = param["Contains_Faces"] 
        #it doesn't improve faces, it reduces overfitting, but if you set the text_encoder at a low value, there won't be overfitting

        # Contains_faces = "No"  # @param ["No", "Female", "Male", "Both"]
        Training_Steps = int(param["Training_Steps"])  # @param{type: 'number'}
        Resume_Training = param.get("Training_Type").upper()
        Old_Model_Path = param.get("Old_Model_Name")

        MODEL_NAME = "/content/stable-diffusion-v1-5"
        PT = ""
        Captionned_instance_images = True
        Session_Name = Session_Name.replace(" ", "_")
        WORKSPACE = '/content/Fast-Dreambooth'
        INSTANCE_NAME = Session_Name
        OUTPUT_DIR = "/content/models/" + Session_Name
        SESSION_DIR = WORKSPACE + '/Sessions/' + Session_Name
        INSTANCE_DIR = SESSION_DIR + '/instance_images'
        MDLPTH = str(SESSION_DIR + "/" + Session_Name + '.ckpt')
        CLASS_DIR = SESSION_DIR + '/Regularization_images'

        def reg(CLASS_DIR):
            with capture.capture_output() as cap:
                if Contains_faces != "No":
                    if not os.path.exists(str(CLASS_DIR)):
                        os.system("""mkdir -p {}""".format(CLASS_DIR))
                    os.chdir(CLASS_DIR)
                    os.system("""rm -rf Women Men Mix""")
                    os.system(
                        """cp -r /content/Fast-Dreambooth/Regularization_images/* ./""")
                    os.system("""unzip Menz > /dev/null 2>&1""")
                    os.system("""unzip Womenz > /dev/null 2>&1""")
                    os.system("""unzip Mixz > /dev/null 2>&1""")
                    # os.system("""rm -rf Menz Womenz Mixz""")
                    os.system("""sudo chmod -R 777 /content""")
                    os.system(
                        """find . -name "* *" -type f | rename 's/ /_/g'""")  # 注意
                    os.chdir("""/content""")
                    clear_output()

        if Resume_Training == "RESUME_TRAINING":
            cos_path = "sd/models/" + \
                Old_Model_Path if Old_Model_Path[:
                                                 3] != "sd/" else Old_Model_Path
            cos_path = cos_path + \
                ".ckpt" if cos_path.rstrip()[-5] != ".ckpt" else cos_path

            logger.info("下载旧模型: "+str(cos_path))
            os.system("""coscmd download {} {}""".format(
                cos_path, str(SESSION_DIR + "/" + Session_Name + '.ckpt')))

        if os.path.exists(str(SESSION_DIR + "/" + Session_Name + '.ckpt')):
            logger.info('加载旧模型')
            reg(CLASS_DIR)
            os.system("""mkdir -p """ + OUTPUT_DIR)
            os.system(
                """python /content/diffusers/scripts/convert_original_stable_diffusion_to_diffusers.py --checkpoint_path {} --dump_path {} --session_dir {}""".format(
                    MDLPTH, OUTPUT_DIR, SESSION_DIR))
            if os.path.exists(OUTPUT_DIR + '/unet/diffusion_pytorch_model.bin'):
                resume = True
                os.system("""rm -rf /content/v1-inference.yaml""")
                logger.info('[1;32mSession loaded.')
            else:
                os.system("""rm -rf /content/v1-inference.yaml""")
                if not os.path.exists(OUTPUT_DIR + '/unet/diffusion_pytorch_model.bin'):
                    logger.info(
                        '[1;31mConversion error, if the error persists, remove the CKPT file from the current session folder')

        elif not os.path.exists(str(SESSION_DIR)):
            os.system("""mkdir -p """ + INSTANCE_DIR)
            logger.info('[1;32mCreating session...')
            reg(CLASS_DIR)
            # if not os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
            #     if os.path.exists('/content/stable-diffusion-v1-5'):
            #         os.system("""rm -rf '/content/stable-diffusion-v1-5'""")
            #     fdownloadmodel()
            if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
                logger.info('[1;32mSession created, proceed to uploading instance images')
            else:
                logger.info(
                    '[1;31mError downloading the model, make sure you have accepted the terms at https://huggingface.co/runwayml/stable-diffusion-v1-5')

        if Contains_faces == "Female":
            CLASS_DIR = CLASS_DIR + '/Women'
        if Contains_faces == "Male":
            CLASS_DIR = CLASS_DIR + '/Men'
        if Contains_faces == "Both":
            CLASS_DIR = CLASS_DIR + '/Mix'

        Remove_existing_instance_images = True  # @param{type: 'boolean'}

        if Remove_existing_instance_images:
            if os.path.exists(str(INSTANCE_DIR)):
                os.system("""rm -rf """ + INSTANCE_DIR)

        if not os.path.exists(str(INSTANCE_DIR)):
            os.system("""mkdir -p """ + INSTANCE_DIR)

        IMAGES_FOLDER_OPTIONAL = os.path.join("/content/original_album/", param["Model_Name"])
        os.system("mkdir -p " + IMAGES_FOLDER_OPTIONAL)
        logger.info("开始下载图片")
        for count, i in enumerate(original_album_param):
            url = i["url"]
            name = i["name"]
            img_path = IMAGES_FOLDER_OPTIONAL + "/" + str(name) + "(" + str(count+1) + ")"
            logger.info(img_path)
            try:
                os.system('wget -q -O "{}" "{}"'.format(img_path, url))
                img = Image.open(img_path)
                img.convert("RGB")
                img.save((img_path + ".jpg").strip("'"), "JPEG",quality=100, optimize=True, progressive=True)
                os.system('rm -rf "{}"'.format(img_path))
            except Exception as e:
                logger.info(e)
            finally:
                pass

        logger.info("图片下载完成")

        Crop_images = True if str(param["Crop_Images"]).upper(
        ) == "TRUE" else False  # @param{type: 'boolean'}
        Crop_size=512

        if IMAGES_FOLDER_OPTIONAL != "":
            if Crop_images:
                # logger.info("开始人脸裁剪")
                # for filename in os.listdir(IMAGES_FOLDER_OPTIONAL):
                #     recoFace.crop_img(os.path.join(
                #         IMAGES_FOLDER_OPTIONAL, filename))
                # logger.info("人脸裁剪完成")
                # os.system(
                #     'cp -r "{}/." "{}"'.format(IMAGES_FOLDER_OPTIONAL, INSTANCE_DIR))
                logger.info("开始图像裁剪")
                for filename in tqdm(os.listdir(IMAGES_FOLDER_OPTIONAL), bar_format='  |{bar:15}| {n_fmt}/{total_fmt} Uploaded'):
                    try:
                        extension = filename.split(".")[1].rstrip("'")
                        identifier=filename.split(".")[0]
                        new_path_with_file = os.path.join(INSTANCE_DIR, filename)
                        file = Image.open(IMAGES_FOLDER_OPTIONAL+"/"+filename)
                        width, height = file.size
                        if file.size !=(Crop_size, Crop_size):      
                            side_length = min(width, height)
                            left = (width - side_length)/2
                            top = (height - side_length)/2
                            right = (width + side_length)/2
                            bottom = (height + side_length)/2
                            image = file.crop((left, top, right, bottom))
                            image = image.resize((Crop_size, Crop_size))
                            if (extension.upper() == "JPG"):
                                image.save(new_path_with_file, format="JPEG", quality = 100)
                            else:
                                image.save(new_path_with_file, format=extension.upper())
                        else:
                            os.system('cp "{}/{}" "{}"'.format(IMAGES_FOLDER_OPTIONAL,filename,INSTANCE_DIR))
                            logger.info("{}/{} 裁剪".format(IMAGES_FOLDER_OPTIONAL,filename))
                    except Exception as e:
                        logger.error(e)
                logger.info("图像裁剪完成")
            else:
                os.system(
                    'cp -r "{}/." "{}"'.format(IMAGES_FOLDER_OPTIONAL, INSTANCE_DIR))

            os.chdir(INSTANCE_DIR)
            os.system("""find . -name "* *" -type f | rename 's/ /_/g'""")
            os.chdir("""/content""")
            if os.path.exists(INSTANCE_DIR + "/.ipynb_checkpoints"):
                os.system("""rm -r """ + INSTANCE_DIR + "/.ipynb_checkpoints")
            logger.info('开始训练模型')

        os.chdir(SESSION_DIR)
        os.system("""rm -rf instance_images.zip""")
        os.system("""zip -r instance_images instance_images""")
        os.chdir("""/content""")

        MODELT_NAME = MODEL_NAME

        Seed = ''  # @param{type: 'string'}

        if Seed == '' or Seed == '0':
            Seed = random.randint(1, 999999)
        else:
            Seed = int(Seed)

        # @markdown - Leave empty for a random seed.

        fp16 = True
        if fp16:
            prec = "fp16"
        else:
            prec = "no"

        s = getoutput('nvidia-smi')
        precision = prec

        if Resume_Training == "RESUME_TRAINING" and os.path.exists(OUTPUT_DIR + '/unet/diffusion_pytorch_model.bin'):
            MODELT_NAME = OUTPUT_DIR
            logger.info('在旧模型的基础上训练新模型')
        elif Resume_Training == "RESUME_TRAINING" and not os.path.exists(OUTPUT_DIR + '/unet/diffusion_pytorch_model.bin'):
            prlogger.infoint('旧模型没找到，直接训练新模型')
            MODELT_NAME = MODEL_NAME

        # @markdown ---------------------------

        try:
            Contain_f
            pass
        except:
            Contain_f = Contains_faces

        Enable_text_encoder_training = True if str(param["Enable_Text_Encoder_Training"]).upper(
        ) == "TRUE" else False  # @param{type: 'boolean'}

        Train_text_encoder_for = int(
            param["Train_Text_Encoder_For"])  # @param{type: 'number'}

        if Train_text_encoder_for >= 100:
            stptxt = Training_Steps
        elif Train_text_encoder_for == 0:
            Enable_text_encoder_training = False
            stptxt = 10
        else:
            stptxt = int((Training_Steps * Train_text_encoder_for) / 100)

        if not Enable_text_encoder_training:
            Contains_faces = "No"
        else:
            Contains_faces = Contain_f

        if Enable_text_encoder_training:
            Textenc = "--train_text_encoder"
        else:
            Textenc = ""

        # @markdown ---------------------------
        Save_Checkpoint_Every_n_Steps = False  # @param {type:"boolean"}
        Save_Checkpoint_Every = 500  # @param{type: 'number'}
        if Save_Checkpoint_Every == None:
            Save_Checkpoint_Every = 1
        # @markdown - Minimum 200 steps between each save.
        stp = 0
        Start_saving_from_the_step = 500  # @param{type: 'number'}
        if Start_saving_from_the_step == None:
            Start_saving_from_the_step = 0
        if (Start_saving_from_the_step < 200):
            Start_saving_from_the_step = Save_Checkpoint_Every
        stpsv = Start_saving_from_the_step
        if Save_Checkpoint_Every_n_Steps:
            stp = Save_Checkpoint_Every
        # @markdown - Start saving intermediary checkpoints from this step.

        Caption = ''
        if Captionned_instance_images:
            Caption = '--image_captions_filename'

        def txtenc_train(Caption, stpsv, stp, MODELT_NAME, INSTANCE_DIR, CLASS_DIR, OUTPUT_DIR, PT, Seed, precision,
                         Training_Steps):
            logger.info('[1;33mTraining the text encoder with regularization...[0m')
            os.system("""accelerate launch /content/diffusers/examples/dreambooth/train_dreambooth.py \
            {} \
            --train_text_encoder \
            --dump_only_text_encoder \
            --pretrained_model_name_or_path="{}" \
            --instance_data_dir="{}" \
            --class_data_dir="{}" \
            --output_dir="{}" \
            --with_prior_preservation --prior_loss_weight=1.0 \
            --instance_prompt="{}"\
            --seed={} \
            --resolution=512 \
            --mixed_precision={} \
            --train_batch_size=1 \
            --gradient_accumulation_steps=1 --gradient_checkpointing \
            --use_8bit_adam \
            --learning_rate=2e-6 \
            --lr_scheduler="polynomial" \
            --lr_warmup_steps=0 \
            --max_train_steps={} \
            --num_class_images=200""".
                      format(Caption, MODELT_NAME, INSTANCE_DIR, CLASS_DIR, OUTPUT_DIR, PT, Seed, precision,
                             Training_Steps))

        def unet_train(Caption, SESSION_DIR, stpsv, stp, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, precision,
                       Training_Steps):
            clear_output()
            logger.info('[1;33mTraining the unet...[0m')
            os.system("""accelerate launch /content/diffusers/examples/dreambooth/train_dreambooth.py \
            {} \
            --train_only_unet \
            --Session_dir={} \
            --save_starting_step={} \
            --save_n_steps={} \
            --pretrained_model_name_or_path="{}" \
            --instance_data_dir="{}" \
            --output_dir="{}" \
            --instance_prompt="{}" \
            --seed={} \
            --resolution=512 \
            --mixed_precision={} \
            --train_batch_size=1 \
            --gradient_accumulation_steps=1 \
            --use_8bit_adam \
            --learning_rate=2e-6 \
            --lr_scheduler="polynomial" \
            --lr_warmup_steps=0 \
            --max_train_steps={}""".
                      format(Caption, SESSION_DIR, stpsv, stp, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed,
                             precision, Training_Steps))

        if Contains_faces != "No":

            txtenc_train(Caption, stpsv, stp, MODELT_NAME, INSTANCE_DIR, CLASS_DIR, OUTPUT_DIR, PT, Seed, precision,
                         Training_Steps=stptxt)
            unet_train(Caption, SESSION_DIR, stpsv, stp, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, precision,
                       Training_Steps)

        else:
            os.system("""accelerate launch /content/diffusers/examples/dreambooth/train_dreambooth.py \
            {} \
            {} \
            --save_starting_step={}\
            --stop_text_encoder_training={} \
            --save_n_steps={}\
            --Session_dir={} \
            --pretrained_model_name_or_path="{}" \
            --instance_data_dir="{}" \
            --output_dir="{}" \
            --instance_prompt="{}" \
            --seed={} \
            --resolution=512 \
            --mixed_precision={} \
            --train_batch_size=1 \
            --gradient_accumulation_steps=1 \
            --use_8bit_adam \
            --learning_rate=2e-6 \
            --lr_scheduler="polynomial" \
            --lr_warmup_steps=0 \
            --max_train_steps={}""".format(
                Caption, Textenc, stpsv, stptxt, stp, SESSION_DIR, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed,
                precision, Training_Steps
            ))

        if os.path.exists('/content/models/' + INSTANCE_NAME + '/unet/diffusion_pytorch_model.bin'):
            os.chdir("""/content""")
            os.system("""python /content/ai-travel/fast_stable_diffusion/convertosd.py {} {} {}""".format(
                OUTPUT_DIR, SESSION_DIR, Session_Name))

            ckpt_model_path = SESSION_DIR + "/" + INSTANCE_NAME + '.ckpt'
            if os.path.exists(ckpt_model_path):
                if not os.path.exists(str(SESSION_DIR + '/tokenizer')):
                    os.system(
                        """cp -r '/content/models/{}/tokenizer' {}""".format(INSTANCE_NAME, SESSION_DIR))
                logger.info("模型训练完成，ckpt模型路径："+str(ckpt_model_path))
                logger.info("上传模型到腾讯云cos")
                os.system(
                    """coscmd upload {} sd/models/""".format(ckpt_model_path))

            else:
                logger.info("模型训练失败")

        else:
            logger.info("模型训练失败")

        def alter(file, old_str, new_str):
            """
            替换文件中的字符串
            :param file:文件名
            :param old_str:就字符串
            :param new_str:新字符串
            :return:

            """
            file_data = ""
            with open(file, "r", encoding="utf-8") as f:
                for line in f:
                    if old_str in line:
                        line = line.replace(old_str, new_str)
                    file_data += line
            with open(file, "w", encoding="utf-8") as f:
                f.write(file_data)
