if ACCELERATOR == "MESA" :
  if STATION == "MOTOR" :
    #todo clean up variable such as MOTORDRIVER_CFG_FILE
    MOTORDRIVER_CFG_FILE="mesamotor.xml"
    
    MOTORS=["1", "2", "3", "4"]
    MOTORDRIVERS=1

    MOTORDRIVER_SLOT=[3]
    MOTORDRIVER_NAME=["MotorDriver1"]
    
    MOTOR_DRIVER=[MOTORDRIVER_NAME[0],MOTORDRIVER_NAME[0],MOTORDRIVER_NAME[0],MOTORDRIVER_NAME[0]]
    MOTOR_DRIVERTYPE=["MD22","MD22","MD22","MD22"]
    MOTOR_TYPE=["LinearMotorWithReferenceSwitch", "LinearMotorWithReferenceSwitch", "LinearMotorWithReferenceSwitch", "LinearMotorWithReferenceSwitch"]
    MOTOR_MODULENAME=["MD22.0", "MD22.0", "MD22.1", "MD22.1"]
    MOTOR_DRIVERID=[0,1,0,1]
    MOTOR_MOTORDRIVERCONFIG=[MOTORDRIVER_CFG_FILE, MOTORDRIVER_CFG_FILE, MOTORDRIVER_CFG_FILE, MOTORDRIVER_CFG_FILE]
    MOTOR_MOTORSTEPSRATIO=[1,1,1,1]
    MOTOR_ENCODERSTEPSRATIO=[1,1,1,1]
    MOTOR_POSITIONUNIT=["steps", "steps", "steps", "steps"]
    
    MOTOR1_DRIVER=MOTORDRIVER_NAME[0]
    MOTOR1_DRIVERTYPE="MD22"
    MOTOR1_TYPE="LinearMotorWithReferenceSwitch"
    MOTOR1_MODULENAME="MD22.0"
    MOTOR1_DRIVERID=0
    MOTOR1_MOTORDRIVERCONFIG=MOTORDRIVER_CFG_FILE
    MOTOR1_MOTORSTEPSRATIO=1
    MOTOR1_ENCODERSTEPSRATIO=1
    MOTOR1_POSITIONUNIT="steps"


    MOTOR2_DRIVER=MOTORDRIVER_NAME[0]
    MOTOR2_DRIVERTYPE="MD22"
    MOTOR2_TYPE="LinearMotorWithReferenceSwitch"
    MOTOR2_MODULENAME="MD22.0"
    MOTOR2_DRIVERID=1
    MOTOR2_MOTORDRIVERCONFIG=MOTORDRIVER_CFG_FILE
    MOTOR2_MOTORSTEPSRATIO=1
    MOTOR2_ENCODERSTEPSRATIO=1
    MOTOR2_POSITIONUNIT="steps"


    MOTOR2_DRIVER=MOTORDRIVER_NAME[0]
    MOTOR3_DRIVERTYPE="MD22"
    MOTOR3_TYPE="LinearMotorWithReferenceSwitch"
    MOTOR3_MODULENAME="MD22.1"
    MOTOR3_DRIVERID=0
    MOTOR3_MOTORDRIVERCONFIG=MOTORDRIVER_CFG_FILE
    MOTOR3_MOTORSTEPSRATIO=1
    MOTOR3_ENCODERSTEPSRATIO=1
    MOTOR3_POSITIONUNIT="steps"


    MOTOR2_DRIVER=MOTORDRIVER_NAME[0]
    MOTOR4_DRIVERTYPE="MD22"
    MOTOR4_TYPE="LinearMotorWithReferenceSwitch"
    MOTOR4_MODULENAME="MD22.1"
    MOTOR4_DRIVERID=1
    MOTOR4_MOTORDRIVERCONFIG=MOTORDRIVER_CFG_FILE
    MOTOR4_MOTORSTEPSRATIO=1
    MOTOR4_ENCODERSTEPSRATIO=1
    MOTOR4_POSITIONUNIT="steps"
    
    
    