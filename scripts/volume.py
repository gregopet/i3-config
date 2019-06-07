#!/usr/bin/env python
import os
import re

volumeLine = re.compile('^\s*volume:')
percentage = re.compile('[0-9]+%')
sinkIndex = re.compile('[*] index: ([0-9]+)')

def containsVolume(line):
    match = volumeRegexp.match(line)
    if match == None:
        return False
    else:
        return "lol"

def isMuted(config):
    return config.find('muted: yes') != -1

def outputVolume(config):
    strikethrough = "true" if isMuted(config) else "false"
    volPerc = percentage.search(next(vol for vol in config.splitlines() if volumeLine.match(vol))).group(0)
    print(f"<span strikethrough='{strikethrough}'>{volPerc}</span>")

def getSinkIndex(config):
    return sinkIndex.search(config).group(1)

def changeVolume(config):
    button = str(os.environ.get("BLOCK_BUTTON"))
    if str(button) == '1':
        firstSink = getSinkIndex(config)
        newMute = "0" if isMuted(config) else "1"
        os.popen(f"pactl set-sink-mute {firstSink} {newMute}").read()
        return True
    if str(button) == '4':
        firstSink = getSinkIndex(config)
        os.popen(f"pactl set-sink-volume {firstSink} +7%").read()
        return True
    if str(button) == '5':
        firstSink = getSinkIndex(config)
        os.popen(f"pactl set-sink-volume {firstSink} -7%").read()
        return True
    return False
    
configBlock = os.popen("/usr/bin/pacmd list-sinks").read()
if changeVolume(configBlock):
    configBlock = os.popen("/usr/bin/pacmd list-sinks").read()
outputVolume(configBlock)