from InquirerPy import inquirer, prompt
import pandas as pd
import csv

def get_devices():
    """
    A method that returns an array filled with the devices 
    present in the csv file. Each Object within the array
    is a dict with the keys NAME (name of device), IP (ip address), 
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

def get_device_info(name, key):
    devices = get_devices
    for device in devices:
        if device.NAME == name:
            if key == "NAME" or key == "name":
                return device.NAME
            if key == "IP" or key == "ip":
                return device.IP
            if key == "UNAME" or key == "uname":
                return device.UNAME
            if key == "PASSWD" or key == "passwd" or key == "psk":
                return device.PASSWD
            else:
                raise ValueError("Please use a valid key for method get_device_info!")
    raise ValueError("Specified device was not found!")

def add_device():
    """
    A method that lets the user add a device to the csv file 
    (devices.csv) via an interactive shell.
    """
    
