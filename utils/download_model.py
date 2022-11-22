import os 
class DownloadModel():
    def __init__(self, param):
        os.system("""rm -rf /content/stable-diffusion-v1-5*""")
        os.system("""coscmd download -f sd/models/stable-diffusion-v1-5.zip /content/stable-diffusion-v1-5.zip""")
        os.system("""unzip /content/stable-diffusion-v1-5.zip > /dev/null 2>&1""")
        os.system("""mv -f /content/content/stable-diffusion-v1-5 /content/stable-diffusion-v1-5""")
        os.system("""rm -rf /content/content""")