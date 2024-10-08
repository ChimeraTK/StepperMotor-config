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

if ACCELERATOR == 'MESA':
    if STATION == 'LLRF':
        #todo clean up MOTORDRIVER_CFG_FILE variable
        MOTORDRIVER_CFG_FILE='mesamotor.xml'

        motor_cfg = MotorConfig()
        motor_cfg.add_device('MotorDriver1', 'FMC20', 3, 'controller_pzt4_md22_md22', '6s45_r2261')
        motor_cfg.add_motor('M1', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'MD22.0', 0, MOTORDRIVER_CFG_FILE)
        motor_cfg.add_motor('M2', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'MD22.0', 1, MOTORDRIVER_CFG_FILE)
        motor_cfg.add_motor('M3', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'MD22.1', 0, MOTORDRIVER_CFG_FILE)
        motor_cfg.add_motor('M4', 'LinearMotorWithReferenceSwitch', 'MotorDriver1', 'MD22.1', 1, MOTORDRIVER_CFG_FILE)
