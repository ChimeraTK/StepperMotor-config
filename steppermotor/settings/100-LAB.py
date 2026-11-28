if ACCELERATOR == "LAB":
    if STATION == "LAMDEV1":
        FACILITY = f"{ACCELERATOR}.SYNC"

        SLOT_NUMBER = 3

        EXPERT_GID = 1432  # msk

        ROTATIONAL_STAGE_CFG_FILE = "2xStanda8MR20-F10_0.2A_320spr_120rpm.xml"
        LINEAR_STAGE_CFG_FILE     = "2xNEMA_0.55A_200spr_480rpm_ES.xml"

        motor_cfg = MotorConfig()
        motor_cfg.add_device('MotorDriver1', 'FMC20', SLOT_NUMBER, 'uni_fmc_pzt4_ctrl', 'md22_md22_2.0.1-0-g162180dd')
        motor_cfg.add_motor('LAMDEV1.CRYSTAL.FWD', 'RotationalMotorWithCentreSwitch', 'MotorDriver1', 0, ROTATIONAL_STAGE_CFG_FILE, 'MD22', 0.0023, 1, 'deg')
        motor_cfg.add_motor('LAMDEV1.CRYSTAL.BWD', 'RotationalMotorWithCentreSwitch', 'MotorDriver1', 1, ROTATIONAL_STAGE_CFG_FILE, 'MD22', 0.0023, 1, 'deg')
        motor_cfg.add_motor('LAMDEV1.ATTENUATOR',      'LinearMotorWithReferenceSwitch', 'MotorDriver1', 0, LINEAR_STAGE_CFG_FILE, 'MD22', 0.5, 1, 'mm')
        motor_cfg.add_motor('LAMDEV1.SPECTRAL_FILTER', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 1, LINEAR_STAGE_CFG_FILE, 'MD22', 0.5, 1, 'mm')

    elif STATION == "LAMDEV2":
        FACILITY = f"{ACCELERATOR}.SYNC"

        SLOT_NUMBER = 3

        EXPERT_GID = 1432  # msk

        LBSYNC_ODL_CFG_FILE = "2xLbSync-ODL_0.55A_400spr_250rpm_invES_chopper.xml"

        motor_cfg = MotorConfig()
        motor_cfg.add_device('MotorDriver1', 'FMC20', SLOT_NUMBER, 'uni_fmc_pzt4_ctrl', 'md22_md22_2.0.1-0-g162180dd')
        motor_cfg.add_motor('LAMDEV2.LBSYNC_ODL.1', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 0, LBSYNC_ODL_CFG_FILE, 'MD22', 1/500, 1.0, 'ps')
        motor_cfg.add_motor('LAMDEV2.LBSYNC_ODL.2', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 1, LBSYNC_ODL_CFG_FILE, 'MD22', 1/500, 1.0, 'ps')
        motor_cfg.add_motor('LAMDEV2.LBSYNC_ODL.3', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 0, LBSYNC_ODL_CFG_FILE, 'MD22', 1/500, 1.0, 'ps')
        motor_cfg.add_motor('LAMDEV2.LBSYNC_ODL.4', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 1, LBSYNC_ODL_CFG_FILE, 'MD22', 1/500, 1.0, 'ps')


    elif STATION == "26A2":
        FACILITY = f"{ACCELERATOR}.SYNC"

        SLOT_NUMBER = 3

        EXPERT_GID = 1432  # msk

        LBSYNC_ODL_CFG_FILE = "2xLbSync-ODL_0.55A_400spr_250rpm_invES_chopper.xml"

        motor_cfg = MotorConfig()
        motor_cfg.add_device('MotorDriver1', 'FMC20', SLOT_NUMBER, 'uni_fmc_pzt4_ctrl', 'md22_md22_2.0.1-0-g162180dd')
        motor_cfg.add_motor('26A2.LBSYNC_ODL.1', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 0, LBSYNC_ODL_CFG_FILE, 'MD22', 1/500, 1.0, 'ps')
        motor_cfg.add_motor('26A2.LBSYNC_ODL.2', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 1, LBSYNC_ODL_CFG_FILE, 'MD22', 1/500, 1.0, 'ps')
        motor_cfg.add_motor('26A2.LBSYNC_ODL.3', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 0, LBSYNC_ODL_CFG_FILE, 'MD22', 1/500, 1.0, 'ps')
        motor_cfg.add_motor('26A2.LBSYNC_ODL.4', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 1, LBSYNC_ODL_CFG_FILE, 'MD22', 1/500, 1.0, 'ps')
