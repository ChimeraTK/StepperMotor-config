#!/usr/bin/python3

import deviceaccess as da
import sys

if len(sys.argv) < 4:
    print("Usage: initMotorDriverHW.py <dMapFileName> <boardAliasName> <bspName>")
    sys.exit(1)

dMapFileName = sys.argv[1]
deviceName = sys.argv[2]
bspName = sys.argv[3]

da.setDMapFilePath(dMapFileName)

print("Performing initialization of device "+deviceName+".")
device = da.Device(deviceName)
device.open()


if device.read(f"{bspName}.WORD_RESET_N") == 0:
    device.write(f"{bspName}.WORD_RESET_N", 1)
