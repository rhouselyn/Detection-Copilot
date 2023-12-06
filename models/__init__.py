import threading
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from transformers import DetrImageProcessor, DetrForObjectDetection, YolosForObjectDetection, YolosImageProcessor
import subprocess

resnet_50_processor = None
resnet_50_model = None
faster_rcnn_model = None
yolo_model = None
yolo_image_processor = None


def init_resnet_50():
    global resnet_50_processor, resnet_50_model
    resnet_50_processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    resnet_50_model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
    print("ResNet-50 initialized")


def init_faster_rcnn():
    global faster_rcnn_model
    faster_rcnn_model = fasterrcnn_resnet50_fpn(pretrained=True)
    print("Faster R-CNN initialized")


def init_yolo():
    global yolo_model, yolo_image_processor
    yolo_model = YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')
    yolo_image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
    print("YOLO initialized")


# def init_dino():
#     subprocess.run(["python", r"C:\Users\14815\Desktop\DINO-main\load_model.py"])
#     print("DINO initialized")


# 创建线程
thread_resnet = threading.Thread(target=init_resnet_50)
thread_faster_rcnn = threading.Thread(target=init_faster_rcnn)
thread_yolo = threading.Thread(target=init_yolo)
# thread_dino = threading.Thread(target=init_dino)

# 启动线程
thread_resnet.start()
thread_faster_rcnn.start()
thread_yolo.start()
# thread_dino.start()

# 等待线程完成
thread_resnet.join()
thread_faster_rcnn.join()
thread_yolo.join()
# thread_dino.join()

print("All models are initialized")
