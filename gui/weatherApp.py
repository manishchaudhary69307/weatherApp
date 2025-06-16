from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
import os
import requests
from dotenv import load_dotenv

load_dotenv()

class WeatherApp(QWidget):
    publishRequested = pyqtSignal(str, str)  # topic, message

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MQTT Weather Controller")
        self.setGeometry(200, 200, 400, 400)
        self.apiKey = os.getenv("API_KEY_OPEN_WEATHER")
        self.initUI()

    def initUI(self):
        self.label = QLabel("MQTT Message Viewer")
        self.label.setFont(QFont("Arial", 16))

        self.weather_output = QLabel("Weather Info")
        self.weather_output.setObjectName("weather_output")
        self.weather_output.setWordWrap(True)

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city")

        self.weather_button = QPushButton("Get Weather")
        self.weather_button.clicked.connect(self.fetch_weather)

        self.message_display = QLabel("Waiting for messages...")
        self.message_display.setWordWrap(True)
        self.message_display.setObjectName("message_display")

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter message to send")

        self.send_button = QPushButton("Send 'led_on'")
        self.send_button.clicked.connect(self.send_led_on)

        self.send_custom_button = QPushButton("Send Custom")
        self.send_custom_button.clicked.connect(self.send_custom)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.weather_button)
        layout.addWidget(self.weather_output)
        layout.addWidget(self.message_display)
        layout.addWidget(self.input_box)
        layout.addWidget(self.send_button)
        layout.addWidget(self.send_custom_button)

        self.setLayout(layout)

        self.setStyleSheet("""
        QWidget {
            background-color: #ecf0d4;
        }
        QLabel {
            color: #3498db;
            font-size: 20px;
            font-weight: bold;
        }
        QLabel#message_display, QLabel#weather_output {
            color: #2c3e50;
            font-size: 16px;
        }
        QLineEdit {
            background-color: #ecf0f1;
            color: #2c3e50;
            border: 1px solid #bdc3c7;
            padding: 5px;
        }
        QPushButton {
            background-color: #3498db;
            color: #ffffff;
            border: 1px solid #2980b9;
            padding: 10px;
            font-weight: bold;
            border-radius: 5px;
        }
        """)

    def send_led_on(self):
        self.publishRequested.emit("led/control/sub", "led_on")

    def send_custom(self):
        msg = self.input_box.text().strip()
        if msg:
            self.publishRequested.emit("led/control/sub", msg)

    def update_message_display(self, topic, message):
        self.message_display.setText(f"Topic: {topic}\nMessage: {message}")

    def fetch_weather(self):
        city = self.city_input.text()
        if not city:
            self.weather_output.setText("Please enter a city name.")
            return

        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {'q': city, 'appid': self.apiKey}

        try:
            res = requests.get(base_url, params=params)
            data = res.json()
            if res.status_code == 200:
                temp_k = data['main']['temp']
                temp_c = temp_k - 273.15
                description = data['weather'][0]['description']
                humidity = data['main']['humidity']
                wind_speed = data['wind']['speed']
                self.weather_output.setText(
                    f"Weather in {city}:\nTemp: {temp_c:.1f}°C\nDesc: {description}\nHumidity: {humidity}%\nWind: {wind_speed} m/s"
                )
            else:
                self.weather_output.setText(f"Error: {data['message']}")
        except Exception as e:
            self.weather_output.setText(f"Request failed: {e}")
