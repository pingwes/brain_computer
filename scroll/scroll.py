from pynput.mouse import Listener
import time
charCount = 0
keys = []
import sys


original_stdout = sys.stdout # Save a reference to the original standard output

def run(epoch_time):
    print("scroll running")
    with open('scroll/data/' + epoch_time + '.log', 'w') as f:
        sys.stdout = f # Change the standard output to the file we created.

        def on_click(x, y, button, pressed):
            current_time = str(time.time())
            sys.stdout = f  # Change the standard output to the file we created.
            if pressed:
                print('{ "input": "click_press", "time": ' + current_time + ', "location": [' + str(x) + ',' + str(y) + ']}')
                sys.stdout = original_stdout  # Reset the standard output to its original value
                print('{ "input": "click_press", "time": ' + current_time + ', "location": [' + str(x) + ',' + str(y) + ']}')
            else:
                print('{ "input": "click_released", "time": ' + current_time + ', "location": [' + str(x) + ',' + str(y) + ']}')
                sys.stdout = original_stdout  # Reset the standard output to its original value
                print('{ "input": "click_released", "time": ' + current_time + ', "location": [' + str(x) + ',' + str(y) + ']}')

        def on_scroll(x, y, dx, dy):
            current_time = str(time.time())

            sys.stdout = f  # Change the standard output to the file we created.
            if dy < 0:
                print('{ "input": "scroll_down", "time": ' + current_time + ',"location": [' + str(x) + ',' + str(y) + ']}')
            elif dy > 0:
                print('{ "input": "scroll_up", "time": ' + current_time + ', "location": [' + str(x) + ',' + str(y) + ']}')
            sys.stdout = original_stdout  # Reset the standard output to its original value
            if dy < 0:
                print('{ "input": "scroll_down", "time": ' + current_time + ', "location": [' + str(x) + ',' + str(y) + ']}')
            elif dy > 0:
                print('{ "input": "scroll_up", "time": ' + current_time + ',"location": [' + str(x) + ',' + str(y) + ']}')

        # Collect events until released
        with Listener(
                on_click=on_click,
                on_scroll=on_scroll) as listener:
            listener.join()