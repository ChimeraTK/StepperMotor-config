if ACCELERATOR == "LAB":
    if STATION == "LAMDEV":
        FACILITY = f"{ACCELERATOR}.SYNC"
        DEVICE = "LAM.FE"
        EXPERT_UID   = 20732 # lbsync
        EXPERT_GID   = 7273  # msk_lbsync
        OPERATOR_GID = 1432  # msk

        ROTATIONAL_STAGE_CFG_FILE = "2xStanda8MR20-F10_0.45A_320_120_8_32MHz_ES_inv_defaults.xml"
        LINEAR_STAGE_CFG_FILE     = "2xNEMA_1.2A_200_480_16_32MHz_ES_defaults.xml"

        motor_cfg = MotorConfig()
        motor_cfg.add_device('MotorDriver1', 'FMC20', 3, 'uni_fmc_pzt4_ctrl', 'md22_md22_2.0.0-2-g17258df0')
        motor_cfg.add_motor('1', 'RotationalMotorWithCentreSwitch', 'MotorDriver1', 'FMC1', 0, ROTATIONAL_STAGE_CFG_FILE, 'MD22', 0.0023, 1, 'deg')
        motor_cfg.add_motor('2', 'RotationalMotorWithCentreSwitch', 'MotorDriver1', 'FMC1', 1, ROTATIONAL_STAGE_CFG_FILE, 'MD22', 0.0023, 1, 'deg')
        motor_cfg.add_motor('3', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'FMC2', 0, LINEAR_STAGE_CFG_FILE, 'MD22', 0.5, 1, 'mm')
        motor_cfg.add_motor('4', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'FMC2', 1, LINEAR_STAGE_CFG_FILE, 'MD22', 0.5, 1, 'mm')

    if STATION == "26A2":
        FACILITY = f"{ACCELERATOR}.SYNC"
        DEVICE = "ODL"
        EXPERT_UID   = 20732 # lbsync
        EXPERT_GID   = 7273  # msk_lbsync
        OPERATOR_GID = 1432  # msk

        LBSYNC_ODL_CFG_FILE = "ODL-0.9A_400FS_250rpm_acc100ms_16us_32MHz_chopper-tuned.xml"

        motor_cfg = MotorConfig()
        motor_cfg.add_device('MotorDriver1', 'FMC20', 3, 'uni_fmc_pzt4_ctrl', 'md22_md22_2.0.0-2-g17258df0')
        motor_cfg.add_motor('1', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'FMC1', 0, LBSYNC_ODL_CFG_FILE, 'MD22')
        motor_cfg.add_motor('2', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'FMC1', 1, LBSYNC_ODL_CFG_FILE, 'MD22')
        motor_cfg.add_motor('3', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'FMC2', 0, LBSYNC_ODL_CFG_FILE, 'MD22')
        motor_cfg.add_motor('4', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'FMC2', 1, LBSYNC_ODL_CFG_FILE, 'MD22')