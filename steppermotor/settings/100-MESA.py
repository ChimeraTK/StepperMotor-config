if ACCELERATOR == 'MESA':
    FACILITY = "MESA.ACTUATOR"
    DEVICE = "MOTOR"

    SLOT_NUMBER = 5

    if STATION == 'LLRF':
        motor_cfg = MotorConfig()
        motor_cfg.add_device('MotorDriver1', 'FMC20', SLOT_NUMBER, 'uni_fmc_pzt4_ctrl', 'md22_md22_2.0.1-0-g162180dd')
        motor_cfg.add_motor('M1', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 0, 'mesamotor.xml')
        motor_cfg.add_motor('M2', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 1, 'mesamotor.xml')
        motor_cfg.add_motor('M3', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 0, 'mesamotor.xml')
        motor_cfg.add_motor('M4', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 1, 'mesamotor.xml')
