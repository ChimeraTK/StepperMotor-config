# The configuration for FMC-carriers (devices) and motors is held in a container, defined in baseconfig.py
# Devices (for the dmap-file) can be added with the method:
#   MotorCfg.add_device(device_name: str,
#                       carrier_type: str,
#                       slot: int,
#                       mapp_base: str,
#                       mapp_version: str)
# And motors can be added with the method:
#  MotorCfg.add_motor(motor_type: str,
#                     device: str,
#                     fmc_slot: str,
#                     port_number: int,
#                     config_file: str,
#                     fmc_type: str = 'MD22',
#                     motor_steps_ratio: float = 1.0,
#                     encoder_steps_ratio: float = 1.0,
#                     position_unit: str = 'steps',
#                     is_dummy: bool = False)

if ACCELERATOR == 'TARLA':
    if STATION == 'MOTORDRV':
        #TODO clean up MOTORDRIVER_CFG_FILE variable
        MOTORDRIVER_CFG_FILE='Limes122-MotorDriverCardConfig-Tarla.xml'
        motor_cfg = MotorConfig()
        motor_cfg.add_device('MotorDriver1', 'FMC25_70t', 3, 'llrf_resonance_ctrl', '1.3.0-0-g154a8033')
        motor_cfg.add_device('MotorDriver2', 'FMC25_70t', 4, 'llrf_resonance_ctrl', '1.3.0-0-g154a8033')
        motor_cfg.add_motor('B1', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'FMC2', 0, MOTORDRIVER_CFG_FILE)
        motor_cfg.add_motor('B2', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'FMC2', 1, MOTORDRIVER_CFG_FILE)
        motor_cfg.add_motor('SC1_1', 'Basic', 'MotorDriver2', 'FMC2', 0, MOTORDRIVER_CFG_FILE)
        motor_cfg.add_motor('SC1_2', 'Basic', 'MotorDriver2', 'FMC2', 1, MOTORDRIVER_CFG_FILE)
        motor_cfg.add_motor('SC2_1', 'Basic', 'MotorDriver2', 'FMC1', 0, MOTORDRIVER_CFG_FILE)
        motor_cfg.add_motor('SC2_2', 'Basic', 'MotorDriver2', 'FMC1', 1, MOTORDRIVER_CFG_FILE)
