# handlers.py
def handle_led(topic, payload):
    print(f"[LED Handler] Topic: {topic} | Payload: {payload}")
    if payload == "led_on":
        print("LED should be turned ON.")
    elif payload == "led_off":
        print("LED should be turned OFF.")
    else:
        print("Unknown LED command.")

def handle_sensor(topic, payload):
    print(f"[Sensor Handler] Topic: {topic} | Data: {payload}")

def handle_motor(topic, payload):
    print(f"[Motor Handler] Topic: {topic} | Command: {payload}")
