if ACCELERATOR == "DEVEL":
    FACILITY = "TEST.DOOCS"
    DEVICE = "MOTOR"

    if STATION == "JG":
        MOTORDRIVER_CFG_FILE = 'Limes122-MotorDriverCardConfig.xml'
        motor_cfg = MotorConfig()
        motor_cfg.add_device('MotorDriver1', 'FMC25_70t', 6, 'uni_fmc_pzt4_ctrl', '2.0.0-0-g4e1f23e1')
        motor_cfg.add_motor('1', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'FMC1', 0, MOTORDRIVER_CFG_FILE, 'MD22', 0.0003125, 0.000001, 'mm')