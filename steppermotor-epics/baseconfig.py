(ACCELERATOR,STATION)=INSTANCE_CONFIG

SERVERNAME=STATION
EXECUTABLE_IN_PACKAGE="/usr/bin/steppermotorserver"
WORKDIR="/var/epics-servers/"+SERVERNAME
FILES_TO_SYMLINK_BETWEEN_INSTANCES=""
MAKE_EXECUTABLE="iocBoot/iocChimeraTKApp/st.cmd iocBoot/iocChimeraTKApp/initMotorDriverHW.py"
CYCLE_TIME_MS=1000
