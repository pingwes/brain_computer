from key import key
from scroll import scroll
from brainwave import brainwave
import time
from multiprocessing import Process


def key_run(epoch_t):
    key.run(epoch_t)

def scroll_run(epoch_t):
    scroll.run(epoch_t)

def brainwave_run(epoch_t):
    brainwave.run(epoch_t)


epoch_time = str(int(time.time()))

if __name__ == '__main__':

    p1 = Process(target=key_run, args=(epoch_time,))
    p2 = Process(target=scroll_run, args=(epoch_time,))
    p3 = Process(target=brainwave_run, args=(epoch_time,))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
