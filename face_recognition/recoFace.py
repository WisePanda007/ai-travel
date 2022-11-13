'''
Author: chenya
Date: 2022-11-08 11:40:10
LastEditors: chenya
LastEditTime: 2022-11-08 19:21:14
FilePath: /chenya/CropFace/recoFace.py
Description: 

'''
import cv2
import numpy as np

prototxt_path = "/content/ai-travel/face_recognition/device_file/deploy.prototxt"
model_path = "/content/ai-travel/face_recognition/device_file/res10_300x300_ssd_iter_140000_fp16.caffemodel"
model = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

# test_json
test_json = {"code":0,"message":'null',"data":{"id":1,"original_album":["https://p1-q.mafengwo.net/s19/M00/A5/EC/CoNBHGNqCGMC1-f8AAAerrl_Opg.jpeg","https://p1-q.mafengwo.net/s19/M00/A1/08/CoNCfmNqCGNX91KiAAAOpAKr1LE.jpeg","https://p1-q.mafengwo.net/s19/M00/FD/07/CoNE4WNqCGNLs833AAATie9uH0I.jpeg","https://p1-q.mafengwo.net/s19/M00/B0/29/CoNJ72NqCGMxcxtVAAAQ7s0KY-Q.jpeg","https://p1-q.mafengwo.net/s19/M00/F3/FB/CoNBdGNqCGN7sBpeAAAWupoKt_I.jpeg"],"stage":"UNSCHEDULED","notice":"UNSCHEDULED-u672au8c03u5ea6 MODELING-u5efau6a21u4e2d PAINTING-u7ed8u56feu4e2d FILTERING-u7b5bu9009u4e2d DELIVERED-u5df2u4ea4u4ed8"}}

# def img_recog_judge(img_url, count, id_name):
#
#     res = urllib.request.urlopen(img_url)
#     img = np.asarray(bytearray(res.read()), dtype="uint8")
#     image = cv2.imdecode(img, cv2.IMREAD_COLOR)
#
#     img_height, img_width = image.shape[:2]
#     image_save_path = './'+str(id_name)+'/'+str(id_name)+'('+str(count)+')'+'.jpg'
#     if img_height<512 or img_width<512:
#         print('img_height:'+str(img_height))
#         print('img_width:'+str(img_width))
#         print('image too small.')
#         if img_height >= img_width:
#             size_diff = int((img_height-img_width)/2)
#             cropped = image[size_diff:size_diff+img_width, 0:img_width]
#         else:
#             size_diff = int((img_width-img_height)/2)
#             cropped = image[0:img_height, size_diff:img_height+size_diff]
#         cropped = cv2.resize(image, (512, 512), interpolation=cv2.INTER_CUBIC)
#         cv2.imwrite(image_save_path, cropped)
#         return 0
#
#     blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),(104.0, 177.0, 123.0))
#     model.setInput(blob)
#     output = np.squeeze(model.forward())
#
#     for i in range(0, output.shape[0]):
#         confidence = output[i, 2]
#         if confidence > 0.3: #置信度
#             box = output[i, 3:7] * np.array([img_width, img_height, img_width, img_height])
#             start_x, start_y, end_x, end_y = box.astype(np.int)
#
#             term0 = end_x - start_x
#             term1 = end_y -  start_y
#             if term0 > 512 or term1>512:
#                 print('person face bigger than 512x512, resize.')
#                 img_c = cv2.resize(image, (512, 512), interpolation=cv2.INTER_CUBIC)
#                 cv2.imwrite(image_save_path, img_c)
#                 return 0
#
#             face_width = end_x + start_x
#             face_width_mid = int(face_width/2)
#             face_height = end_y +  start_y
#             face_height_mid = int(face_height/2)
#
#             start_x_1 = face_width_mid-400
#             end_x_1 = face_width_mid+400
#             if start_x_1 < 0:
#                 start_x_1 = start_x
#                 # print('start_x_1 < 0')
#             if end_x_1 > img_width:
#                 end_x_1 = end_x
#                 # print('end_x_1 > img_width')
#
#             start_y_1 = face_height_mid-400
#             end_y_1 = face_height_mid+400
#             if start_y_1 < 0:
#                 start_y_1 = start_y
#                 # print('start_y_1 < 0')
#             if end_y_1 > img_height:
#                 end_y_1 = end_y
#                 # print('end_y_1 > face_height')
#
#             face_width = end_x_1 - start_x_1
#             face_height = end_y_1 - start_y_1
#             # print('face_height_changed:'+str(face_height))
#             # print('face_width_changed:'+str(face_width))
#
#             cropped = image[start_y_1:end_y_1, start_x_1:end_x_1]
#             cropped = cv2.resize(cropped, (512, 512), interpolation=cv2.INTER_CUBIC)
#             cv2.imwrite(image_save_path, cropped)
#             return 0

def crop_img(img_path):

    image = cv2.imread(img_path)
    img_height, img_width = image.shape[:2]
    image_save_path = img_path

    if img_height<512 or img_width<512:
        print('img_height:'+str(img_height))
        print('img_width:'+str(img_width))
        print('image too small.')
        if img_height >= img_width:
            size_diff = int((img_height-img_width)/2)
            cropped = image[size_diff:size_diff+img_width, 0:img_width]
        else:
            size_diff = int((img_width-img_height)/2)
            cropped = image[0:img_height, size_diff:img_height+size_diff]
        cropped = cv2.resize(image, (512, 512), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(image_save_path, cropped)
        return 0

    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),(104.0, 177.0, 123.0))
    model.setInput(blob)
    output = np.squeeze(model.forward())

    for i in range(0, output.shape[0]):
        confidence = output[i, 2]
        if confidence > 0.3: #置信度
            box = output[i, 3:7] * np.array([img_width, img_height, img_width, img_height])
            start_x, start_y, end_x, end_y = box.astype(np.int)

            term0 = end_x - start_x
            term1 = end_y -  start_y
            if term0 > 512 or term1>512:
                print('person face bigger than 512x512, resize.')
                img_c = cv2.resize(image, (512, 512), interpolation=cv2.INTER_CUBIC)
                cv2.imwrite(image_save_path, img_c)
                return 0

            face_width = end_x + start_x
            face_width_mid = int(face_width/2)
            face_height = end_y +  start_y
            face_height_mid = int(face_height/2)

            start_x_1 = face_width_mid-400
            end_x_1 = face_width_mid+400
            if start_x_1 < 0:
                start_x_1 = start_x
                # print('start_x_1 < 0')
            if end_x_1 > img_width:
                end_x_1 = end_x
                # print('end_x_1 > img_width')

            start_y_1 = face_height_mid-400
            end_y_1 = face_height_mid+400
            if start_y_1 < 0:
                start_y_1 = start_y
                # print('start_y_1 < 0')
            if end_y_1 > img_height:
                end_y_1 = end_y
                # print('end_y_1 > face_height')

            face_width = end_x_1 - start_x_1
            face_height = end_y_1 - start_y_1
            # print('face_height_changed:'+str(face_height))
            # print('face_width_changed:'+str(face_width))

            cropped = image[start_y_1:end_y_1, start_x_1:end_x_1]
            cropped = cv2.resize(cropped, (512, 512), interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(image_save_path, cropped)
            return 0
    
