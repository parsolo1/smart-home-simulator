from flask import Flask, render_template, request, jsonify
import threading, time, random

app = Flask(__name__)

devices = {
    "light": False,
    "fan": False,
    "door": False,
    "temperature": 28
}

# 🧩 Background thread to simulate temperature changes
def auto_update_temperature():
    while True:
        time.sleep(3)  # update every 3 seconds

        # Simulate effect of devices
        if devices["fan"]:
            devices["temperature"] -= random.uniform(0.2, 0.5)  # fan cools down
        if devices["light"]:
            devices["temperature"] += random.uniform(0.1, 0.3)  # light heats slightly
        if devices["door"]:
            devices["temperature"] += random.uniform(-0.3, 0.3)  # open door: random effect

        # Keep temperature realistic
        devices["temperature"] = round(max(18, min(devices["temperature"], 35)), 1)

# Start background simulation thread
threading.Thread(target=auto_update_temperature, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html', devices=devices)

@app.route('/toggle/<device>', methods=['POST'])
def toggle_device(device):
    if device in devices and isinstance(devices[device], bool):
        devices[device] = not devices[device]
    return jsonify(devices)

@app.route('/temperature', methods=['GET'])
def get_temperature():
    return jsonify({"temperature": devices["temperature"]})

if __name__ == '__main__':
    app.run(debug=True)
