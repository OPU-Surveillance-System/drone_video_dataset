import sys, os, random, mimetypes, json
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QByteArray, Qt
import imageio

VIDEOS_PATH = 'DroneProtect-testing-set/'

class Window(QWidget):
    
    def __init__(self, videosPath):
        super().__init__()
        
        self.videos = [videosPath + f for f in os.listdir(VIDEOS_PATH) if mimetypes.guess_type(f)[0] is not None and mimetypes.guess_type(f)[0].split('/')[0] == 'video']

        self.initUI()
        self.load_image()
        
        
    def initUI(self):
        self.acceptButton = QPushButton("Normal")
        self.refuseButton = QPushButton("Anormal")
        
        self.acceptButton.clicked.connect(self.accept)
        self.refuseButton.clicked.connect(self.refuse)

        self.imageWidget = QLabel()

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.setRowStretch(0, 2)

        self.grid.addWidget(self.imageWidget, 0, 0, 1, 2)
        self.grid.addWidget(self.acceptButton, 1, 0)
        self.grid.addWidget(self.refuseButton, 1, 1)
        
        self.setLayout(self.grid)    
        
        self.setWindowTitle('--')    
        self.show()

    def load_save(self):
        x = 0

    def accept(self):
        self.load_image()
    
    def refuse(self):
        self.load_image()

    def load_image(self):
        video = random.choice(self.videos)
        reader = imageio.get_reader(video)

        n = reader.get_length()
        i = random.randrange(0, n)
        frame = reader.get_data(i)

        image = QImage(frame, frame.shape[1], frame.shape[0], frame.shape[1] * 3, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        smaller_pixmap = pixmap.scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.imageWidget.setPixmap(smaller_pixmap)
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Window(VIDEOS_PATH)
    sys.exit(app.exec_())