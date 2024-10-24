import otp_exchange
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class window(QWidget):
    def __init__(self, parent = None):
        super(window, self).__init__(parent)

        layout = QVBoxLayout()


        self.pad_select_btn = QPushButton("select pad zipfile")
        self.pad_select_btn.clicked.connect(self.set_pad)

        layout.addWidget(self.pad_select_btn)

        self.setLayout(layout)
        self.setWindowTitle("OTP Exchange")

    def set_pad(self):
        f_path, _filter = QFileDialog.getOpenFileName(self, 'Select file', '~',"Zip files (*.zip)")
        self.pad = otp_exchange.OneTimePad(f_path, "bin/temp_local_pad")
        self.pad_select_btn.setText(f"pad selected, {self.pad.remaining()} bytes remaining")



def main():
    app = QApplication(sys.argv)
    ex = window()
    ex.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
