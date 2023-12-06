import sys

from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QLabel, QMenuBar, QAction, QLineEdit, QFrame,
                             QSizePolicy, QFileDialog)

from windows import window_process


class ChatWindow(QMainWindow):
    current_image = None

    def get_current_image(self):
        return self.current_image

    def set_current_image(self, image):
        self.current_image = image

    def __init__(self):
        super().__init__()

        # Initialize the Menu Bar
        self.menuBar = self.menuBar()
        choose_menu = self.menuBar.addAction('Choose Image')
        choose_menu.triggered.connect(self.choose_image)

        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Left side - Image display area
        self.imageLabel = QLabel()
        self.imageLabel.setStyleSheet("background-color: white; border: 1px solid black")

        # Right side - Chat area
        self.chatDisplay = QTextEdit()
        self.chatDisplay.setReadOnly(True)  # Make the chat display read-only

        # Create a frame for the input area and buttons
        self.inputFrame = QFrame()
        self.inputFrame.setFrameShape(QFrame.StyledPanel)
        self.inputFrame.setFrameShadow(QFrame.Raised)
        self.inputFrame.setStyleSheet("background-color: white;")

        self.chatInput = QLineEdit()  # Single-line input
        self.chatInput.setStyleSheet("border: none;")
        self.chatInput.setFixedHeight(50)  # Set a fixed height for the input area
        self.chatInput.setPlaceholderText("Type your message here...")
        # Allow vertical scrolling for the input when text overflows
        self.chatInput.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.sendButton = QPushButton('Send')
        self.sendButton.setStyleSheet("border: none;")
        self.clearButton = QPushButton('Clear')
        self.clearButton.setStyleSheet("border: none;")

        # Connect the send button and enter key press to the send message function
        self.sendButton.clicked.connect(self.send_message)
        self.chatInput.returnPressed.connect(self.send_message)
        self.clearButton.clicked.connect(self.clear_chat)

        # Layout for the input frame
        input_layout = QHBoxLayout(self.inputFrame)
        input_layout.addWidget(self.chatInput)
        input_layout.addWidget(self.clearButton)
        input_layout.addWidget(self.sendButton)

        # Chat area layout
        chat_layout = QVBoxLayout()
        chat_layout.addWidget(self.chatDisplay, 1)  # Allow the chat display to expand more
        chat_layout.addWidget(self.inputFrame)  # Add the input frame to the layout

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.imageLabel, 3)  # Image display takes 3/4 of the window
        main_layout.addLayout(chat_layout, 1)  # Chat area takes 1/4 of the window

        # Set the layout to the central widget
        central_widget.setLayout(main_layout)

        # Window settings
        self.setWindowTitle('Detection Copilot')
        self.showMaximized()  # Show the window maximized

    def send_message(self):
        window_process.send_message(self)

    def display_reply(self, reply):
        window_process.display_reply(self, reply)

    def clear_chat(self):
        window_process.clear_chat(self)

    def choose_image(self):
        window_process.choose_image(self)

    def update_image(self, image):
        window_process.update_image(self, image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ChatWindow()
    win.show()
    sys.exit(app.exec_())
