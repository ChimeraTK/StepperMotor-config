print(ACCELERATOR)
print(STATION)
if ACCELERATOR == "LAB" :

  SERVERNAME="steppermotor_"+STATION+"_server"
  SVR_LOCATION=HOSTNAME.upper()+"."+STATION+"._SVR"
  FACILITY="LAB.SYNC"
  DEVICE="EXP.ODL.MOTOR"
  WATCHDOG_ADDRESS="LAB.SYSTEM/"+HOSTNAME.upper()+".WATCH/SVR.STEPPERMOTOR_"+STATION

  if STATION == "26A2" :

    RPC_NUMBER=610489684

    MAPFILE_BASENAME="controller_pzt4_md22_md22_fmc20_6s45_r"
    FIRMWARE_REV_MOTDRV ="2261"

    MOTORS=["1","2", "3", "4"]
    MOTORDRIVERS=1

    MOTORDRIVER_SLOT=[3]
    MOTORDRIVER_NAME=["MotorDriver1"]

    MOTOR_DRIVER=[MOTORDRIVER_NAME[0],MOTORDRIVER_NAME[0],MOTORDRIVER_NAME[0],MOTORDRIVER_NAME[0]]
    MOTOR_DRIVERTYPE=["MD22","MD22","MD22","MD22"]

    MOTOR_TYPE=["LinearMotorWithReferenceSwitch", "LinearMotorWithReferenceSwitch", "LinearMotorWithReferenceSwitch", "LinearMotorWithReferenceSwitch"]
    MOTOR_MODULENAME=["MD22.0", "MD22.0", "MD22.1", "MD22.1"]
    MOTOR_DRIVERID=[0,1,0,1]
    MOTOR_MOTORDRIVERCONFIG=["ODL-0.9A_400FS_250rpm_acc100ms_16us_32MHz_endsw_inv_chopper-tuned.xml", "ODL-0.9A_400FS_250rpm_acc100ms_16us_32MHz_endsw_inv_chopper-tuned.xml", "ODL-0.9A_400FS_250rpm_acc100ms_16us_32MHz_endsw_inv_chopper-tuned.xml", "ODL-0.9A_400FS_250rpm_acc100ms_16us_32MHz_endsw_inv_chopper-tuned.xml"]
    MOTOR_MOTORSTEPSRATIO=[0.5, 0.5, 0.5, 0.5]
    #MOTOR_ENCODERSTEPSRATIO giving as string otherwise python does scientific converstion.
    MOTOR_ENCODERSTEPSRATIO=["0.000001", "0.000001", "0.000001", "0.000001"]
    MOTOR_POSITIONUNIT=["mm", "mm", "mm", "mm"]
    
  if STATION == "26A1" :

    RPC_NUMBER=610489684

    MAPFILE_BASENAME="controller_pzt4_md22_md22_fmc20_6s45_r"
    FIRMWARE_REV_MOTDRV ="2261"

    MOTORS=["1","2", "3", "4"]
    MOTORDRIVERS=1

    MOTORDRIVER_SLOT=[6]
    MOTORDRIVER_NAME=["MotorDriver1"]

    MOTOR_DRIVER=[MOTORDRIVER_NAME[0],MOTORDRIVER_NAME[0],MOTORDRIVER_NAME[0],MOTORDRIVER_NAME[0]]
    MOTOR_DRIVERTYPE=["MD22","MD22","MD22","MD22"]

    MOTOR_TYPE=["LinearMotorWithReferenceSwitch", "LinearMotorWithReferenceSwitch", "LinearMotorWithReferenceSwitch", "LinearMotorWithReferenceSwitch"]
    MOTOR_MODULENAME=["MD22.0", "MD22.0", "MD22.1", "MD22.1"]
    MOTOR_DRIVERID=[0,1,0,1]
    MOTOR_MOTORDRIVERCONFIG=["ODL-0.9A_400FS_250rpm_acc100ms_16us_32MHz_endsw_inv_chopper-tuned.xml", "ODL-0.9A_400FS_250rpm_acc100ms_16us_32MHz_endsw_inv_chopper-tuned.xml", "ODL-0.9A_400FS_250rpm_acc100ms_16us_32MHz_endsw_inv_chopper-tuned.xml", "ODL-0.9A_400FS_250rpm_acc100ms_16us_32MHz_endsw_inv_chopper-tuned.xml"]
    MOTOR_MOTORSTEPSRATIO=[0.5, 0.5, 0.5, 0.5]
    #MOTOR_ENCODERSTEPSRATIO giving as string otherwise python does scientific converstion.
    MOTOR_ENCODERSTEPSRATIO=["0.000001", "0.000001", "0.000001", "0.000001"]
    MOTOR_POSITIONUNIT=["mm", "mm", "mm", "mm"]        
