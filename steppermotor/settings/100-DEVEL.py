if ACCELERATOR == "DEVEL":
    FACILITY = "TEST.DOOCS"
    DEVICE = "MOTOR"

    if STATION == "JG":
        MOTORDRIVER_CFG_FILE = 'Limes122-MotorDriverCardConfig.xml'
        motor_cfg = MotorConfig()
        motor_cfg.add_device('MotorDriver1', 'FMC25_70t', 6, 'controller_pzt4_md22_md22', '6s45_r2261')
        motor_cfg.add_motor('1', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'MD22.0', 0, MOTORDRIVER_CFG_FILE, 'MD22', 0.0003125, 0.000001, 'mm')
