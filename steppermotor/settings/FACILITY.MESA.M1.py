if ACCELERATOR == "MESA" :
  if STATION == "M1" :

    MOTORS=[1]
    MOTORDRIVERS=1

    MOTORDRIVER_SLOT=[5]
    MOTORDRIVER1_NAME=["MotorDriver1"]

    MOTOR_DRIVER=[MOTORDRIVER_NAME[0]]
    MOTOR_DRIVERTYPE=["MD22"]
    MOTOR_TYPE=["LinearMotorWithReferenceSwitch"]
    MOTOR_MODULENAME=["MD22.0"]
    MOTOR_DRIVERID=[0]
    MOTOR_MOTORDRIVERCONFIG=[MOTORDRIVER_CFG_FILE]
    MOTOR_MOTORSTEPSRATIO=[1]
    MOTOR_ENCODERSTEPSRATIO=[1]
    MOTOR_POSITIONUNIT=["steps"]
