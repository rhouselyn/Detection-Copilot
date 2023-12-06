# Detection-Copilot
gpt交互式多目标检测模型

### 目前功能：
**选择检测类别**
**切换模型**
**调整阈值**
**调整标签颜色**
**调整检测框颜色**
**是否显示标签**
**是否显示得分**

### 简介
Detection Copilot 是一款基于 GPT 大型语言模型预设文本原理构建的目标检测软件。本软件综合运用了多种先进的目标检测模型(resnet-50, yolo-tiny, faster-RCNN)，并与 ChatGPT 工具紧密结合，为用户提供了一种全新的交互体验。我们为该软件设计了一套专门的代码交互规范，并对其进行了深入的学习和优化，使其在与用户对话时能够根据用户指令返回预定义的代码，同时提供精准的语言回复。

通过这种方式，用户无需手动进行繁琐的操作，如选择标签类别、切换模型、调整阈值、标注对象、显示标签与得分，或更改框体和字体颜色。相反，用户仅需通过自然语言与程序进行交互，表达自己的需求，ChatGPT 便能自动执行相关命令，以实现图像的精确调整和展示。

此外，Detection Copilot 大大简化了展示、集成和对比新模型的过程，使其变得更加直观和便捷。特别是当用户需要查看特定类别的检测结果（例如动物、交通工具或人类）时，他们可以通过直接对话来自动选择所需类别，而无需手动勾选，从而节省大量时间。用户还可以随时调整显示阈值来查看模型的性能，设置是否显示标签和得分以简化或详化检测界面。甚至在图像背景导致原有勾选框和字体颜色难以识别的情况下，用户可以通过直接交流来获得对比色，而不必手动尝试寻找合适的颜色，这进一步提高了软件的用户友好性和实用性。

![G5(K2F$F$)@WFYN{DY~1JW0](https://github.com/rhouselyn/Detection-Copilot/assets/125283997/8fd54a25-5aa6-4f29-824f-9090b7c2bd88)

### 默认配置
```
model = "resnet-50"
object_list = coco_dataset
threshold = 0.7
word_color = "black"
box_color = "red"
is_label = True
is_score = False
```

### 如何使用
1. 下载项目
```
git clone https://github.com/rhouselyn/Detection-Copilot.git
```
2. 下载依赖
```
cd Detection-Copilot
pip install -r requirement.txt
```
3. 请自行在包内创建.env文件存放apikeys以调用chatgpt，和img_path存放默认选取图片打开地址，格式为
```
api_keys = key1,key2 # 逗号后无空格，不需要双引号
img_path = path\to\your\imgs
```
4. 运行
```
python main.py
```
进入界面后即可选取图像对话使用
