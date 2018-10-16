import re

from adb_android import adb_android

adb_android.wait_for_device()

BlockListTable = adb_android.shell("ls -l /dev/block/platform/soc/c0c4000.sdhci/by-name ")
BlockListArray = BlockListTable[1].split("\n")
BlockListArray.pop()
BlockListArray.pop(0)
ListNameBlocks = []
while len(BlockListArray) > 0:
    regex = r"\W([a-z_]+)\W\W+(\/dev\/block\/[a-z0-9]+)"
    line = BlockListArray.pop()
    matches = re.finditer(regex, line, re.MULTILINE)
    for matchNum, match in enumerate(matches):
        matchNum = matchNum + 1
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            print ("Found {groupNum} - {group}".format(groupNum = groupNum, group = match.group(groupNum)))
