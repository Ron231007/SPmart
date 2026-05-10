import queue

shared_keypad_queue = queue.Queue()

def clear_queue():
    while not shared_keypad_queue.empty():
        shared_keypad_queue.get_nowait()


def key_pressed(key):
    shared_keypad_queue.put(key)