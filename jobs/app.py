from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/device_data')
def jobs():
    return(render_template('index.html'))