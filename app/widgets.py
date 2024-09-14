from PySide6.QtWidgets import QProgressBar, QPushButton

from PySide6.QtGui import QColor, QPalette

DEFAULT_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: lightblue;
    width: 10px;
    margin: 1px;
}
"""

FAILED_STYLE = """
QProgressBar{
    border: 2px solid red;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: red;
    width: 10px;
    margin: 1px;
}
"""

COMPLETED_STYLE = """
QProgressBar{
    border: 2px solid grey;
    border-radius: 5px;
    text-align: center
}

QProgressBar::chunk {
    background-color: red;
    width: 10px;
    margin: 1px;
}
"""

class CustomProgressBar(QProgressBar):
    def __init__(self, parent = None):
        QProgressBar.__init__(self, parent)
        self.setStyleSheet(DEFAULT_STYLE)

    def changeWhenFailed(self):
        self.setStyleSheet(FAILED_STYLE)


class CustomButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize with a default color (optional)
        self.setGray()

    def setBlue(self):
        self._setColor(QColor("darkblue"), QColor("white"))

    def setGreen(self):
        self._setColor(QColor("green"), QColor("white"))

    def setGray(self):
        self._setColor(QColor("gray"), QColor("darkGray"))

    def _setColor(self, background_color, text_color):
        palette = self.palette()
        palette.setColor(QPalette.Button, background_color)
        palette.setColor(QPalette.ButtonText, text_color)
        self.setPalette(palette)

        # Ensure the button does not resize horizontally
        self.setFixedWidth(150)  # Adjust the width as needed