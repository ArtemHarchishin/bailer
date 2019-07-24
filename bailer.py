import collections
import time
import threading


Storage = collections.namedtuple('Storage', 'list, by_id, by_name')
Config = collections.namedtuple('Config', 'notice_interval')


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


storage = None
callbacks = None
notice_process = None
config = Config(3)  # TODO move to file or something else


def init_notice(interval=None):
    global config

    if interval is None:
        interval = config.notice_interval
    else:
        config = config._replace(notice_interval=interval)

    global callbacks

    callbacks = []

    threading.Timer(interval, notify).start()


def init_storage(exists_storage=None):
    global storage

    if exists_storage:
        storage = exists_storage
    else:
        storage = Storage([], {}, collections.defaultdict(list))


def add_notify_callback(cb):
    if callable(cb):
        callbacks.append(cb)
    else:
        raise Exception(F"Callback incorrect - {cb}")


def remove_notify_callback(cb):
    callbacks.remove(cb)


def notify():
    l = need_watering_list()

    need_call = len(l) > 0

    if need_call:
        for cb in callbacks:
            try:
                cb(l)
            except TypeError:
                cb()

    threading.Timer(config.notice_interval, notify).start()


def create_flower_entry(name, watering_interval):
    flower_id = time.time()
    return FlowerEntry(flower_id, name, watering_interval, flower_id)


def add_flower(name, watering_interval):
    if not name:
        raise Exception("Flower's name can't be empty.")

    if isinstance(watering_interval, str):
        watering_interval = float(watering_interval)

    if watering_interval <= 0:
        raise Exception("Watering interval can't be negative or zero.")

    entry = create_flower_entry(name, watering_interval)

    storage.list.append(entry)
    storage.by_id[entry.id] = entry
    storage.by_name[entry.name].append(entry)


def get_all_flowers():
    return storage.list


def remove_flower(name):
    flowers = storage.by_name[name]
    if len(flowers):
        flower = flowers.pop()
        storage.list.remove(flower)
        del storage.by_id[flower.id]
        return True
    return False


def water_flower(name):
    watered = False
    flowers = storage.by_name[name]
    if len(flowers):
        cur_time = time.time()
        for flower in flowers:
            if flower.need_watering(cur_time):
                flower.last_watering = cur_time
                watered = True
                break
    return watered


def need_watering_list():
    cur_time = time.time()
    return [flower for flower in storage.list if flower.need_watering(cur_time)]
