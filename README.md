# ai-travel

# 一：代码结构
### &emsp;config: 参数
&emsp;&emsp;模型训练参数,提示词参数,各种路径

### &emsp;face-recognition: 人脸识别 接收url；输出512*512

### &emsp;img：图片存储路径

### &emsp;model：模型缓存路径

### &emsp;script：执行脚本
### &emsp;&emsp;Main
&emsp;&emsp;&emsp;&emsp;调用face,调用train,调用deply,调用util

### &emsp;stable diffusion 
&emsp;  &emsp;train  接收512*512，训练参数；输出model 

&emsp; &emsp;deply  接收model，提示词，渲染参数；输出图片
### &emsp;util ：以上几个模块的工具类