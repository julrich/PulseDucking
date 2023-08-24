#!/usr/bin/python3

import subprocess


class Input:
    def __init__(self, index, name, state, volume):
        self.index = index
        self.name = name
        self.state = state
        self.volume = volume

    def __str__(self):
        return f"{self.name} ({self.index})"


def get():
    def reset():
        index = None
        state = None
        name = None
        volume = None

    reset()
    devices = list()

    data = subprocess.getoutput("pacmd list-sink-inputs")

    for line in data.splitlines()[1:]:
        if "index" in line:
            index = line.split(": ")[1]
        elif "state: " in line:
            state = line.split(": ")[1]
        elif "volume: " in line:
            volume = line.split(": ")[2].split(" /")[0]
        elif "application.name = " in line:
            name = line.split(' = "')[1][:-1]
            devices.append(Input(index, name, state, volume))
            reset()

    return devices


if __name__ == "__main__":
    print(get())
