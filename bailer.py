import collections
import time
import threading
from flower_entry import FlowerEntry
from storage import Storage

Config = collections.namedtuple('Config', 'notice_interval')


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

    storage.add_entry(entry)

    return True


def get_all_flowers():
    return storage.list


def remove_flower(name):
    return storage.delete_entry_by_name(name)


def water_flower(name):
    watered = False
    flowers = storage.by_name[name]
    if flowers:
        cur_time = time.time()
        for flower in flowers:
            if flower.need_watering(cur_time):
                flower.last_watering = cur_time
                watered = True
                break
    return watered


def water_flower_force(name):
    watered = False
    flowers = storage.by_name[name]
    if flowers:
        cur_time = time.time()
        for flower in flowers:
            flower.last_watering = cur_time
            watered = True
            break
    return watered


def need_watering_list():
    cur_time = time.time()
    return [flower for flower in storage.list if flower.need_watering(cur_time)]
