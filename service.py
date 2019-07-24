import flask
import flask_socketio

import bailer

import functools

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)


@app.route("/bailer/socket", methods=['GET'])
def socket_client():
    return flask.render_template('socket_client.html')


@socketio.on('notify_watering')
def handle_notify_watering(data):
    bailer.init_notice()
    bailer.add_notify_callback(start_notify_watering)


def start_notify_watering():
    s = need_watering_list()
    socketio.emit('need_watering', s, broadcast=True)


@app.route("/bailer/need", methods=['GET'])
def need_watering_list():
    l = bailer.need_watering_list()
    if len(l):
        return functools.reduce(lambda acc, item: acc + str(item), l, "")
    else:
        return ""


@app.route("/bailer/add", methods=['POST'])
def add_flower():
    request = flask.request
    interval = request.form['i']
    name = request.form['n']
    bailer.add_flower(name, interval)
    return "True"


@app.route("/bailer/remove/<flowername>", methods=['DELETE'])
def delete(flowername):
    return str(bailer.remove_flower(flowername))


@app.route("/bailer/water/<flowername>", methods=['UPDATE'])
def update(flowername):
    return str(bailer.water_flower(flowername))


if __name__ == "__main__":
    bailer.init_storage()
    app.run(debug=True)
    socketio.run(app)
