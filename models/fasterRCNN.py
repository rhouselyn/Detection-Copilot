import torch
from torchvision.transforms import functional as F
from PIL import Image
from models import faster_rcnn_model


# 将对象检测逻辑封装到一个函数中
def detect(image):
    # 加载模型
    model = faster_rcnn_model
    model.eval()

    # 图像转换为张量
    image_tensor = F.to_tensor(image).unsqueeze(0)

    COCO_INSTANCE_CATEGORY_NAMES = [
        '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
        'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
        'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
        'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
        'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
        'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
        'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
        'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table', 'N/A',
        'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
        'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
    ]

    # 使用模型进行预测
    with torch.no_grad():
        prediction = model(image_tensor)

    # 获取检测到的对象信息
    try:
        detected_objects = []
        for score, label, box in zip(prediction[0]['scores'], prediction[0]['labels'], prediction[0]['boxes']):
            detected_objects.append({
                "box": [round(i, 2) for i in box.tolist()],
                "label": COCO_INSTANCE_CATEGORY_NAMES[label.item()],
                "score": round(score.item(), 3),
            })
    except Exception as e:
        print(e)

    return detected_objects


if __name__ == '__main__':
    image_path = r"C:\Users\14815\Desktop\微信图片编辑_20231204165750.jpg"
    image = Image.open(image_path).convert("RGB")

    detections = detect(image)
    for detection in detections:
        print(detection)
