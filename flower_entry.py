import time

class FlowerEntry(object):
    def __init__(self, id, name, watering_interval, last_watering):
        self.id = id
        self.name = name
        self.watering_interval = watering_interval
        self.last_watering = last_watering

    def need_watering(self, cur_time=None):
        if cur_time is None:
            cur_time = time.time()
        next_watering = self.last_watering + self.watering_interval
        return cur_time > next_watering

    def to_string(self):
        return F"({self.name}, interval: {self.watering_interval}, last: {self.last_watering})"

    def __repr__(self):
        return self.to_string()

    def __str__(self):
        return self.to_string()