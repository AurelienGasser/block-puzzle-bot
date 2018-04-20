
class InputThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global s
        while True:
            txt = input()
            print(txt)
            s = (int)(txt)