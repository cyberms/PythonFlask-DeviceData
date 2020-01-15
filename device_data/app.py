import eventlet
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO

PATH= 'db/jobs.sqlite'

eventlet.monkey_patch()

app = Flask(__name__, template_folder='./templates')
app.config['MQTT_BROKER_URL'] = '47.97.228.120'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0

mqtt = Mqtt(app)
socketio = SocketIO(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('application/#')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    # emit a mqtt_message event to the socket containing the message data
    socketio.emit('mqtt_message', data=data)

@app.route('/')
def index():
    return render_template('graph.html')

@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)

socketio.run(app, host='localhost', port=5000, use_reloader=True, debug=True)


# @app.route('/')
# @app.route('/device_pressure')
# def read_device_pressure():
    
#     return(render_template('index.html', jobs=jobs))