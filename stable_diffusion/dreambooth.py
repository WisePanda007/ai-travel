import os
from IPython.display import clear_output
from IPython.utils import capture
import wget
import time

# @markdown #Create/Load a Session


def dreamBooth(Session_Name="", Session_Link_optional="", Contains_faces="No",token=""):
    MODEL_NAME = "/content/stable-diffusion-v1-5"
    PT = ""

    Captionned_instance_images = True

    while Session_Name == "":
        print('[1;31mInput the Session Name:')
        Session_Name = input('')
    Session_Name = Session_Name.replace(" ", "_")

    WORKSPACE = '/content/gdrive/MyDrive/Fast-Dreambooth'

    if Session_Link_optional != "":
        print('[1;32mDownloading session...')
    with capture.capture_output() as cap:
        os.chdir("""/content""")
        if Session_Link_optional != "":
            if not os.path.exists(str(WORKSPACE+'/Sessions')):
                os.system("""mkdir -p {}'/Sessions'""".format(WORKSPACE))
                time.sleep(1)
            os.chdir("""{}'/Sessions'""".format(WORKSPACE))
            os.system(
                """gdown --folder --remaining-ok -O {}    {}""".format(Session_Name, Session_Link_optional))
            os.chdir("""{}""".format(Session_Name))
            os.system("""rm -r instance_images""")
            os.system("""rm -r Regularization_images""")
            os.system("""unzip instance_images.zip""")
            os.system("""rm instance_images.zip""")
            os.system("""mv *.ckpt {}.ckpt""".format(Session_Name))
            os.chdir("""/content""")

    INSTANCE_NAME = Session_Name
    OUTPUT_DIR = "/content/models/"+Session_Name
    SESSION_DIR = WORKSPACE+'/Sessions/'+Session_Name
    INSTANCE_DIR = SESSION_DIR+'/instance_images'
    MDLPTH = str(SESSION_DIR+"/"+Session_Name+'.ckpt')
    CLASS_DIR = SESSION_DIR+'/Regularization_images'

    # @param ["No", "Female", "Male", "Both"]

    if os.path.exists(str(SESSION_DIR)) and not os.path.exists(str(SESSION_DIR+"/"+Session_Name+'.ckpt')):
        print('[1;32mLoading session with no previous model, using the original model or the custom downloaded model')
        reg(Contains_faces,CLASS_DIR)
        if not os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
            if os.path.exists('/content/stable-diffusion-v1-5'):
                os.system("""rm -r '/content/stable-diffusion-v1-5'   """)
            fdownloadmodel(token)
        if not os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
            print('[1;31mError downloading the model, make sure you have accepted the terms at https://huggingface.co/runwayml/stable-diffusion-v1-5')
        else:
            print('[1;32mSession Loaded, proceed to uploading instance images')

    elif os.path.exists(str(SESSION_DIR+"/"+Session_Name+'.ckpt')):
        print('[1;32mSession found, loading the trained model ...')
        reg(Contains_faces,CLASS_DIR)
        os.system("""mkdir -p '{}'""".format(OUTPUT_DIR))
        os.system("""python /content/diffusers/scripts/convert_original_stable_diffusion_to_diffusers.py --checkpoint_path "{}" --dump_path "{}" --session_dir "{}" """.format(MDLPTH, OUTPUT_DIR, SESSION_DIR))
        if os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
            resume = True
            os.system("""rm /content/v1-inference.yaml""")
            clear_output()
            print('[1;32mSession loaded.')
        else:
            os.system("""rm /content/v1-inference.yaml""")
            if not os.path.exists(OUTPUT_DIR+'/unet/diffusion_pytorch_model.bin'):
                print(
                    '[1;31mConversion error, if the error persists, remove the CKPT file from the current session folder')

    elif not os.path.exists(str(SESSION_DIR)):
        os.system("""mkdir -p "" """.format(INSTANCE_DIR))
        print('[1;32mCreating session...')
        reg(Contains_faces,CLASS_DIR)
        if not os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
            if os.path.exists('/content/stable-diffusion-v1-5'):
                os.system("""rm -r '/content/stable-diffusion-v1-5'""")
            fdownloadmodel(token)
        if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
            print('[1;32mSession created, proceed to uploading instance images')
        else:
            print('[1;31mError downloading the model, make sure you have accepted the terms at https://huggingface.co/runwayml/stable-diffusion-v1-5')

    if Contains_faces == "Female":
        CLASS_DIR = CLASS_DIR+'/Women'
    if Contains_faces == "Male":
        CLASS_DIR = CLASS_DIR+'/Men'
    if Contains_faces == "Both":
        CLASS_DIR = CLASS_DIR+'/Mix'

        # @markdown

        # @markdown # The most importent step is to rename the instance pictures of each subject to a unique unknown identifier, example :
        # @markdown - If you have 30 pictures of yourself, simply select them all and rename only one to the chosen identifier for example : phtmejhn, the files would be : phtmejhn (1).jpg, phtmejhn (2).png ....etc then upload them, do the same for other people or objects with a different identifier, and that's it.
        # @markdown - Check out this example : https://i.imgur.com/d2lD3rz.jpeg


def fdownloadmodel(token):
    if token=="":
        token = input("Insert your huggingface token :")
    os.chdir("""/content/""")
    os.system("""mkdir /content/stable-diffusion-v1-5""")
    os.chdir("""/content/stable-diffusion-v1-5""")
    os.system("""git init""")
    os.system("""git lfs install --system --skip-repo""")
    os.system("""git remote add -f origin    "https://USER:{}@huggingface.co/runwayml/stable-diffusion-v1-5" """.format(token))
    os.system("""git config core.sparsecheckout true""")
    os.system("""echo -e "feature_extractor\nsafety_checker\nscheduler\ntext_encoder\ntokenizer\nunet\nmodel_index.json" > .git/info/sparse-checkout""")
    os.system("""git pull origin main""")
    if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
        os.system(
            """git clone "https://USER:{}@huggingface.co/stabilityai/sd-vae-ft-mse" """.format(token))
        os.system(
            """mv /content/stable-diffusion-v1-5/sd-vae-ft-mse /content/stable-diffusion-v1-5/vae""")
        os.system("""rm -r /content/stable-diffusion-v1-5/.git""")
        os.chdir("""/content/""")
        clear_output()


def reg(Contains_faces,CLASS_DIR):
    with capture.capture_output() as cap:
        if Contains_faces != "No":
            if not os.path.exists(str(CLASS_DIR)):
                os.system("""mkdir -p {}""".format(CLASS_DIR))
            os.chdir("""{}""".format(CLASS_DIR))
            os.system("""rm -r Women Men Mix""")
            os.system(
                """wget -O Womenz 'https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dreambooth/Regularization/Women'""")
            os.system(
                """wget -O Menz 'https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dreambooth/Regularization/Men'""")
            os.system(
                """wget -O Mixz 'https://github.com/TheLastBen/fast-stable-diffusion/raw/main/Dreambooth/Regularization/Mix'""")
            os.system("""unzip Menz""")
            os.system("""unzip Womenz""")
            os.system("""unzip Mixz""")
            os.system("""rm Menz Womenz Mixz""")
            os.system("""find . -name "* *" -type f | rename 's/ /_/g'""")
            os.chdir("""/content       """)

# @markdown - If you're training on a subject with a face or a movie/style that contains faces. (experimental, still needs some tuning)
