import torch
from PIL import Image
from models import resnet_50_model, resnet_50_processor


def detect(image):
    # 初始化处理器和模型
    processor = resnet_50_processor
    model = resnet_50_model

    # 处理图像并获取模型输出
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # 后处理：从模型输出中获取边界框和类别信息
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0)[0]

    detected_objects = []

    # 处理每个检测到的对象
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        detected_objects.append({
            "box": [round(i, 2) for i in box.tolist()],
            "label": model.config.id2label[label.item()],
            "score": round(score.item(), 3),
        })

    return detected_objects


if __name__ == '__main__':
    # 调用函数
    image_path = r"C:\Users\14815\Desktop\微信图片编辑_20231204165750.jpg"
    image = Image.open(image_path).convert("RGB")

    detections = detect(image)
    for detection in detections:
        print(detection)
