import eventlet, json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from random import seed
from random import randint
import base64, datetime

# seed random number generator
seed(1)

eventlet.monkey_patch()

app = Flask(__name__, template_folder='./templates')
app.config['MQTT_BROKER_URL'] = 'localhost'
#app.config['MQTT_BROKER_URL'] = '47.97.228.120'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_REFRESH_TIME'] = 1.0

mqtt = Mqtt(app)
socketio = SocketIO(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('application/#')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):

    json_event= json.loads(message.payload.decode())

    # print("data {0}".format(json_event.get('data')))

    if json_event.get('data') == 'ZGV2aWNlTm90SGE=':
        pressure_reading = randint(60, 70)
    else:
        pressure_reading = int(base64.b64decode(json_event.get('data')))
        print("Pressure reading: {0}".format(pressure_reading))
        #pressure_reading = randint(60, 80)

    data = dict(
            topic=message.topic,
            pressure_reading=pressure_reading,
            datetime= datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            device= json_event.get('devEUI')
            )

    # emit a mqtt_message event to the socket containing the message data
    socketio.emit('mqtt_message', data=data)

@app.route('/device_pressure')
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