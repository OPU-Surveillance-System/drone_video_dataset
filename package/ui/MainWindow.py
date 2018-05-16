from PyQt5.QtWidgets import QAction, QFileDialog, QMainWindow, qApp

from package.ui.LabelingWidget import LabelingWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.lw = None
        self.initUI()

    def initUI(self):
        openAct = QAction('&Labeling', self)
        openAct.setShortcut('Ctrl+O')
        openAct.setStatusTip('Open the directory of videos to label')
        openAct.triggered.connect(self.open)

        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.fileMenu = self.menuBar().addMenu('&File')
        self.fileMenu.addAction(openAct)
        self.fileMenu.addAction(exitAct)

        self.show()

    def open(self, index):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        if self.lw is not None:
            del self.lw

        self.lw = LabelingWidget(file + '/')
        self.setCentralWidget(self.lw)
