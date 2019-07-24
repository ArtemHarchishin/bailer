import threading

def cb():
    print("cb")
    threading.Timer(3, cb).start()

cb()

