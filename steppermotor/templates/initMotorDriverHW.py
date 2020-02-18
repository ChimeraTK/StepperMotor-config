##mako
#!/usr/bin/python3

import mtca4u
import sys

if len(sys.argv) < 3 :
  print("Usage: initMotorDriverHW.py <dMapFileName> <boardAliasName>")
  sys.exit(1)

dMapFileName = sys.argv[1]
deviceName   = sys.argv[2]

print("Performing initialization of device "+deviceName+".")
mtca4u.set_dmap_location(dMapFileName)
device = mtca4u.Device(deviceName)
 
device.write("BOARD/0", "WORD_RESET_N", 1);
