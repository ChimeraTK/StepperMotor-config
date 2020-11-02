print(ACCELERATOR)
print(STATION)
if ACCELERATOR == "TEST" :
  if STATION == "XLAB1" :

    RPC_NUMBER=610489684

    MAPFILE_BASENAME="controller_pzt4_md22_md22_fmc20_6s45_r"

    MOTORS=["1","2"]
    MOTORDRIVERS=1

    MOTORDRIVER_SLOT=[8]
    MOTORDRIVER_NAME=["MotorDriver1"]

    MOTOR_DRIVER=[MOTORDRIVER_NAME[0], MOTORDRIVER_NAME[0]]
    MOTOR_DRIVERTYPE=["MD22", "MD22"]
    MOTOR_TYPE=["LinearMotorWithReferenceSwitch", "LinearMotorWithReferenceSwitch"]
    MOTOR_MODULENAME=["MD22.0", "MD22.0"]
    MOTOR_DRIVERID=[0,1]
    MOTOR_MOTORDRIVERCONFIG=["motorConfig_2xlimes60_optimal_bam.xml", "motorConfig_2xlimes60_optimal_bam.xml"]
    MOTOR_MOTORSTEPSRATIO=[0.49951, 0.5001]
    #MOTOR_ENCODERSTEPSRATIO giving as string otherwise python does scientific converstion.
    MOTOR_ENCODERSTEPSRATIO=["0.000001", "0.000001"]
    MOTOR_POSITIONUNIT=["mm", "mm"]
