from PyQt5.QtWidgets import QAction, QFileDialog, QMainWindow, qApp

from package.ui.LabelingWidget import LabelingWidget
from package.ui.ReviewWidget import ReviewWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.lw = None
        self.rw = None
        self.initUI()

    def initUI(self):
        openAct = QAction('&Labeling', self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open the directory of videos to label')
        openAct.triggered.connect(self.open)

        reviewAct = QAction('&Review', self)
        reviewAct.setShortcut('Ctrl+R')
        reviewAct.setStatusTip('Open the directory of videos to review')
        reviewAct.triggered.connect(self.review)

        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.fileMenu = self.menuBar().addMenu('&File')
        self.fileMenu.addAction(openAct)
        self.fileMenu.addAction(reviewAct)
        self.fileMenu.addAction(exitAct)

        self.show()
        self.review(4)

    def clearWidget(self):
        self.takeCentralWidget()
        if self.lw is not None:
            del self.lw
            self.lw = None
        if self.rw is not None:
            del self.rw
            self.rw = None

    def open(self, index):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        self.clearWidget()
        self.lw = LabelingWidget(file + '/')
        self.setCentralWidget(self.lw)

    def review(self, index):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        self.clearWidget()        
        self.rw = ReviewWidget(file + '/')
        self.setCentralWidget(self.rw)
