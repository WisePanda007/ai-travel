import os
import time
from IPython.display import clear_output
from IPython.utils import capture

# @markdown - Skip this cell if you are loading a previous session

# @markdown ---


def downloadModel(Huggingface_Token="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", Path_to_HuggingFace="nitrosocke/redshift-diffusion", CKPT_Path="", CKPT_Link="", Compatiblity_Mode=""):

    with capture.capture_output() as cap:
        os.system("""cd /content/""")

    if Path_to_HuggingFace != "":
        downloadmodel_hf(Huggingface_Token,Path_to_HuggingFace)
    elif CKPT_Path != "":
        if os.path.exists('/content/stable-diffusion-v1-5'):
            os.system("""rm -r /content/stable-diffusion-v1-5""")
        if os.path.exists(str(CKPT_Path)):
            os.system("""mkdir /content/stable-diffusion-v1-5""")
            with capture.capture_output() as cap:
                if Compatiblity_Mode:
                    os.system("""wget https://raw.githubusercontent.com/huggingface/diffusers/039958eae55ff0700cfb42a7e72739575ab341f1/scripts/convert_original_stable_diffusion_to_diffusers.py """)
                    os.system(
                        """python /content/convert_original_stable_diffusion_to_diffusers.py --checkpoint_path "$CKPT_Path" --dump_path /content/stable-diffusion-v1-5 """)
                    os.system(
                        """rm /content/convert_original_stable_diffusion_to_diffusers.py""")
                else:
                    os.system("""python /content/diffusers/scripts/convert_original_stable_diffusion_to_diffusers.py --checkpoint_path "$CKPT_Path" --dump_path /content/stable-diffusion-v1-5    """)
            if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
                os.system("""rm /content/v1-inference.yaml""")
                print('[1;32mDONE !')
            else:
                os.system(
                    """rm /content/convert_original_stable_diffusion_to_diffusers.py""")
                os.system("""rm /content/v1-inference.yaml""")
                os.system("""rm -r /content/stable-diffusion-v1-5""")
                while not os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
                    print(
                        '[1;31mConversion error, Insufficient RAM or corrupt CKPT, use a 4.7GB CKPT instead of 7GB')
                    time.sleep(5)
        else:
            while not os.path.exists(str(CKPT_Path)):
                print(
                    '[1;31mWrong path, use the colab file explorer to copy the path')
                time.sleep(5)

    elif CKPT_Link != "":
        if os.path.exists('/content/stable-diffusion-v1-5'):
            os.system("""rm -r /content/stable-diffusion-v1-5     """)
        os.system("""gdown --fuzzy $CKPT_Link -O model.ckpt        """)
        if os.path.exists('/content/model.ckpt'):
            if os.path.getsize("/content/model.ckpt") > 1810671599:
                os.system("""mkdir /content/stable-diffusion-v1-5""")
                with capture.capture_output() as cap:
                    if Compatiblity_Mode:
                        os.system(
                            """wget https://raw.githubusercontent.com/huggingface/diffusers/039958eae55ff0700cfb42a7e72739575ab341f1/scripts/convert_original_stable_diffusion_to_diffusers.py""")
                        os.system(
                            """python /content/convert_original_stable_diffusion_to_diffusers.py --checkpoint_path /content/model.ckpt --dump_path /content/stable-diffusion-v1-5""")
                        os.system(
                            """rm /content/convert_original_stable_diffusion_to_diffusers.py         """)
                    else:
                        os.system(
                            """python /content/diffusers/scripts/convert_original_stable_diffusion_to_diffusers.py --checkpoint_path /content/model.ckpt --dump_path /content/stable-diffusion-v1-5""")
                if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
                    print('[1;32mDONE !')
                    os.system("""rm /content/v1-inference.yaml""")
                    os.system("""rm /content/model.ckpt""")
                else:
                    if os.path.exists('/content/v1-inference.yaml'):
                        os.system("""rm /content/v1-inference.yaml""")
                    os.system(
                        """rm /content/convert_original_stable_diffusion_to_diffusers.py""")
                    os.system("""rm -r /content/stable-diffusion-v1-5""")
                    os.system("""rm /content/model.ckpt""")
                    while not os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
                        print(
                            '[1;31mConversion error, Insufficient RAM or corrupt CKPT, use a 4.7GB CKPT instead of 7GB')
                        time.sleep(5)
            else:
                while os.path.getsize('/content/model.ckpt') < 1810671599:
                    print('[1;31mWrong link, check that the link is valid')
                    time.sleep(5)
    else:
        downloadmodel(Huggingface_Token)
    print("模型下载完成")


