from PyQt5.QtCore import QObject, pyqtSignal
import paho.mqtt.client as mqtt
from topics import TOPICS
from handlers import handle_led, handle_sensor, handle_motor

class MQTTClient(QObject):
    messageReceived = pyqtSignal(str, str)  # topic, message

    def __init__(self, broker="broker.hivemq.com", port=1883):
        super().__init__()
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.topic_handlers = {
            TOPICS["led_control"]: handle_led,
            TOPICS["sensor_data"]: handle_sensor,
        }

        self.subscriptions = list(self.topic_handlers.keys())

        self.client.connect(broker, port, 60)

    def on_connect(self, client, userdata, flags, rc):
        print("[MQTT] Connected with result code", rc)
        for topic in self.subscriptions:
            self.client.subscribe(topic)
            print(f"[MQTT] Subscribed to: {topic}")

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode()
        print(f"[MQTT] Message received: {topic} → {payload}")
        handler = self.topic_handlers.get(topic)
        if handler:
            handler(topic, payload)

        # Emit signal to update GUI
        self.messageReceived.emit(topic, payload)

    def publish(self, topic, message):
        print(f"[MQTT] Publishing to {topic}: {message}")
        self.client.publish(topic, message)

    def loop_start(self):
        self.client.loop_start()