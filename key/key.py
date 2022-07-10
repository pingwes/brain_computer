import pynput
from pynput.keyboard import Key, Listener
import time
charCount = 0
keys = []
import csv
import sys

original_stdout = sys.stdout # Save a reference to the original standard output

def run(epoch_time):
    print("key running")
    with open('key/data/' + epoch_time + '.log', 'w') as f:

        def onKeyPress(key):
            sys.stdout = f  # Change the standard output to the file we created.

            try:
                sys.stdout = f  # Change the standard output to the file we created.
                current_time = str(time.time())
                if not str(key) == '"' or not str(key) == "'":
                    print('{ "input": "key_pressed", "key": "' + str(key) + '", "time": ' + current_time + '}')
                    sys.stdout = original_stdout
                    print('{ "input": "key_pressed", "key": "' + str(key) + '", "time": ' + current_time + '}')
            except Exception as ex:
                print('There was an error : ',ex)

        def onKeyRelease(key):
            current_time = str(int(time.time()))

            sys.stdout = f  # Change the standard output to the file we created.
            if not str(key) == '"' or not str(key) == "'":
                print('{ "input": "key_released", "key": "' + str(key) + '", "time": ' + current_time + '}')
                sys.stdout = original_stdout
                print('{ "input": "key_released", "key": "' + str(key) + '", "time": ' + current_time + '}')

        with Listener(on_press=onKeyPress,\
            on_release=onKeyRelease) as listener:
            listener.join()
