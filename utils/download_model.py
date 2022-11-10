class DownloadModel():
    def __init__(self, param):
        import os
        import time
        from IPython.display import clear_output
        from IPython.utils import capture

        # @markdown - Skip this cell if you are loading a previous session

        # @markdown ---

        with capture.capture_output() as cap:
            os.chdir("""/content/""")

        Huggingface_Token = param["Huggingface_Token"]  # @param {type:"string"}
        token = Huggingface_Token

        def downloadmodel():
            print("开始下载模型")
            token = Huggingface_Token
            if token == "":
                token = input("Insert your huggingface token :")
            if os.path.exists('/content/stable-diffusion-v1-5'):
                os.system("""rm -r /content/stable-diffusion-v1-5""")

            os.chdir("""/content/""")
            os.system("""mkdir -p /content/stable-diffusion-v1-5""")
            os.chdir("""/content/stable-diffusion-v1-5""")
            os.system("""git init""")
            os.system("""git lfs install --system --skip-repo""")
            os.system(
                'git remote add -f origin  "https://USER:{}@huggingface.co/runwayml/stable-diffusion-v1-5"'.format(
                    token))
            os.system("""git config core.sparsecheckout true""")
            os.system(
                """echo "feature_extractor\nsafety_checker\nscheduler\ntext_encoder\ntokenizer\nunet\nmodel_index.json" > .git/info/sparse-checkout""")
            os.system("""git pull origin main""")
            if os.path.exists('/content/stable-diffusion-v1-5/unet/diffusion_pytorch_model.bin'):
                os.system("""git clone "https://USER:{}@huggingface.co/stabilityai/sd-vae-ft-mse" """.format(token))
                os.system("""mv /content/stable-diffusion-v1-5/sd-vae-ft-mse /content/stable-diffusion-v1-5/vae""")
                os.system("""rm -r /content/stable-diffusion-v1-5/.git""")
                alter("/content/stable-diffusion-v1-5/scheduler/scheduler_config.json", '"trained_betas": null', '"trained_betas": null,\naaaaa')
                alter("/content/stable-diffusion-v1-5/scheduler/scheduler_config.json", "aaaaa", '  "clip_sample": false')
                alter("/content/stable-diffusion-v1-5/vae/config.json", '"sample_size": 512,', '"sample_size": 256,')
                os.chdir("""/content/""")
                print('模型下载完成')
            else:
                while not os.path.exists('/content/stable-diffusion-v1-5'):
                    print(
                        '[1;31mMake sure you accepted the terms in https://huggingface.co/runwayml/stable-diffusion-v1-5')
                    time.sleep(5)

        def alter(file,old_str,new_str):
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
                        line = line.replace(old_str,new_str)
                    file_data += line
            with open(file,"w",encoding="utf-8") as f:
                f.write(file_data)

        downloadmodel()
