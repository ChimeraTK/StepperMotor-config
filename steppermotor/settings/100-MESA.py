if ACCELERATOR == 'MESA':
    FACILITY = "MESA.ACTUATOR"
    DEVICE = "MOTOR"

    if STATION == 'LLRF':
        motor_cfg = MotorConfig()
        motor_cfg.add_device('MotorDriver1', 'FMC20', 5, 'controller_pzt4_md22_md22', '6s45_r2261')
        motor_cfg.add_motor('M1', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'MD22.0', 0, 'mesamotor.xml')
        motor_cfg.add_motor('M2', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'MD22.0', 1, 'mesamotor.xml')
        motor_cfg.add_motor('M3', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'MD22.1', 0, 'mesamotor.xml')
        motor_cfg.add_motor('M4', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'MD22.1', 1, 'mesamotor.xml')