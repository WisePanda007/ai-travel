import os
import time
from IPython.utils import capture

with capture.capture_output() as cap:
    os.chdir("""/content/""")

Huggingface_Token = "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"  # @param {type:"string"}
token = Huggingface_Token


def downloadmodel(Huggingface_Token):
    token = Huggingface_Token
    if token == "":
        token = input("Insert your huggingface token :")
    if os.path.exists('/content/stable-diffusion-v1-5'):
        os.system("""rm -r /content/stable-diffusion-v1-5""")

    os.chdir("""/content/""")
    os.system("""mkdir /content/stable-diffusion-v1-5""")
    os.chdir("""/content/stable-diffusion-v1-5""")
    os.system("""git init""")
    os.system("""git lfs install --system --skip-repo""")
    os.system('git remote add -f origin  "https://USER:{}@huggingface.co/runwayml/stable-diffusion-v1-5"'.format(token))
    os.system("""git config core.sparsecheckout true""")
    os.system(
        """echo -e "feature_extractor\nsafety_checker\nscheduler\ntext_encoder\ntokenizer\nunet\nmodel_index.json" > .git/info/sparse-checkout""")
    os.system("""git pull origin main""")
    if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
        os.system('git clone "https://USER:{}@huggingface.co/stabilityai/sd-vae-ft-mse'.format(token))
        os.system("""mv /content/stable-diffusion-v1-5/sd-vae-ft-mse /content/stable-diffusion-v1-5/vae""")
        os.system("""rm -r /content/stable-diffusion-v1-5/.git""")
        os.system(
            """sed -i 's@"clip_sample": false@@g' /content/stable-diffusion-v1-5/scheduler/scheduler_config.json""")
        os.system(
            """sed -i 's@"trained_betas": null,@"trained_betas": null@g' /content/stable-diffusion-v1-5/scheduler/scheduler_config.json""")
        os.system(
            """sed -i 's@"sample_size": 256,@"sample_size": 512,@g' /content/stable-diffusion-v1-5/vae/config.json""")
        os.chdir("""/content/""")
        print('[1;32mDONE !')
    else:
        while not os.path.exists('/content/stable-diffusion-v1-5'):
            print('[1;31mMake sure you accepted the terms in https://huggingface.co/runwayml/stable-diffusion-v1-5')
            time.sleep(5)


downloadmodel(Huggingface_Token)
