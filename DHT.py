import sys
import random
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from init import *
from MQTT_client import *

# Creating Client name -
global clientname
r=random.randrange(1,10000000)
clientname="DHT_sensor-"+room_ID+"-"+str(r)
update_rate = 5000 # in msec


class ConnectionDock(QDockWidget):
    """Main """

    def __init__ (self, mc):
        QDockWidget.__init__(self)

        self.mc = mc
        self.mc.set_on_connected_to_form(self.on_connected)
        self.eHostInput = QLineEdit()
        self.eHostInput.setInputMask('999.999.999.999')
        self.eHostInput.setText(broker_ip)

        self.ePort = QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(4)
        self.ePort.setText(broker_port)

        self.eClientID = QLineEdit()
        global clientname
        self.eClientID.setText(clientname)

        self.eUserName = QLineEdit()
        self.eUserName.setText(username)

        self.ePassword = QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText(password)

        self.eKeepAlive = QLineEdit()
        self.eKeepAlive.setValidator(QIntValidator())
        self.eKeepAlive.setText("60")

        self.eSSL = QCheckBox()

        self.eCleanSession = QCheckBox()
        self.eCleanSession.setChecked(True)

        self.eConnectbtn = QPushButton("Enable/Connect", self)
        self.eConnectbtn.setToolTip("click me to connect")
        self.eConnectbtn.clicked.connect(self.on_button_connect_click)
        self.eConnectbtn.setStyleSheet("background-color: gray")

        self.ePublisherTopic = QLineEdit()
        self.ePublisherTopic.setText(DHT_topic)

        self.Temperature = QLineEdit()
        self.Temperature.setText('')

        self.Humidity = QLineEdit()
        self.Humidity.setText('')

        formLayot = QFormLayout()
        formLayot.addRow("Turn On/Off", self.eConnectbtn)
        formLayot.addRow("Pub topic", self.ePublisherTopic)
        formLayot.addRow("Temperature", self.Temperature)
        formLayot.addRow("Humidity", self.Humidity)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)
        self.setWindowTitle("Connect")

    def on_connected (self):
        self.eConnectbtn.setStyleSheet("background-color: green")

    def on_button_connect_click (self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        self.mc.set_username(self.eUserName.text())
        self.mc.set_password(self.ePassword.text())
        self.mc.connect_to()
        self.mc.start_listening()

    def push_button_click (self):
        self.mc.publish_to(self.ePublisherTopic.text(), '"value":1')


class MainWindow(QMainWindow):

    def __init__ (self, parent=None):
        QMainWindow.__init__(self, parent)

        # Init of Mqtt_client class
        self.mc = Mqtt_client()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(update_rate)  # in msec

        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)

        # set up main window
        self.setGeometry(30, 600, 300, 150)
        self.setWindowTitle('DHT')

        # Init QDockWidget objects
        self.connectionDock = ConnectionDock(self.mc)

        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)

    def update_data (self):
        print('Next update')
        temp = 22 + random.randrange(1, 10) / 10
        hum = 30 + random.randrange(1, 60)
        current_data = 'temperature: ' + str(temp) + ' humidity: ' + str(hum)
        self.connectionDock.Temperature.setText(str(temp))
        self.connectionDock.Humidity.setText(str(hum))
        self.mc.publish_to(DHT_topic, current_data)

app = QApplication(sys.argv)
mainwin = MainWindow()
mainwin.show()
app.exec_()
