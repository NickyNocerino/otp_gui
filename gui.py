import otp_exchange

import sys
import subprocess
from requests import get

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class PingThread(QThread):

    done=pyqtSignal(bool)

    def __init__(self, ip_to_ping):
        super().__init__()
        self.ip = ip_to_ping

    def run(self):
        try:
            print(f"Pinging {self.ip}...")
            # Using subprocess.Popen to ping the given IP address

            process = subprocess.Popen(
                ['ping', '-c', '1', self.ip],  # Ping with 4 packets (for Windows, replace '-c' with '-n')
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            # Capture output and errors, and wait for the process to finish
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                print("Ping successful")
                success = True
            else:
                print(f"Ping failed with error: {stderr.decode()}")
                success = False

        except Exception as e:
            print(f"Exception occurred: {e}")
            success = False
        self.done.emit(success)



class window(QWidget):
    def __init__(self, parent = None):
        super(window, self).__init__(parent)

        layout = QGridLayout()

        self.pub_ip_label = QLabel(self)
        self.pub_ip_label.setText("your public ip address:")
        layout.addWidget(self.pub_ip_label, 1, 1)

        self.pub_ip = QLabel(self)
        self.pub_ip.setText("{}".format(get('https://api.ipify.org').content.decode('utf8')))
        layout.addWidget(self.pub_ip, 1, 2)

        self.client_ip_label = QLabel(self)
        self.client_ip_label.setText("remote public ip address:")
        layout.addWidget(self.client_ip_label, 2, 1)


        self.client_ip = QLineEdit(self)
        self.client_ip.setText("")
        layout.addWidget(self.client_ip, 2, 2)

        self.ping_remote_btn = QPushButton("Ping")
        self.ping_remote_btn.clicked.connect(self.ping_remote)
        layout.addWidget(self.ping_remote_btn, 2, 3)

        self.pad_select_btn = QPushButton("select pad zipfile")
        self.pad_select_btn.clicked.connect(self.set_pad)

        layout.addWidget(self.pad_select_btn, 4, 3)

        self.setLayout(layout)
        self.setWindowTitle("OTP Exchange")
        #self.setGeometry(100,100, 600, 300)

    def set_pad(self):
        f_path, _filter = QFileDialog.getOpenFileName(self, 'Select file', '/',"Zip files (*.zip)")
        self.pad = otp_exchange.OneTimePad(f_path, "bin/temp_local_pad")
        self.pad_select_btn.setText(f"pad selected, {self.pad.remaining()} bytes remaining")

    def ping_remote(self):
        ip_to_ping = self.client_ip.text()
        self.client_ip.setStyleSheet("background-color: grey;")
        self.worker = PingThread(ip_to_ping)
        self.worker.done.connect(self.post_ping)
        self.worker.start()

    def post_ping(self, success):
        if success:
            self.client_ip.setStyleSheet("background-color: green;")
            self.valid_client_ip = self.client_ip.text()
            self.ping_remote_btn.setText("Success (press again to update remote)")
        else:
            self.client_ip.setStyleSheet("background-color: red;")
            self.ping_remote_btn.setText("remote client could not be reached (try again)")


def main():
    app = QApplication(sys.argv)
    ex = window()
    ex.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
