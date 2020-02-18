if ACCELERATOR == "DEVEL.SHOWCASE" :
  if STATION == "DS" :

    RPC_NUMBER=610489684

    MAPFILE_BASENAME="controller_pzt4_unio_md22_fmc25_70t_r"

    MOTORS=["1","2"]
    MOTORDRIVERS=1

    MOTORDRIVER_SLOT=[4]
    MOTORDRIVER_NAME=["MotorDriver1"]

    MOTOR_DRIVER=[MOTORDRIVER_NAME[0], MOTORDRIVER_NAME[0]]
    MOTOR_DRIVERTYPE=["MD22", "MD22"]
    MOTOR_TYPE=["Basic", "LinearMotorWithReferenceSwitch"]
    MOTOR_MODULENAME=["MD22.0", "MD22.0"]
    MOTOR_DRIVERID=[0,1]
    MOTOR_MOTORDRIVERCONFIG=["Limes122-MotorDriverCardConfig.xml", "Limes122-MotorDriverCardConfig.xml"]
    MOTOR_MOTORSTEPSRATIO=[0.0003125, 0.0003125]
    #MOTOR_ENCODERSTEPSRATIO giving as string otherwise python does scientific converstion.
    MOTOR_ENCODERSTEPSRATIO=["0.000001", "0.000001"]
    MOTOR_POSITIONUNIT=["mm", "mm"]
