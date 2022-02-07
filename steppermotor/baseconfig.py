(ACCELERATOR,STATION)=INSTANCE_CONFIG

SERVERNAME="steppermotorserver"
EXECUTABLE_IN_PACKAGE="/export/doocs/server/steppermotorserver/steppermotorserver"
MAKE_EXECUTABLE="initMotorDriverHW.py"
FILES_TO_SYMLINK_BETWEEN_INSTANCES=""
WORKDIR="/export/doocs/server/"+SERVERNAME
USE_DOOCS_WATCHDOG="true"
SYSTEM_UID="doocsadm"
SYSTEM_GID="doocsadm"
OPERATOR_GID=406
CYCLE_TIME_MS=1000
