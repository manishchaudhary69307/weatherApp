from PyQt5.QtWidgets import QApplication
from gui.weatherApp import WeatherApp
from mqtt_client import MQTTClient
import sys

def main():
    app = QApplication(sys.argv)

    window = WeatherApp()
    mqtt_client = MQTTClient()

    window.publishRequested.connect(mqtt_client.publish)
    mqtt_client.messageReceived.connect(window.update_message_display)

    mqtt_client.loop_start()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()