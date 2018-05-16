from PyQt5.QtWidgets import QApplication

from package.ui.MainWindow import MainWindow


def run(argv):
    app = QApplication(argv)
    _ = MainWindow() # noqa
    app.exec_()
