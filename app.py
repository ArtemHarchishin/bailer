from flask import Flask, jsonify

app = Flask(__name__)

def add_flower(name, watering_interval):
    return (name, watering_interval)

def delete_flower(name):
    pass

def watering_flower(name):
    pass

def what_need_watering():
    pass

if __name__ == "__main__":
    app.run(debug=True)