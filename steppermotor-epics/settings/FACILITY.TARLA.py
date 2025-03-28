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
    if STATION == 'LLRF2':
        #TODO clean up MOTORDRIVER_CFG_FILE variable
        MOTORDRIVER_CFG_FILE='Limes122-MotorDriverCardConfig-Tarla.xml'
        motor_cfg = MotorConfig()
        motor_cfg.add_device('MotorDriver1', 'FMC25_70t', 3, 'llrf_resonance_ctrl', '1.1.0-9-g193bac26')
        motor_cfg.add_motor('Test1', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'FMC1', 0, MOTORDRIVER_CFG_FILE)
        motor_cfg.add_motor('Test2', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'FMC1', 1, MOTORDRIVER_CFG_FILE)
        motor_cfg.add_motor('Test3', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'FMC2', 0, MOTORDRIVER_CFG_FILE)
        motor_cfg.add_motor('Test4', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'FMC2', 1, MOTORDRIVER_CFG_FILE)
        motor_cfg.add_device('MotorDriver2', 'FMC25_70t', 4, 'llrf_resonance_ctrl', '1.1.0-9-g193bac26')
        motor_cfg.add_motor('Test5', 'LinearMotorWithReferenceSwitch', 'MotorDriver2', 'FMC1', 0, MOTORDRIVER_CFG_FILE)
        motor_cfg.add_motor('Test6', 'LinearMotorWithReferenceSwitch', 'MotorDriver2', 'FMC1', 1, MOTORDRIVER_CFG_FILE)
