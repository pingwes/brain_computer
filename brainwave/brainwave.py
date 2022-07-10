from neurosity import neurosity_sdk
from dotenv import load_dotenv
import os
import sys

load_dotenv()
neurosity = neurosity_sdk({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID"),
})
neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

original_stdout = sys.stdout

def print_data(data):
    print('{"data": ' + str(data['data']) +
          ', "info": { "channelNames": ["CP3", "C3", "F5", "PO3", "PO4", "F6", "C4", "CP4"], "notchFrequency": ' +
          ' "' + str(data['info']['notchFrequency']) + '"' +
          ',"samplingRate":' + str(data['info']['samplingRate']) +
          ', "startTime": ' + str(data['info']['startTime']) +
          '}, "label": "' + str(data['label']) + '"}')


def run(epoch_time):
    f = open('brainwave/data/' + epoch_time + '.log', 'w')

    def callback(data):
        if data != None:
            sys.stdout = f  # Change the standard output to the file we created.
            print_data(data)
            sys.stdout = original_stdout  # Reset the standard output to its original value
            print_data(data)

    neurosity.brainwaves_raw(callback)