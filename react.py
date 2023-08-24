import math
import json
import subprocess
import inputs
import time

fullVolume = 65536
volumesOriginal = dict()


def current_milli_time():
    return int(time.time() * 1000)


def onPlayStateChange(playing):
    with open("config.json", "r") as f:
        config = json.load(f)

    duckPercent = int(config["preferences"]["duckByPercent"]) or 50
    duckRamp = int(config["preferences"]["rampUpMs"])

    inputsList = inputs.get()

    namesToDuck = [a["name"]
                   for a in config["applications"] if a["role"] == "slave"]
    inputsToDuck = [i for i in inputsList if i.name in namesToDuck]

    starttime = current_milli_time()
    elapsedtime = 0

    while elapsedtime < duckRamp:
        elapsedtime = current_milli_time() - starttime
        time.sleep(0.01)
        for input in inputsToDuck:
            if playing:
                volumesOriginal[input.index] = int(input.volume)
                duckedVolumeDifference = math.floor(
                    volumesOriginal[input.index]
                    - ((100 - duckPercent) / 100 *
                       volumesOriginal[input.index])
                )
                volume = min(
                    math.floor(
                        volumesOriginal[input.index]
                        - (duckedVolumeDifference * (elapsedtime / duckRamp))
                    ),
                    fullVolume,
                )
            else:
                volumeStart = int(input.volume)
                if input.index in volumesOriginal:
                    volume = min(
                        math.floor(
                            volumesOriginal[input.index]
                            - (
                                (volumesOriginal[input.index] - volumeStart)
                                * (1 - (elapsedtime / duckRamp))
                            )
                        ),
                        fullVolume,
                    )
                else:
                    volume = int(input.volume)
            r = subprocess.check_output(
                ["pacmd", "set-sink-input-volume",
                    str(input.index), str(volume)]
            )
