try:
    MOTOR_DRIVERCARD
except:
    MOTOR_DRIVERCARD=[]
    for _ in MOTORS:
        MOTOR_DRIVERCARD.append("BOARD.0")
