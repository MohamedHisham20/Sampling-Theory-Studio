# on values_changed, and on QTimer timeout, update all plots
# _____________________________________________________________________________________________
# | Signal Composer:               | __________________________________________________________|
# |                                |   Signal Plot:                |   Reconstruction Plot:    |
# |                                |                               |                           |
# |                                |                               |                           |
# |                                |                               |                           |
# | _______________________________|                               |                           |
# | Sampling frequency:            |                               |                           |
# | Reconstruction technique:      | __________________________________________________________|
# |                                |   Difference Plot:            |   Frequency Domain Plot:  |
# |                                |                               |                           |
# |                                |                               |                           |
# |________________________________|                               |                           |
# |Noise Controls                  |                               |                           |
# |                                |                               |                           |
# |                                |                               |                           |
# |_____________________________________________________________________________________________
from PySide6.QtWidgets import QMainWindow, QApplication


class MainWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Sampling Theory Studio")
        self.resize(1000, 600)
        self.show()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow(None)
    app.exec()
