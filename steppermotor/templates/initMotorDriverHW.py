#!/usr/bin/python3

import mtca4u
import sys

if len(sys.argv) < 4 :
  print("Usage: initMotorDriverHW.py <dMapFileName> <boardAliasName> <bspName>")
  sys.exit(1)

dMapFileName = sys.argv[1]
deviceName   = sys.argv[2]
bspName = sys.argv[3]

print("Performing initialization of device "+deviceName+".")
mtca4u.set_dmap_location(dMapFileName)
device = mtca4u.Device(deviceName)
 
if device.read(bspName, "WORD_RESET_N") == 0:
    device.write(bspName, "WORD_RESET_N", 1);
