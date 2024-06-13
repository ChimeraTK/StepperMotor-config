##mako
#!/usr/bin/steppermotorserver
${"## Register all support components"}
dbLoadDatabase("../../dbd/ChimeraTK.dbd",0,0)
ChimeraTK_registerRecordDeviceDriver(pdbbase)

${"## Set up ChimeraTKApp application and set polling intervall to 100us"}
chimeraTKConfigureApplication("ChimeraTKApp", 100)

${"## Set up search path for autosave request files"}
#set_requestfile_path("<Path>/")

${"## Set up search path for autosave save files"}
#set_savefile_path("<Path>/")

${"## Load record instances"}
dbLoadRecords("../../db/steppermotorserver.db","P=${STATION},APP=ChimeraTKApp")
dbLoadRecords("../../db/steppermotorserver-motor.db","P=${STATION},APP=ChimeraTKApp")

${"## Set up PV-Restore at boot up. pass0 and pass1 refer to different stages during boot."}
${"## For more information refer to: https://htmlpreview.github.io/?https://github.com/epics-modules/autosave/blob/master/documentation/autoSaveRestore.html#How%20to%20use%20autosave"}
#set_pass0_restoreFile("<FilenameOrPath>.sav")
#set_pass1_restoreFile("<FilenameOrPath>.sav")

${"### autoSaveRestore setup"}
${"## Backup file names contain a datetime stamp if this option is enabled (1)"}
#save_restoreSet_DatedBackupFiles(1)
${"## Debug switch"}
#save_restoreSet_Debug(0)
${"## Tell autosave to maintain x copies of the save file, which are copied in sequence every y seconds"}
#save_restoreSet_NumSeqFiles(<x>)
#save_restoreSet_SeqPeriodInSeconds(<y>)

${"## Initialise the IOC"}
iocInit()

${"## Set up autosave to monitor a set of PV, defined in the request file and every x seconds, if one of the PVs has been posted, makes a save. "}
#create_monitor_set("<FilenameOrPath>.req", <x>)

${"## Set up autosave to periodically save a set of PVs, defined in the request file, and every x seconds. "}
#create_periodic_set("<FilenameOrPath>.req", <x>)

${"## Set up autosave to save a set of PVs, defined in the request file, whenever PV is posted (e.g. changes). "}
#create_triggered_set("<FilenameOrPath>.req", <PV>)

${"## Set up autosave to save a set of PVs, defined in the request file, everytime manual_save(\"<FilenameOrPath>.req\") is executed. "}
#create_manual_set("<FilenameOrPath>.req", <x>)

${"## Start any sequence programs"}
#seq sncllrfctrl,"user=<user>"
