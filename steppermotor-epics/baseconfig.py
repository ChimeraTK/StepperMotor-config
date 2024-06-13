(ACCELERATOR,STATION)=INSTANCE_CONFIG

SERVERNAME=STATION
EXECUTABLE_IN_PACKAGE="/usr/bin/steppermotorserver"
WORKDIR="/var/epics-servers/"+SERVERNAME
FILES_TO_SYMLINK_BETWEEN_INSTANCES=""
MAKE_EXECUTABLE="initMotorDriverHW.py"
CYCLE_TIME_MS=1000

class FmcCarrier:
    """Container class to hold the information to compile entries for motor driver devices in the .dmap-file."""
    def __init__(self, device_name: str, carrier_type: str, slot: int, mapp_base: str, mapp_version: str):
        """Init-function of FmcCarrier class
        :param device_name: Name of the device, used to refer to device in init-script and config files
        :param carrier_type: Type of FMC-carrier card. Used to compile filename of mapp-file. I.e.: 'FMC25'
        :param slot: Slot in crate, where FMC-carrier is mounted. Used to compile device file name.
        :param mapp_base: First segment of mapp-file name, without trailing underscore. I.e.: 'llrf_resonance_control'
        :param mapp_version: Version number of the mapp-file, without leading underscore. I.e.: '1.0.0-0-g1fd3b2b2'
        """
        self.name = device_name
        self.type = carrier_type.lower()
        self.slot = slot
        # Hack to distinguish old firmware from new one
        self.board = 'BOARD.0' if mapp_base.split('_')[0] == 'controller' else 'BSP'
        self.mapp_file = f'{mapp_base}_{self.type}_{mapp_version}.mapp'

class Motor:
    """Container class to hold the information necessary to configure a single motor"""
    def __init__(self,
                 motor_name: str,
                 motor_type: str,
                 device: FmcCarrier,
                 fmc_slot: str,
                 port_number: int,
                 config_file: str,
                 fmc_type: str,
                 motor_steps_ratio: float,
                 encoder_steps_ratio: float,
                 position_unit: str,
                 is_dummy: bool):
        """Init-function of class Motor
        :param motor_name: Name to be used in PV to address the motor.
        :param motor_type: i.e.: 'LinearMotorWithReferenceSwitch'
        :param device: The FMC-carrier, the motor is connected to.
        :param fmc_slot: Name used in the firmware to address the FMCs. In newer fw 'FMC1/2' in older fw 'MD22.0/1'.
        :param port_number: Number of the port on the FMC, the motor is connected to: 0: left/bottom, 1: right/top
        :param config_file: Path to MD22-configuration file.
        :param fmc_type: Type of FMC. Usually 'MD22'
        :param motor_steps_ratio: Conversion factor from steps to unit for the motor.
        :param encoder_steps_ratio: Conversion factor from steps to unit for the encoder.
        :param position_unit: Unit to convert steps to.
        :param is_dummy: If true, a dummy instance is created in the server, instead of reading from the firmware.
        """
        self.name = motor_name
        self.type = motor_type
        self.device = device
        self.fmc_slot = fmc_slot
        self.port = port_number
        self.config_file = config_file
        self.fmc_type = fmc_type
        self.steps_ratio = [motor_steps_ratio, encoder_steps_ratio]
        self.unit = position_unit
        self.dummy = is_dummy

    def is_dummy(self) -> str:
        """Converts Bool to strings '1'/'0' for use in config-file."""
        return '1' if self.dummy else '0'

class MotorConfig:
    """Configuration database class."""
    def __init__(self):
        self._devices = {}
        self._number_devices = 0
        self._motors = {}
        self._number_motors = 0

    # The following property-functions prevent direct access to the class members, enforcing the use of
    # add_device() and add_motor() to add entries.
    @property
    def devices(self) -> dict:
        return self._devices

    @property
    def motors(self) -> dict:
        return self._motors

    @property
    def number_devices(self) -> int:
        return self._number_devices

    @property
    def number_motors(self) -> int:
        return self._number_motors

    def add_device(self, device_name: str, carrier_type: str, slot: int, mapp_base: str, mapp_version: str) -> None:
        """Add a device to the database. Is required before it can be referenced in add_motor().
        :param device_name: Name of the device, used to refer to device in init-script and config files
        :param carrier_type: Type of FMC-carrier card. Used to compile filename of mapp-file. I.e.: 'FMC25'
        :param slot: Slot in crate, where FMC-carrier is mounted. Used to compile device file name.
        :param mapp_base: First segment of mapp-file name, without trailing underscore. I.e.: 'llrf_resonance_control'
        :param mapp_version: Version number of the mapp-file, without leading underscore. I.e.: '1.0.0-0-g1fd3b2b2'
        """
        if device_name in self.devices:
            raise ValueError(f'Device "{device_name}" already exists. Device names have to be unique.')
        self._devices[device_name] = FmcCarrier(device_name, carrier_type, slot, mapp_base, mapp_version)
        self._number_devices += 1

    def add_motor(self,
                  motor_name: str,
                  motor_type: str,
                  device: str,
                  fmc_slot: str,
                  port_number: int,
                  config_file: str,
                  fmc_type: str = 'MD22',
                  motor_steps_ratio: float = 1.0,
                  encoder_steps_ratio: float = 1.0,
                  position_unit: str = 'steps',
                  is_dummy: bool = False) -> None:
        """Add motor instance to the configuration database.
        :param motor_name: Name to be used in PV to address the motor. Needs to be unique.
        :param motor_type: i.e.: 'LinearMotorWithReferenceSwitch'
        :param device: The FMC-carrier, the motor is connected to. Has to be added by add_device(), before.
        :param fmc_slot: Name used in the firmware to address the FMCs. In newer fw 'FMC1/2' in older fw 'MD22.0/1'.
        :param port_number: Number of the port on the FMC, the motor is connected to: 0: left/bottom, 1: right/top
        :param config_file: Path to MD22-configuration file.
        :param fmc_type: Type of FMC. Defaults to 'MD22'
        :param motor_steps_ratio: Conversion factor from steps to unit for the motor. Defaults to 1.0
        :param encoder_steps_ratio: Conversion factor from steps to unit for the encoder. Defaults to 1.0
        :param position_unit: Unit to convert steps to. Defaults to 'steps'
        :param is_dummy: If true, a dummy instance is created in the server, instead of reading from the firmware.
         Defaults to True
        """
        if device not in self.devices:
            raise ValueError(f'Unknown device: {device}\nKnown devices: {self.devices.keys()}')
        if port_number not in [0, 1]:
            raise ValueError(f'{port_number} is not a valid port number. Port numbers should be either 0 or 1')
        if motor_name in [x.name for x in self.motors.values()]:
            raise ValueError(f'The motor name "{motor_name}" is not unique!')
        self._motors[self.number_motors] = Motor(motor_name, 
                                                 motor_type,
                                                 self.devices[device],
                                                 fmc_slot,
                                                 port_number,
                                                 config_file,
                                                 fmc_type,
                                                 motor_steps_ratio,
                                                 encoder_steps_ratio,
                                                 position_unit,
                                                 is_dummy)
        self._number_motors += 1
