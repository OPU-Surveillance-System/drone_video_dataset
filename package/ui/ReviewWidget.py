import json
import mimetypes
import os
import subprocess

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QGridLayout, QLabel, QListWidget, QPushButton,
                             QWidget, QSizePolicy)


class ReviewWidget(QWidget):

    def __init__(self, videosPath):
        super().__init__()

        self.videosPath = videosPath
        self.videos = [
            f for f in os.listdir(videosPath) if (
                mimetypes.guess_type(f)[0] is not None and
                mimetypes.guess_type(f)[0].split('/')[0] == 'video'
            )
        ]

        self.load_dataset()
        self.initUI()

    def initUI(self):
        self.list = QListWidget()
        self.list.addItems(self.videos)

        self.list.setFlow(self.list.LeftToRight)
        self.list.setWrapping(True)
        self.list.setResizeMode(self.list.Adjust)
        self.list.setSpacing(1)
        fm = self.list.fontMetrics()
        
        listHeight = (len(self.videos) + 1)*(fm.ascent() + fm.descent())
        height = min(500, listHeight)
        self.list.setMaximumHeight(listHeight)

        self.text = QLabel("", self)
        self.text.setAlignment(Qt.AlignCenter)

        self.openButton = QPushButton("Open", self)
        self.openButton.clicked.connect(self.open)        

        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.grid.setColumnMinimumWidth(0, 300)
        self.grid.setColumnMinimumWidth(1, 300)
        self.grid.setRowMinimumHeight(0, height / 2)
        self.grid.setRowMinimumHeight(1, height / 2)

        self.grid.addWidget(self.text, 0, 1)
        self.grid.addWidget(self.openButton, 1, 1)
        self.grid.addWidget(self.list, 0, 0, 2, 1)

        self.setLayout(self.grid)

        self.list.currentItemChanged.connect(lambda x: self.select(x.text()))
        self.select(self.videos[0])

    def select(self, video):
        labeled = len(self.dataset[video]['frames'])
        self.text.setText(
            '%s\n\n%i/%i frames labeled' %
            (video, labeled, self.dataset[video]['frames_count']))

    def open(self):
        subprocess.call(["xdg-open", self.videosPath + self.list.currentItem().text()])

    def load_dataset(self):
        fname = self.videosPath + 'dataset.jsons'
        if os.path.isfile(fname):
            with open(fname) as f:
                self.dataset = json.load(f)
                for video, data in self.dataset.items():
                    self.dataset[video]['frames'] = {
                        int(k): v
                        for k, v in data['frames'].items()
                    }
            return True
        else:
            return False
