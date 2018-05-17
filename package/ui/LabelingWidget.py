import hashlib
import json
import mimetypes
import os
import random

import imageio
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QGridLayout, QLabel, QPushButton,
                             QWidget)


def sha1(filename):
    """Return the sha1 of a file."""
    BUF_SIZE = 65536
    sha1 = hashlib.sha1()

    with open(filename, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


class LabelingWidget(QWidget):

    def __init__(self, videosPath):
        super().__init__()
        self.setWindowTitle('Initialization...')

        self.videosPath = videosPath
        self.videos = [
            f for f in os.listdir(videosPath) if (
                mimetypes.guess_type(f)[0] is not None and
                mimetypes.guess_type(f)[0].split('/')[0] == 'video'
            )
        ]

        self.load_dataset()
        self.save_dataset()

        self.initUI()
        self.load_image()

    def initUI(self):
        """Initialize the UI."""
        self.acceptButton = QPushButton("Normal")
        self.refuseButton = QPushButton("Anormal")

        self.acceptButton.clicked.connect(self.accept)
        self.refuseButton.clicked.connect(self.refuse)

        self.imageWidget = QLabel()

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.grid.addWidget(self.imageWidget, 0, 0, 1, 2)
        self.grid.addWidget(self.acceptButton, 1, 0)
        self.grid.addWidget(self.refuseButton, 1, 1)

        self.setLayout(self.grid)

    def initialize_dataset(self):
        """Generate a new dataset."""
        self.dataset = {}
        for video in self.videos:
            reader = imageio.get_reader(self.videosPath + video)
            n = reader.get_length()

            self.dataset[video] = {
                'sha1': sha1(self.videosPath + video),
                'frames_count': n,
                'frames': {}
            }

    def load_dataset(self):
        """Load an already existing dataset or initialize a new one."""
        fname = self.videosPath + 'dataset.jsons'
        if os.path.isfile(fname):
            with open(fname) as f:
                self.dataset = json.load(f)
                for video, data in self.dataset.items():
                    self.dataset[video]['frames'] = {
                        int(k): v
                        for k, v in data['frames'].items()
                    }
        else:
            self.initialize_dataset()

    def save_dataset(self):
        """Save data to `dataset.json` along side the videos."""
        fname = self.videosPath + 'dataset.jsons'
        with open(fname, 'w') as outfile:
            json.dump(self.dataset, outfile, indent=2, sort_keys=True)
            outfile.close()

    def keyPressEvent(self, event):
        """Handle key pressed event.

        Enter, A, S, D, F : Label frame as normal
        Backspace, J, K, L, `;` : Label frane as anormal
        """
        if self.current is not None:
            acceptKeys = [Qt.Key_Enter, Qt.Key_A, Qt.Key_S,
                          Qt.Key_D, Qt.Key_F]
            refuseKeys = [Qt.Key_Backspace, Qt.Key_J, Qt.Key_K,
                          Qt.Key_L, Qt.Key_Semicolon]

            if event.key() in acceptKeys:
                self.accept()
            elif event.key() in refuseKeys:
                self.refuse()

    def accept(self):
        """Label current frame as normal and load the next frame"""
        self.dataset[self.current[0]]['frames'][int(self.current[1])] = True
        self.save_dataset()
        self.load_image()

    def refuse(self):
        """Label current frame as anormal and load the next frame"""
        self.dataset[self.current[0]]['frames'][int(self.current[1])] = False
        self.save_dataset()
        self.load_image()

    def load_image(self):
        """Select a random unlabeled frame from all videos"""

        # Ignore fully labeled videos
        filtered_videos = list(
            filter(
                lambda video:
                    (len(self.dataset[video]['frames']) <
                        self.dataset[video]['frames_count']),
                self.videos
            )
        )

        if len(filtered_videos) == 0:
            self.end()
            return

        video = random.choice(filtered_videos)
        reader = imageio.get_reader(self.videosPath + video)

        n = reader.get_length()

        # Select a random frame from those who are not labeled
        i = random.choice(list(
            filter(
                lambda j:
                    self.dataset[video]['frames'].get(int(j)) is None,
                range(0, n)
            )
        ))
        frame = reader.get_data(i)

        self.current = (video, i)
        self.setWindowTitle('%s, frame %i/%i' % (video, i, n))

        image = QImage(
            frame, frame.shape[1], frame.shape[0], frame.shape[1] * 3,
            QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        smaller_pixmap = pixmap.scaled(
            800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.imageWidget.setPixmap(smaller_pixmap)

    def end(self):
        """Display a message and unset current"""
        label = QLabel("Every frames have been labeled, thank you.")
        label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.grid.addWidget(label, 0, 0, 1, 2)

        self.imageWidget.setHidden(True)
        self.acceptButton.setHidden(True)
        self.refuseButton.setHidden(True)

        self.current = None
