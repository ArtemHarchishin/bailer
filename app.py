from flask import Flask, jsonify
import time
import collections

app = Flask(__name__)

db = ([], {})

FlowerEntry = collections.namedtuple('FlowerEntry', 'id, name, watering_interval, last_watering')

def create_flower_entry(name, watering_interval):
    flower_id = time.time()
    return FlowerEntry(flower_id, name, watering_interval, flower_id)


def add_flower(name, watering_interval):
    entry = create_flower_entry(name, watering_interval)

    db[0].append(entry)
    db[1][entry.id] = entry


def delete_flower(name):
    pass

def watering_flower(name):
    pass

def what_need_watering():
    res = []
    for entry in db[0]:
        next_watering = entry.last_watering + entry.watering_interval
        if next_watering < time.time():
            res.append(entry)
    return res

if __name__ == "__main__":
    app.run(debug=True)