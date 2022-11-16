# @markdown #Create/Load a Session
class DreamBooth():
    def __init__(self, param, original_album_param):
        import os
        from IPython.utils import capture
        import time
        from face_recognition import recoFace
        from PIL import Image
        from subprocess import getoutput
        from IPython.display import clear_output
        import random

        def fdownloadmodel():
            token = input("Insert your huggingface token :")
            os.chdir("""/content/""")
            os.system("""mkdir /content/stable-diffusion-v1-5""")
            os.chdir("""/content/stable-diffusion-v1-5""")
            os.system("""git init""")
            os.system("""git lfs install --force --system --skip-repo""")
            os.system(
                """git remote add -f origin  'https://USER:{}@huggingface.co/runwayml/stable-diffusion-v1-5'""".format(
                    token))
            os.system("""git config core.sparsecheckout true""")
            os.system(
                """echo "feature_extractor\nsafety_checker\nscheduler\ntext_encoder\ntokenizer\nunet\nmodel_index.json" > .git/info/sparse-checkout""")
            os.system("""git pull origin main""")
            if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
                os.system("""git clone 'https://USER:{}@huggingface.co/stabilityai/sd-vae-ft-mse'""".format(token))
                os.system("""mv /content/stable-diffusion-v1-5/sd-vae-ft-mse /content/stable-diffusion-v1-5/vae""")
                os.system("""rm -r /content/stable-diffusion-v1-5/.git""")
                os.chdir("""/content/""")
                clear_output()

        MODEL_NAME = "/content/stable-diffusion-v1-5"
        PT = ""

        Captionned_instance_images = True

        Session_Name = param["Session_Name"]  # @param{type: 'string'}
        while Session_Name == "":
            print('[1;31mInput the Session Name:')
            Session_Name = input('')
        Session_Name = Session_Name.replace(" ", "_")

        Session_Link_optional = ""  # @param{type: 'string'}

        WORKSPACE = '/content/Fast-Dreambooth'

        if Session_Link_optional != "":
            print('[1;32mDownloading session...')
        with capture.capture_output() as cap:
            os.chdir("""/content""")
            # if Session_Link_optional != "":
            #     if not os.path.exists(str(WORKSPACE + '/Sessions')):
            #         os.system("mkdir -p " + str(WORKSPACE + '/Sessions'))
            #         time.sleep(1)
            #     os.chdir(str(WORKSPACE + '/Sessions'))
            #     os.system("""gdown --folder --remaining-ok -O {} {} """.format(Session_Name, Session_Link_optional))
            #     os.chdir(Session_Name)
            #     os.system("""rm -r instance_images""")
            #     os.system("""rm -r Regularization_images""")
            #     os.system("""unzip instance_images.zip""")
            #     os.system("""rm instance_images.zip""")
            #     os.system("""mv *.ckpt {}.ckpt""".format(Session_Name))
            #     os.chdir("""/content""")

        INSTANCE_NAME = Session_Name
        OUTPUT_DIR = "/content/models/" + Session_Name
        SESSION_DIR = WORKSPACE + '/Sessions/' + Session_Name
        INSTANCE_DIR = SESSION_DIR + '/instance_images'
        MDLPTH = str(SESSION_DIR + "/" + Session_Name + '.ckpt')
        CLASS_DIR = SESSION_DIR + '/Regularization_images'

        Contains_faces = param["Contains_Faces"]  # @param ["No", "Female", "Male", "Both"]

        def reg(CLASS_DIR):
            with capture.capture_output() as cap:
                if Contains_faces != "No":
                    if not os.path.exists(str(CLASS_DIR)):
                        os.system("""mkdir -p {}""".format(CLASS_DIR))
                    os.chdir(CLASS_DIR)
                    os.system("""rm -rf Women Men Mix""")
                    os.system(
                        """wget -p -O Womenz 'https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dreambooth/Regularization/Women'""")
                    os.system(
                        """wget -p -O Menz 'https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dreambooth/Regularization/Men'""")
                    os.system(
                        """wget -p -O Mixz 'https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dreambooth/Regularization/Mix'""")
                    os.system("""unzip Menz""")
                    os.system("""unzip Womenz""")
                    os.system("""unzip Mixz""")
                    os.system("""rm -rf Menz Womenz Mixz""")
                    os.system("""find . -name "* *" -type f | rename 's/ /_/g'""")  # 注意
                    os.chdir("""/content""")
                    clear_output()

        if os.path.exists(str(SESSION_DIR)) and not os.path.exists(str(SESSION_DIR + "/" + Session_Name + '.ckpt')):
            print(
                '[1;32mLoading session with no previous model, using the original model or the custom downloaded model')
            reg(CLASS_DIR)
            if not os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
                if os.path.exists('/content/stable-diffusion-v1-5'):
                    os.system("""rm -rf '/content/stable-diffusion-v1-5'""")
                fdownloadmodel()
            if not os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
                print(
                    '[1;31mError downloading the model, make sure you have accepted the terms at https://huggingface.co/runwayml/stable-diffusion-v1-5')
            else:
                print('[1;32mSession Loaded, proceed to uploading instance images')

        elif os.path.exists(str(SESSION_DIR + "/" + Session_Name + '.ckpt')):
            print('[1;32mSession found, loading the trained model ...')
            reg(CLASS_DIR)
            os.system("""mkdir -p """ + OUTPUT_DIR)
            os.system(
                """python /content/diffusers/scripts/convert_original_stable_diffusion_to_diffusers.py --checkpoint_path {} --dump_path {} --session_dir {}""".format(
                    MDLPTH, OUTPUT_DIR, SESSION_DIR))
            if os.path.exists(OUTPUT_DIR + '/unet/diffusion_pytorch_model.bin'):
                resume = True
                os.system("""rm -rf /content/v1-inference.yaml""")
                print('[1;32mSession loaded.')
            else:
                os.system("""rm -rf /content/v1-inference.yaml""")
                if not os.path.exists(OUTPUT_DIR + '/unet/diffusion_pytorch_model.bin'):
                    print(
                        '[1;31mConversion error, if the error persists, remove the CKPT file from the current session folder')

        elif not os.path.exists(str(SESSION_DIR)):
            os.system("""mkdir -p """ + INSTANCE_DIR)
            print('[1;32mCreating session...')
            reg(CLASS_DIR)
            if not os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
                if os.path.exists('/content/stable-diffusion-v1-5'):
                    os.system("""rm -rf '/content/stable-diffusion-v1-5'""")
                fdownloadmodel()
            if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
                print('[1;32mSession created, proceed to uploading instance images')
            else:
                print(
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

        IMAGES_FOLDER_OPTIONAL = os.path.join('/content/original_album/',param["Session_Name"])
        os.system("mkdir -p " + IMAGES_FOLDER_OPTIONAL)
        for count, i in enumerate(original_album_param):
            url = i["url"]
            name = i["name"]
            img_path = IMAGES_FOLDER_OPTIONAL +"/"+ str(name) + '(' + str(count) + ')' + '.jpeg'
            os.system('wget "{}" -O "{}"'.format(url, img_path))
            img = Image.open(img_path)
            img.save(img_path.rstrip(".jpeg") + ".jpg", "JPEG", quality=100, optimize=True, progressive=True)
            os.system('rm -rf "{}"'.format(img_path))


        Crop_images = True if param["Crop_Images"].upper() == "TRUE" else False  # @param{type: 'boolean'}
        Crop_size = 512  # @param{type: 'number'}

        while IMAGES_FOLDER_OPTIONAL != "" and not os.path.exists(str(IMAGES_FOLDER_OPTIONAL)):
            print('[1;31mThe image folder specified does not exist, use the colab file explorer to copy the path :')
            IMAGES_FOLDER_OPTIONAL = input('')

        if IMAGES_FOLDER_OPTIONAL != "":
            with capture.capture_output() as cap:
                if Crop_images:
                    print("开始人脸裁剪")
                    for filename in os.listdir(IMAGES_FOLDER_OPTIONAL):
                        recoFace.crop_img(os.path.join(IMAGES_FOLDER_OPTIONAL, filename))
                        os.system('cp -r "{}/." "{}"'.format(IMAGES_FOLDER_OPTIONAL, INSTANCE_DIR))
                    print("人脸裁剪完成")
                else:
                    os.system('cp -r "{}/." "{}"'.format(IMAGES_FOLDER_OPTIONAL, INSTANCE_DIR))

                os.chdir(INSTANCE_DIR)
                os.system("""find . -name "* *" -type f | rename 's/ /_/g'""")  # 注意
                os.chdir("""/content""")
                if os.path.exists(INSTANCE_DIR + "/.ipynb_checkpoints"):
                    os.system("""rm -r """ + INSTANCE_DIR + "/.ipynb_checkpoints")
            print('[1;32mDone, proceed to the training cell')

        with capture.capture_output() as cap:
            os.chdir(SESSION_DIR)
            os.system("""rm -rf instance_images.zip""")
            os.system("""zip -r instance_images instance_images""")
            os.chdir("""/content""")

        Resume_Training = False  # @param {type:"boolean"}

        if not Resume_Training and not os.path.exists(
                '/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
            if os.path.exists('/content/stable-diffusion-v1-5'):
                os.system("""rm -rf '/content/stable-diffusion-v1-5'""")
            print('[1;31mOriginal model not found, downloading....[0m')
            fdownloadmodel()
            if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
                print('[1;32mModel downloaded, proceeding to training...')
            else:
                print(
                    '[1;31mError downloading the model, make sure you have accepted the terms at https://huggingface.co/runwayml/stable-diffusion-v1-5')

        MODELT_NAME = MODEL_NAME

        Training_Steps = int(param["Training_Steps"])  # @param{type: 'number'}

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

        try:
            resume
            if resume and not Resume_Training:
                print(
                    '[1;31mOverwrite your previously trained model ?, answering "yes" will train a new model, answering "no" will resume the training of the previous model?  yes or no ?[0m')
                while True:
                    ansres = input('')
                    if ansres == 'no':
                        Resume_Training = True
                        del ansres
                        break
                    elif ansres == 'yes':
                        Resume_Training = False
                        resume = False
                        break
        except:
            pass

        if Resume_Training and os.path.exists(OUTPUT_DIR + '/unet/diffusion_pytorch_model.bin'):
            MODELT_NAME = OUTPUT_DIR
            print('[1;32mResuming Training...[0m')
        elif Resume_Training and not os.path.exists(OUTPUT_DIR + '/unet/diffusion_pytorch_model.bin'):
            print('[1;31mPrevious model not found, training a new model...[0m')
            MODELT_NAME = MODEL_NAME

        # @markdown ---------------------------

        try:
            Contain_f
            pass
        except:
            Contain_f = Contains_faces

        Enable_text_encoder_training = True if param[
                                                   "Enable_Text_Encoder_Training"].upper() == "TRUE" else False  # @param{type: 'boolean'}

        Train_text_encoder_for = int(param["Train_Text_Encoder_For"])  # @param{type: 'number'}

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
            print('[1;33mTraining the text encoder with regularization...[0m')
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
                      format(Caption, MODEL_NAME, INSTANCE_DIR, CLASS_DIR, OUTPUT_DIR, PT, Seed, precision,
                             Training_Steps))

        def unet_train(Caption, SESSION_DIR, stpsv, stp, MODELT_NAME, INSTANCE_DIR, OUTPUT_DIR, PT, Seed, precision,
                       Training_Steps):
            clear_output()
            print('[1;33mTraining the unet...[0m')
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
            print("Almost done ...")
            os.chdir("""/content""")
            os.system("""python /content/ai-travel/fast_stable_diffusion/convertosd.py {} {} {}""".format(OUTPUT_DIR,
                                                                                                          SESSION_DIR,
                                                                                                          Session_Name))
            if os.path.exists(SESSION_DIR + "/" + INSTANCE_NAME + '.ckpt'):
                if not os.path.exists(str(SESSION_DIR + '/tokenizer')):
                    os.system("""cp -R '/content/models/{}/tokenizer' {}""".format(INSTANCE_NAME, SESSION_DIR))
                print("[1;32mDONE, the CKPT model is in your Gdrive in the sessions folder")
            else:
                print("[1;31mSomething went wrong")

        else:
            print("[1;31mSomething went wrong")

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
