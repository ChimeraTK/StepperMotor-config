if ACCELERATOR == "DEVEL":
    FACILITY = "TEST.DOOCS"
    DEVICE = "MOTOR"

    if STATION == "JG":
        MOTORDRIVER_CFG_FILE = 'Limes122-MotorDriverCardConfig.xml'
        SLOT_NUMBER = 6
        motor_cfg = MotorConfig()
        motor_cfg.add_device('MotorDriver1', 'FMC25_70t', SLOT_NUMBER, 'uni_fmc_pzt4_ctrl', 'md22_md22_2.0.1-0-g162180dd')
        motor_cfg.add_motor('1', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 0, MOTORDRIVER_CFG_FILE, 'MD22', 0.0003125, 0.000001, 'mm')
