from InquirerPy import inquirer, prompt
import pandas as pd
import csv

def get_devices():
    """
    A method that returns an array filled with the devices 
    present in the csv file. Each Object within the array
    is a dict with the keys IP (ip address), 
    UNAME (username) and PASSWD (password).
    """
    file = open('devices.csv', 'r') 
    devices = [line.strip() for line in file.readlines()]
    keys = ["NAME", "IP", "UNAME", "PASSWD"]
    targets = []
    
    i = 0

    for each in devices:
        current = devices[i]
        vals = next(csv.reader([current]))
        obj = dict(zip(keys, vals))
        i += 1
        targets.append(obj)
    return(targets)

print(get_devices())