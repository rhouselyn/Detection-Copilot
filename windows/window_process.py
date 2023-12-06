import os

from PIL import Image
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtWidgets import QFileDialog

from models import chatbot, execute_code as execute
from windows import image_process
from dotenv import load_dotenv

load_dotenv()


def send_message(self):
    text = self.chatInput.text()
    if text:  # If there's text in the input field
        # Append text to the chat display
        self.chatDisplay.append(f"You:\n{text}\n")
        self.chatInput.clear()  # Clear the input field
        self.reply_thread = WorkerThread(text, self)
        self.reply_thread.reply_received.connect(self.display_reply)
        self.reply_thread.start()


def display_reply(self, reply):
    # 当收到回复时，将其显示在聊天区域
    self.chatDisplay.append(f"Model Assistant:\n{reply}\n")


def clear_chat(self):
    self.chatDisplay.clear()  # Clear the chat display
    chatbot.clear_dialog()  # Clear the dialog history


def choose_image(self):
    img_path = os.getenv("img_path")
    image_path, _ = QFileDialog.getOpenFileName(self, 'Choose Image',
                                                img_path,
                                                'Image Files (*.jpg *.png *.jpeg)')
    if image_path:  # Check if a file was selected
        rgb_image = Image.open(image_path).convert("RGB")
        self.set_current_image(rgb_image)
        self.update_image(rgb_image)
        copy_image = rgb_image.copy()
        self.repaint()

        # Start the image processing thread
        processing_thread = ImageProcessingThread(copy_image, self)
        processing_thread.processing_done.connect(self.update_image)  # Connect the signal
        processing_thread.start()


def update_image(self, image):
    if not image:
        return

    new = image_process.pil_image_to_qpixmap(image)
    self.imageLabel.setPixmap(new.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))


class WorkerThread(QThread):
    # 创建一个pyqtSignal信号，用于在得到回复时发送数据
    reply_received = pyqtSignal(str)

    def __init__(self, prompt, parent):
        super().__init__()
        self.prompt = prompt
        self.window = parent

    def run(self):
        code, reply = chatbot.get_output(self.prompt)  # 假设这个函数返回模型的回复

        if code:
            execute.run_code(code)
            self.update_image(True if 'model' in code else False)

        self.reply_received.emit(reply)

    def update_image(self, update_model):
        image = self.window.get_current_image().copy()

        if not image:
            return

        new_image = image_process.update_label(image, update_model)
        self.window.update_image(new_image)


class ImageProcessingThread(QThread):
    processing_done = pyqtSignal(Image.Image)  # Signal to emit the processed image

    def __init__(self, image, parent=None):
        super().__init__(parent)
        self.image = image

    def run(self):
        processed_image = image_process.process_new_image(self.image)
        self.processing_done.emit(processed_image)
