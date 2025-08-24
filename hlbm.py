from InquirerPy import inquirer, prompt
import pandas as pd
import csv
import paramiko
import threading
import sys


def interactive_shell(chan):
    while True:
        data = chan.recv(1024)
        if not data:
            break
        sys.stdout.write(data.decode())
        sys.stdout.flush()


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
    name = inquirer.text(message="Enter the name for the new device: ").execute()
    ip = inquirer.text(message="Enter the ip for the new device: ").execute()
    uname = inquirer.text(message="Enter your username for the new device: ").execute()
    passwd = inquirer.text(message="Enter your password for the new device: ").execute()
    new_device = pd.DataFrame([{"NAME": name, "IP": ip, "UNAME": uname, "PASSWD": passwd}])
    new_device.to_csv("devices.csv", mode="a", header=False, index=False)
    print("Device added successfully.")

def view_devices():
    """
    Prints all available devices with name and IP into the terminal.
    """
    devices = get_devices()
    if not devices:
        print("no devices available in the csv file!")
    else:
        for device in devices:
            if device['NAME'] == "NAME":
                continue
            print(f"{device['NAME']} with IP: {device['IP']}")

def establish_connection():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    devices = get_devices()
    choices = []
    for device in devices:
        if device['NAME'] == "NAME":
            continue
        name = device['NAME']
        choices.append(name)
    if not devices:
        print("There are no devices available.")
        return 0
    else:
        target = inquirer.select(
            message = "Which device would you like to connect to?",
            choices = choices
        ).execute()
    for device in devices:
        if device['NAME'] != target:
            continue
        print(f"Establishing a connection with {target}")
        ssh.connect(device['IP'], username=device['UNAME'], password=device['PASSWD'])
    chan = ssh.invoke_shell()

# Start a thread to print remote output
    threading.Thread(target=interactive_shell, args=(chan,), daemon=True).start()

# Send user input to the remote shell
    try:
        while True:
            cmd = sys.stdin.readline()
            if cmd == "exit":
                chan.close()
                ssh.close()
                return 0
            if not cmd:
                break
            chan.send(cmd)
    except KeyboardInterrupt:
        chan.close()
        ssh.close()

def remove_device():
    devices = get_devices()
    choices = []
    for device in devices:
        if device['NAME'] == "NAME":
            continue
        name = device['NAME']
        choices.append(name)
    if not devices:
        print("There are no devices available.")
        return 0
    else:
        target = inquirer.select(
            message = "Which device do you want to remove?",
            choices = choices
        ).execute()
    df = pd.read_csv("devices.csv")
    df = df[df["NAME"] != target]
    df.to_csv("devices.csv", index = False)
    print(f"Removed device {target}")      


def main():
    action = inquirer.select(
        message="What would you like to do?",
        choices=["Add an SSH device", "Establish an SSH connection", "View my SSH devices", "Remove an SSH device"]
    ).execute()
    if action == "Add an SSH device":
        add_device()
    elif action == "View my SSH devices":
        view_devices()
    elif action == "Establish an SSH connection":
        establish_connection()
    elif action == "Remove an SSH device":
        remove_device()

main()