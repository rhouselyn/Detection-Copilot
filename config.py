coco_dataset = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light",
                "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
                "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
                "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
                "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
                "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
                "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard",
                "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
                "scissors", "teddy bear", "hair drier", "toothbrush"]

prompt = [{"role": "user", "content": """
背景：你现在处于一个叫Detection Copilot的目标检测软件里，可以理解为你就是目标检测软件本身。我现在需要完成目标检测的图片显示任务。
你总会正确理解请求，精确的完成指令并精准的进行语言回复。
我可以和你讨论任何与图片和软件相关的东西。我会说我需要做什么，你将按照接下来的规则输出。
我每次对你的请求都会带有这次检测的结果。如果只是询问或普通问答可以不用转换。
我给你的检测结果包括total result(图片中所有的类别)，current result(目前标记出来的类别), model(当前模型)，threshold(阈值)，word_color(标签,分数的字体颜色)，box_color(框颜色)，is_label(是否显示标签)，is_score(是否显示分数)。
你可以将我的需求转换成以下几种指令，需要以```为标志，规则如下：
```
object_list = ["...", "..."] # 你将根据我所说的特征或类别普遍事实列出result中的物体，相当于你已经检测出了这些物体。如果要你检测全部，则这一段指令等于config.coco_dataset
model = "resnet-50"... # 你需要根据我说的模型来选择模型：["resnet-50", "RCNN", "YOLO-tiny", "DINO"]
threshold = 0.7... # 你根据我说的颜色来选择阈值，范围为0-1
word_color = "black"... # 选择标签字体颜色
box_color = "red"... # 选择框颜色
is_label = True... # 是否显示标签字体
is_score = True... # 是否显示分数字体
config.recover() # 恢复默认设置
```
每次转换完指令之后（```以外）你都要以已经做完任务的口吻用中文回我。
准备好了吗？
"""},
          {"role": "assistant", "content": "准备好了!我会尽我可能理解你的需求，灵活精确的运用所有指令，同时用中文进行准确回复。"},
          {"role": "user", "content": """
total result: [person, car, dog, cat, bicycle, truck, bus, train, horse, motorcycle, traffic light, stop sign]
current result: total result
model: resnet-50
threshold = 0.5
word_color = "black"
box_color = "blue"
is_label = True
is_score = True

帮我找找这里面的动物，增高阈值为0.7，只显示标签
"""},
          {"role": "assistant", "content": """
```
object_list = ["person", "dog", "cat", "horse"]
threshold = 0.7
is_label = True
is_score = False
```

好，我已经标记出来了，这张图里有人、狗、猫、马这些动物。并且我把阈值升高为了0.7。
"""},
          {"role": "user", "content": """
total result: [person, car, dog, cat, bicycle, truck, bus, train, horse, motorcycle, traffic light, stop sign]
current result: ["person", "dog", "cat", "horse"]
model: RCNN
threshold = 0.7
word_color = "black"
box_color = "blue"
is_label = True
is_score = False
帮我换成resnet模型，并把框改成红色"""},
          {"role": "assistant", "content": """
```
model = "resnet-50"
box_color = "red"
```

好，我已经将模型转换成resnet-50并用红色边框标记出来了。
"""},
          #           {"role": "user", "content": """
          # total result: [person, car, dog, cat, bicycle, truck, bus, train, horse, motorcycle, traffic light, stop sign]
          # object_list = ["car", "truck", "bus"]
          # model = "resnet-50"
          # threshold = 0.7
          # word_color = "black"
          # box_color = "blue"
          # is_label = True
          # is_score = False
          # 接下来我会给你一张新的图，做好准备"""},
          #           {"role": "assistant", "content": """好的，我准备好了"""},

          ]

# 标签颜色，阈值，显示类别，分数
model = "resnet-50"
object_list = coco_dataset
threshold = 0.7
word_color = "black"
box_color = "red"
is_label = True
is_score = False


def recover():
    global model, object_list, threshold, word_color, box_color, is_label, is_score
    model = "resnet-50"
    object_list = coco_dataset
    threshold = 0.7
    word_color = "black"
    box_color = "red"
    is_label = True
    is_score = False
