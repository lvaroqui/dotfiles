#!/usr/bin/python

import subprocess


def defaultSinkName():
    return (
        subprocess.run(["pactl", "get-default-sink"], capture_output=True)
        .stdout.decode()
        .strip()
    )


def allSinks():
    tmp = (
        subprocess.run(["pactl", "list", "short", "sinks"], capture_output=True)
        .stdout.decode()
        .strip()
        .split("\n")
    )
    sinks = []
    for sink in tmp:
        a = sink.split("\t")
        if "hdmi" in a[1]:
            continue
        sinks.append((a[0], a[1]))
    return sinks


def next_sink():
    sinks = allSinks()
    nextSinkIndex = 0
    for i, sink in enumerate(sinks):
        if sink[1] == defaultSinkName():
            nextSinkIndex = i
            break
    else:
        print("error")
        exit

    nextSink = sinks[(nextSinkIndex + 1) % len(sinks)]

    (
        subprocess.run(["pactl", "set-default-sink", nextSink[0]], capture_output=True)
        .stdout.decode()
        .strip()
    )


if __name__ == "__main__":
    next_sink()
