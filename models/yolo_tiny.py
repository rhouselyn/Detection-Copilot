from PIL import Image
import torch
import time
from models import yolo_model, yolo_image_processor


def detect(image):
    # 加载模型及其处理器
    model = yolo_model
    image_processor = yolo_image_processor

    # 预处理图像并进行对象检测
    start_time = time.time()
    inputs = image_processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    elapsed_time = time.time() - start_time
    print(f"Time: {elapsed_time}")

    # 后处理获取结果
    target_sizes = torch.tensor([image.size[::-1]])
    results = image_processor.post_process_object_detection(outputs, threshold=0, target_sizes=target_sizes)[0]

    # 整理检测结果
    detected_objects = []
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        detected_objects.append({
            "box": [round(i, 2) for i in box.tolist()],
            "label": model.config.id2label[label.item()],
            "score": round(score.item(), 3),
        })

    return detected_objects


if __name__ == '__main__':
    image_path = r"C:\Users\14815\Desktop\微信图片编辑_20231204165750.jpg"
    image = Image.open(image_path).convert("RGB")

    detected_objects = detect(image)
    for obj in detected_objects:
        print(obj)
