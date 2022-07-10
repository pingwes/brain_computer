import json
import os
import pandas as pd
import shutil

labeling_directory = os.listdir('data')

channels = ["CP3", "C3", "F5", "PO3", "PO4", "F6", "C4", "CP4"]
header = [(channel + '_' + str(i)) for channel in channels for i in range(0, 16)]

header.append("label")
df = pd.DataFrame(columns=header,)

bw_dir = '../brainwave/data'
key_dir = '../key/data'
scroll_dir = '../scroll/data'

def matrices_to_row(data):
    row = []
    for matrix in data:
        for vector in matrix:
            row.append(vector)
    return row

def create_label(string):
    string = string.lower()
    if string == "key.down" or string == "scroll_down":
        return "down"
    elif string == "key.up" or string == "scroll_up":
        return "up"
    else:
        return "neutral"


def load_list(dataset):
    obj_list = []
    for data in dataset:
        obj = json.loads(data)
        obj_list.append(obj)

    return obj_list


def label_data(bw_data,scroll_data,key_data):

    bw_objs = load_list(bw_data)
    scroll_objs = load_list(scroll_data)
    key_objs = load_list(key_data)

    for bw_obj in bw_objs:
        bw_time = bw_obj["info"]["startTime"] / 1000

        for scroll_obj in scroll_objs:
            scroll_time = scroll_obj["time"]

            if abs(bw_time - scroll_time) < .1:
                scroll_objs.remove(scroll_obj)

                row = matrices_to_row(bw_obj["data"])
                label = create_label(scroll_obj['input'])
                if label:
                    row.append(label)
                    df.loc[len(df.index)] = row
                break
            else:
                if len(df.query('label == "neutral"')) <  len(df.query('label == "down"')):
                    row = matrices_to_row(bw_obj["data"])
                    row.append("neutral")
                    df.loc[len(df.index)] = row


    neutral_count = len(df.query('label == "neutral"'))
    down_count = len(df.query('label == "down"'))
    up_count = len(df.query('label == "up"'))
    data = df.drop(df.query('label == "neutral"').sample(frac=1-(down_count/neutral_count)).index)
    if up_count > 0: data = df.drop(df.query('label == "up"').sample(frac=1 - (down_count / up_count)).index)

    return data

for filename in os.listdir(bw_dir):

    file = os.path.join(bw_dir, filename)
    if not os.path.isfile(file): continue

    bw_data = open(bw_dir + '/' + filename, "r")
    scroll_data = open(scroll_dir + '/' + filename, "r")
    key_data = open(key_dir + '/' + filename, "r")

    data = label_data(bw_data,scroll_data,key_data)

    shutil.move(bw_dir + '/' + filename, bw_dir + '/archive/' + filename)
    shutil.move(scroll_dir + '/' + filename, scroll_dir + '/archive/' + filename)
    shutil.move(key_dir + '/' + filename, key_dir + '/archive/' + filename)

    data.to_pickle("data/data" + str(len(labeling_directory)) + ".pkl")

