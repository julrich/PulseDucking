import math
import json
import subprocess
import inputs

with open("config.json", "r") as f:
    config = json.load(f)

duckPercent = int(config["preferences"]["duckByPercent"]) or 50
# TODO read current volume value from sink to duck based on that
FULL_VOLUME = math.floor(65536 * 0.8)


def onPlayStateChange(playing):
    inputsList = inputs.get()
    namesToDuck = [a["name"] for a in config["applications"] if a["role"] == "slave"]
    inputsToDuck = [i for i in inputsList if i.name in namesToDuck]

    volume = (
        math.floor(FULL_VOLUME * ((100 - duckPercent) / 100))
        if playing
        else FULL_VOLUME
    )
    for input in inputsToDuck:
        # TODO don't set immediately (jarring), but ramp to target volume
        r = subprocess.check_output(
            ["pacmd", "set-sink-input-volume", str(input.index), str(volume)]
        )
