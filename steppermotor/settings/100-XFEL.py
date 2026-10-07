if ACCELERATOR == "XFEL":
    if DEVICE == "LAM.ACT.EXP":
        FACILITY = f"{ACCELERATOR}.SYNC"

        SLOT_NUMBER = 3

        EXPERT_GID = 516  # `xfelsync` (XFEL LbSync)

        ROTATIONAL_STAGE_CFG_FILE = "2xStanda8MR20-F10_0.45A_320_120_8_32MHz_ES_inv_defaults.xml"
        LINEAR_STAGE_CFG_FILE     = "2xNEMA_1.2A_200_480_16_32MHz_ES_defaults.xml"

        motor_cfg = MotorConfig()
        motor_cfg.add_device('MotorDriver1', 'FMC20', SLOT_NUMBER, 'uni_fmc_pzt4_ctrl', 'md22_md22_2.0.0-2-g17258df0')
        motor_cfg.add_motor('CRYSTAL.FWD', 'RotationalMotorWithCentreSwitch', 'MotorDriver1', 'FMC1', 0, ROTATIONAL_STAGE_CFG_FILE, 'MD22', 0.0023, 1, 'deg')
        motor_cfg.add_motor('CRYSTAL.BWD', 'RotationalMotorWithCentreSwitch', 'MotorDriver1', 'FMC1', 1, ROTATIONAL_STAGE_CFG_FILE, 'MD22', 0.0023, 1, 'deg')
        motor_cfg.add_motor('ATTENUATOR',      'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'FMC2', 0, LINEAR_STAGE_CFG_FILE, 'MD22', 0.5, 1, 'mm')
        motor_cfg.add_motor('SPECTRAL_FILTER', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'FMC2', 1, LINEAR_STAGE_CFG_FILE, 'MD22', 0.5, 1, 'mm')

        match STATION:
            case 'XHEXP1.FXE.ILH':
                CUSTOMER_GID = 5994 # `xctrl_fxe` (XFEL Control FXE)
            case 'XHEXP1.SPB.EH':
                CUSTOMER_GID = 6003 # `xctrl_spb` (XFEL Control SPB)
            case 'XHEXP1.HED.EH':
                CUSTOMER_GID = 5999 # `xctrl_hed` (XFEL Control HED)
            case 'XHEXP1.HED.ILH':
                CUSTOMER_GID = 5999 # `xctrl_hed` (XFEL Control HED)
            case 'XHEXP1.MID.EH':
                CUSTOMER_GID = 5998 # `xctrl_mid` (XFEL Control MID)
            case 'XHEXP1.SQS.EH':
                CUSTOMER_GID = 5996 # `xctrl_sqs` (XFEL Control SQS)