def downloadmodel(Huggingface_Token):
    print("下载Huggingface模型")
    token = Huggingface_Token
    if token == "":
        token = input("Insert your huggingface token :")
    if os.path.exists('/content/stable-diffusion-v1-5'):
        os.system("""rm -r /content/stable-diffusion-v1-5""")

    os.system("""cd /content/""")
    os.system("""mkdir /content/stable-diffusion-v1-5""")
    os.system("""cd /content/stable-diffusion-v1-5""")
    os.system("""git init""")
    os.system("""git lfs install --system --skip-repo""")
    os.system(
        """git remote add -f origin    "https://USER:{}@huggingface.co/runwayml/stable-diffusion-v1-5" """.format(Huggingface_Token))
    os.system("""git config core.sparsecheckout true""")
    os.system("""echo -e "feature_extractor\nsafety_checker\nscheduler\ntext_encoder\ntokenizer\nunet\nmodel_index.json" > .git/info/sparse-checkout""")
    os.system("""git pull origin main""")
    if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
        os.system(
            """git clone "https://USER:{}@huggingface.co/stabilityai/sd-vae-ft-mse" """.format(Huggingface_Token))
        os.system(
            """mv /content/stable-diffusion-v1-5/sd-vae-ft-mse /content/stable-diffusion-v1-5/vae""")
        os.system("""rm -r /content/stable-diffusion-v1-5/.git""")
        os.system(
            """sed -i 's@"clip_sample": false@@g' /content/stable-diffusion-v1-5/scheduler/scheduler_config.json""")
        os.system("""sed -i 's@"trained_betas": null,@"trained_betas": null@g' /content/stable-diffusion-v1-5/scheduler/scheduler_config.json""")
        os.system(
            """sed -i 's@"sample_size": 256,@"sample_size": 512,@g' /content/stable-diffusion-v1-5/vae/config.json""")
        os.system("""cd / content /""")
        print('[1;32mDONE !')
    else:
        while not os.path.exists('/content/stable-diffusion-v1-5'):
            print(
                '[1;31mMake sure you accepted the terms in https://huggingface.co/runwayml/stable-diffusion-v1-5')
            time.sleep(5)


def downloadmodel_hf(Huggingface_Token,Path_to_HuggingFace):

    print("下载Huggingface模型2")
    print(Huggingface_Token,Path_to_HuggingFace)

    if os.path.exists('/content/stable-diffusion-v1-5'):
        os.system("""rm -r /content/stable-diffusion-v1-5""")

    os.system("""cd /content/""")
    os.system("""mkdir /content/stable-diffusion-v1-5""")
    os.system("""cd /content/stable-diffusion-v1-5""")
    os.system("""git init""")
    os.system("""git lfs install --system --skip-repo""")
    os.system(
        """git remote add -f origin    \"https://USER:{}@huggingface.co/{}\" """.format(aaaa,bbbbb))
    os.system("""git config core.sparsecheckout true""")
    os.system("""echo -e "feature_extractor\nsafety_checker\nscheduler\ntext_encoder\ntokenizer\nunet\nmodel_index.json" > .git/info/sparse-checkout""")
    os.system("""git pull origin main""")
    if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
        os.system(
            """git clone \"https://USER:{}@huggingface.co/stabilityai/sd-vae-ft-mse\" """.format(Huggingface_Token))
        os.system(
            """mv /content/stable-diffusion-v1-5/sd-vae-ft-mse /content/stable-diffusion-v1-5/vae""")
        os.system("""rm -r /content/stable-diffusion-v1-5/.git""")
        os.system(
            """sed -i 's@"clip_sample": false@@g' /content/stable-diffusion-v1-5/scheduler/scheduler_config.json""")
        os.system("""sed -i 's@"trained_betas": null,@"trained_betas": null@g' /content/stable-diffusion-v1-5/scheduler/scheduler_config.json""")
        os.system(
            """sed -i 's@"sample_size": 256,@"sample_size": 512,@g' /content/stable-diffusion-v1-5/vae/config.json        """)
        os.system("""cd /content/        """)
        print('[1;32mDONE !')
    else:
        while not os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
            print('[1;31mCheck the link you provided')
            time.sleep(5)
