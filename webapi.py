from flask import Flask, render_template, request
from overdrive import Overdrive
import time

car = None
connected = False
mac_str = None
connection_info = "<p style='color:red'>Not Connected</p>"
connection_now = "options"
current_speed = 0
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', connection=connection_info, speed=current_speed, connection_now=connection_now)

@app.route('/connect', methods=['POST'])
def connect():
    global car, connected, mac_str, connection_info, connection_now, current_speed

    mac_str = request.form['mac']
    if not connected:
        car = Overdrive(mac_str)
        connection_info = f"<p style='color:green'>Connected to {mac_str}</p>"
        connection_now = "all" 
        connected = True
    return render_template('index.html', connection=connection_info, speed=current_speed, connection_now=connection_now)

@app.route('/disconnect')
def disconnect():
    global car, connected, connection_info, connection_now, current_speed

    if connected:
        car.changeSpeed(0, 1000)
        time.sleep(2)
        car.disconnect()
        connection_info = "<p style='color:red'>Not Connected</p>"
        connection_now = "options"
        connected = False
    return render_template('index.html', connection=connection_info, speed=current_speed, connection_now=connection_now)

@app.route('/left')
def left():
    global car, connected, connection_info, connection_now, current_speed

    if connected:
        car.changeLane(1000,1000, -20) 
    return render_template('index.html', connection=connection_info, speed=current_speed, connection_now=connection_now)

@app.route('/right')
def right():
    global car, connected, connection_info, connection_now, current_speed

    if connected:
        car.changeLane(1000,1000, 20) 
    return render_template('index.html', connection=connection_info, speed=current_speed, connection_now=connection_now)

@app.route('/control', methods=['POST'])
def control():
    global car, connected, connection_info, connection_now, current_speed

    if not connected:
        return render_template('index.html', connection=connection_info, speed=current_speed, connection_now=connection_now)

    speed_str = request.form.get('speed')
    current_speed = speed_str
    
    if speed_str is not None:  # Check if speed_str is not None
        try:
            speed = int(speed_str)
            car.changeSpeed(speed, 1000)
        except ValueError:
            return "error"
            pass  # Handle invalid speed input here if needed

    return render_template('index.html', connection=connection_info, speed=current_speed, connection_now=connection_now)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
