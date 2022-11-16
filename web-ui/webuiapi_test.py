import webuiapi
from PIL import Image

# create API client
api = webuiapi.WebUIApi()

# set host, port
api = webuiapi.WebUIApi(host='127.0.0.1', port=7863)

# # # set default sampler, steps.
api = webuiapi.WebUIApi(sampler='Euler a', steps=20)

result1 = api.txt2img(prompt="cute Sumiyao",
                    negative_prompt="ugly, out of frame",
                    seed=1003,
                    styles=["anime"],
                    cfg_scale=7,
#                      sampler_index='DDIM',
#                      steps=30,
                    )
# images contains the returned images (PIL images)
result1.images
test_path = "/root/autodl-tmp/weui-bstable-diffusion/test_image/"
count = 0
for image in result1.images:
    image.save(test_path + str(count)+ '.jpg')
    count += 1
            
# image is shorthand for images[0]
# im = result1.image
# im.save("out.jpeg")
# # # cv2.imwrtie('api_out.jpg',result1.image)
print('saved')
# # # info contains text info about the api call
# # result1.info

# # info contains paramteres of the api call
# result1.parameters

# result1.imagepython 