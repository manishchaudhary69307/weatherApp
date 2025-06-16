from PyQt5.QtWidgets import (
QWidget, QPushButton, QLabel, QVBoxLayout, QLineEdit, QCheckBox, QGroupBox, QHBoxLayout
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
import os
import requests
from dotenv import load_dotenv
import json
load_dotenv()

class WeatherApp(QWidget):
    publishRequested = pyqtSignal(str, str) # topic, message
    latest_sensor_data = "No data"

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MQTT Weather Controller")
        self.setGeometry(200, 200, 600, 600)
        self.apiKey = os.getenv("API_KEY_OPEN_WEATHER")
        self.initUI()

    def initUI(self):
        # Weather Info Group
        weather_box = QGroupBox("Weather Info")
        weather_layout = QVBoxLayout()

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city")

        self.weather_button = QPushButton("Get Weather")
        self.weather_button.clicked.connect(self.fetch_weather)

        self.weather_output = QLabel("Weather Info")
        self.weather_output.setObjectName("weather_output")
        self.weather_output.setWordWrap(True)

        weather_layout.addWidget(self.city_input)
        weather_layout.addWidget(self.weather_button)
        weather_layout.addWidget(self.weather_output)
        weather_box.setLayout(weather_layout)

        # Sensor Info Group
        sensor_box = QGroupBox("Sensor Info")
        sensor_layout = QVBoxLayout()

        self.sensor_output = QLabel("Sensor Data will appear here")
        self.sensor_output.setObjectName("sensor_output")
        self.sensor_output.setWordWrap(True)

        sensor_layout.addWidget(self.sensor_output)
        sensor_box.setLayout(sensor_layout)

        # Device Control Group
        control_box = QGroupBox("Device Control")
        control_layout = QVBoxLayout()

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter custom message")

        self.led_toggle = QCheckBox("LED ON/OFF")
        self.led_toggle.stateChanged.connect(self.toggle_led)

        self.send_custom_button = QPushButton("Send Custom")
        self.send_custom_button.clicked.connect(self.send_custom)

        control_layout.addWidget(self.input_box)
        control_layout.addWidget(self.led_toggle)
        control_layout.addWidget(self.send_custom_button)
        control_box.setLayout(control_layout)

        # Main Layout
        main_layout = QVBoxLayout()
        title = QLabel("MQTT Message Viewer")
        title.setFont(QFont("Arial", 16))

        main_layout.addWidget(title)
        main_layout.addWidget(weather_box)
        main_layout.addWidget(sensor_box)
        main_layout.addWidget(control_box)

        self.setLayout(main_layout)

        # Styling
        self.setStyleSheet("""
        QWidget {
            background-color: #ecf0d4;
        }
        QLabel {
            color: #3498db;
            font-size: 20px;
            font-weight: bold;
        }
        QLabel#weather_output, QLabel#sensor_output {
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
        QCheckBox {
            font-size: 16px;
            color: #2c3e50;
        }
        QGroupBox {
            border: 2px solid #3498db;
            border-radius: 5px;
            margin-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
            font-size: 16px;
        }
        """)

    def toggle_led(self, state):
        if state == Qt.Checked:
            self.publishRequested.emit("led/control/sub", "led_on")
        else:
            self.publishRequested.emit("led/control/sub", "led_off")

    def send_custom(self):
        msg = self.input_box.text().strip()
        if msg:
            self.publishRequested.emit("led/control/sub", msg)

    def update_message_display(self, topic, message):
        if topic == "overobot/2024112805":
            WeatherApp.latest_sensor_data = message
            parsed = WeatherApp.parse_sensor_data(message)
            if parsed:
                temp = parsed.get("temperature", "N/A")
                humidity = parsed.get("humidity", "N/A")
                sensor_text = (
                    f"Sensor Data:\n"
                    f"Temp: {temp}°C\n"
                    f"Humidity: {humidity}%"
                )
            else:
                sensor_text = f"Sensor Data:\n{message}"

            self.sensor_output.setText(sensor_text)

    @staticmethod
    def parse_sensor_data(raw):
        json_string =raw
        data = json.loads(json_string)
        print(data['ID'],"data")
        if isinstance(data, dict):
            return {
                "temperature": data.get("temperature", "N/A"),
                "humidity": data.get("humidity", "N/A")
            }
        return None

    @staticmethod
    def set_latest_sensor_data(data):
        WeatherApp.latest_sensor_data = data

    @staticmethod
    def update_sensor_display(data):
        WeatherApp.set_latest_sensor_data(data)
        print (f"[WeatherApp] Sensor data updated: {data.get('temperature', 'N/A')}°C, ")
        sensor_text = (
            f"Sensor Data:\n"
            f"Temp: {data.get('temperature', 'N/A')}°C\n"
            f"Humidity: {data.get('humidity', 'N/A')}%"
        )
        return sensor_text


    def fetch_weather(self):
        city = self.city_input.text().strip()
        if not city:
            self.sensor_output.setText(f"Sensor Data:\n{WeatherApp.latest_sensor_data}")
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
                    f"Weather in {city}:\n"
                    f"Temp: {temp_c:.1f}°C\n"
                    f"Desc: {description}\n"
                    f"Humidity: {humidity}%\n"
                    f"Wind: {wind_speed} m/s"
                )
            else:
                self.weather_output.setText(f"Error: {data['message']}")
        except Exception as e:
            self.weather_output.setText(f"Request failed: {e}")
