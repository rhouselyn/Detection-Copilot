import io

from PIL import ImageDraw, ImageFont, ImageQt
from PyQt5.QtGui import QImage, QPixmap

import config
from models import yolo_tiny, resnet50, fasterRCNN

current_total_objects = []


def process_new_image(image, obj_list=None):
    global current_total_objects

    copy_image = image.copy()

    model = config.model
    if model == "YOLO-tiny" or model.lower() == "yolo":
        current_total_objects = yolo_tiny.detect(image)
    elif model == "resnet-50" or model.lower() == "resnet":
        current_total_objects = resnet50.detect(image)
    # elif model == "DINO":
    #     current_total_objects = dino.detect(image)
    elif model.lower() == "rcnn":
        current_total_objects = fasterRCNN.detect(image)
    else:
        return None

    detected_objects = current_total_objects

    if obj_list:
        detected_objects = [obj for obj in current_total_objects if obj["label"] in obj_list]

    return label_image(copy_image, detected_objects)


def label_image(image, detected_objects):
    if not image:
        return None

    label_color = config.label_color
    box_color = config.box_color
    threshold = config.threshold
    is_label = config.is_label
    is_score = config.is_score

    # Create an ImageDraw object to draw
    draw = ImageDraw.Draw(image)

    # Use the default font provided by PIL
    font = ImageFont.truetype('arial.ttf', 15)  # 使用Arial字体，大小为15

    for obj in detected_objects:
        # Extract the annotation information
        box = obj["box"]
        label = obj["label"]
        score = obj["score"]

        # Check if the score is above the threshold
        if score > threshold:
            # Draw a rectangle outline
            draw.rectangle(((box[0], box[1]), (box[2], box[3])), outline=box_color, width=2)

            if is_label and is_score:
                display_text = f"{label} {score:.3f}"
            elif is_label:
                display_text = label
            elif is_score:
                display_text = f"{score:.3f}"
            else:
                display_text = ""

            # Draw the text with black color
            draw.text((box[0], box[1]), display_text, fill=label_color, font=font)

    return image


def update_label(image, update_model):
    global current_total_objects

    detected_objects = [obj for obj in current_total_objects if obj["label"] in config.object_list]

    if not image:
        return None

    if update_model:
        return process_new_image(image, config.object_list)
    else:
        return label_image(image, detected_objects)


def pil_image_to_qpixmap(pil_img):
    """
    将PIL图像转换为QPixmap对象。
    """
    # 将PIL图像转换为字节
    byte_array = io.BytesIO()
    pil_img.save(byte_array, format='PNG')

    # 创建QImage并从字节转换
    qimg = QImage()
    qimg.loadFromData(byte_array.getvalue())

    # 将QImage转换为QPixmap
    pixmap = QPixmap.fromImage(qimg)
    return pixmap
