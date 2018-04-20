import queue

def init():
    global messages
    messages = queue.Queue()
    global s
    s = 20
    global els
    els = []
