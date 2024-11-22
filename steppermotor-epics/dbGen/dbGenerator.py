#!/usr/bin/python3

"""@package docstring
Tool to map ChimeraTK variables and possible other sources to EPICS database via
a configuration xml-file.
Written and tested for Python 3.8 by Patrick Nonn for DESY/MSK
"""

import argparse  # Parse command line arguments
import os  # For file manipulation
import re
import sys  # To access stdout and stdin
import xml.etree.ElementTree as xmlEleTree  # xml parser
from typing import List, Dict, Any, Union, Optional  # Type hints
from datetime import datetime  # To access system time


VERSION = '1.2'

'''
Changelog:

1.0:
    22.Apr.2020: First release
    04.Nov.2022: Added support for boolean, void and unknown value types
1.1:
    13.Oct.2023: Added mako-hashtag to output db-files
1.2:
    14.Oct.2024: Limited aliasing for generated config files to one level
    17.Oct.2024: Added list of unused source file entries to log
    04.Nov.2024: Added ability to process <mask> and <record> entries under <ignore>
'''


# Function to abbreviate long terms
def abbreviate(in_word: str) -> str:
    """
    Function to abbreviate strings by look-up table.
    :param in_word: Word to be abbreviated.
    :return: Abbreviation, if in_word is in "abbr"-dictionary, in_word else.
    """
    if not isinstance(in_word, str):
        raise TypeError('The argument "input" of function "abbreviate" has to be of type string!')
    abbr = {
        'amplitude': 'ampl',
        'average': 'avrg',
        'calibration': 'cal',
        'configuration': 'cfg',
        'correction': 'corr',
        'deviation': 'dev',
        'filesystem': 'fs',
        'maximum': 'max',
        'minimum': 'min',
        'output': 'out',
        'processes': 'procs',
        'register': 'reg',
        'registers': 'regs',
        'request': 'req',
        'standard': 'std',
        'statistics': 'stats',
        'watchdog': 'wd',
        'adcboard0': 'adcbrd0',
        'channel0': 'ch0',
        'channel1': 'ch1',
        'channel2': 'ch2',
        'channel3': 'ch3',
        'channel4': 'ch4',
        'channel5': 'ch5',
        'channel6': 'ch6',
        'channel7': 'ch7',
        'automation': 'atmtn',
        'feedback': 'fb',
        'feedforward': 'ff',
        'setpoint': 'sp',
        'vectormodulator': 'vm',
        'amplitudephaseerror': 'aperror',
        'averagingwindow': 'avrgwin',
        'cascadeinputautomation': 'cscdinputauto',
        'cascadeinputovc': 'cscdinputovc',
        'commoncalibration': 'commoncal',
        'controller': 'ctrl',
        'devices': 'dev',
        'forwardvectorsum': 'fwdvs',
        'learningfeedforward': 'lff',
        'outputvectorcorrection': 'ovc',
        'mimocoefficients': 'mimocoeff',
        'phasemodulation': 'phasemod',
        'referencepoint': 'refpoint',
        'smithcoefficients': 'smithcoeff',
        'vectorsum': 'vs',
        'proportional': 'prop',
        'datalosscounter': 'dlcounter'
    }
    try:
        output = abbr[in_word]
    except KeyError:
        output = in_word
    return output


# Class for text formatting
class AsciiFormat:
    """Class to provide formatted strings for stdout."""
    warning = '\033[1m\033[93mWarning:\033[0m '
    error = '\033[1m\033[91mError:\033[0m '
    palette = {'RED': '\033[31m',
               'GREEN': '\033[32m',
               'YELLOW': '\033[33m',
               'BLUE': '\033[34m',
               'MAGENTA': '\033[35m',
               'CYAN': '\033[36m',
               'DGRAY': '\033[90m',
               'BOLDRED': '\033[1;31m',
               'BOLDGREEN': '\033[1;32m',
               'BOLDYELLOW': '\033[1;33m',
               'BOLDBLUE': '\033[1;34m',
               'BOLDMAGENTA': '\033[1;35m',
               'BOLDCYAN': '\033[1;36m',
               'BOLDDGRAY': '\033[1;90m'}
    reset = '\033[0m'

    @staticmethod
    def bold(text: str) -> str:
        """Makes the input be printed out as bold test in stdout
        :param text: Input text
        :return: Bold-formatted text
        """
        return f'\033[1m{text}\033[0m'

    @staticmethod
    def colored(text: str, color: str) -> str:
        """Adds ASCII-format specifiers for a range of colors to a string
        :param text: ASCII test to be colored
        :param color: Color from AsciiFormat.palette to color the text
        :return: Color-formatted text
        """
        return AsciiFormat.palette[color.upper()] + text + AsciiFormat.reset


# Define Exceptions
class XmlNodeError(Exception):
    """Exception raised, if xml-node invalid"""

    def __init__(self, xpath, message):
        self.xPath = xpath
        self.Message = message


class SkipLoop(Exception):
    """Exception raised, to skip a loop outside of the innermost one"""

    def __init__(self, message):
        self.message = message


class SourceLoadError(Exception):
    """Exception to handle unsuccessful attempts to load sourcefile"""

    def __init__(self, message):
        self.message = message


# End of Exception definitions


class Logging:
    """
    Class to provide logging to file and stdout
    """

    def __init__(self, logfile_path: str):
        """
        Constructor of class Logging.
        :param logfile_path: String holding filename of path to file to write log into.
        """
        if logfile_path is None or logfile_path == '' or os.path.isdir(logfile_path):  # Check plausability
            raise AttributeError('Class "Logging" initiated without defining path to logfile!')
        if not isinstance(logfile_path, str):  # Check Type
            raise TypeError('Class "Logging" was initiated with something different than a string!')
        if not os.path.isfile(logfile_path):  # Check, if file exists
            logfile_path_dir, logfile_path_filename = os.path.split(logfile_path)
            if logfile_path_dir == '':  # Check, if logfile_path is only filename
                self.logfile_path = os.path.abspath(logfile_path_filename)
            elif os.path.isdir(logfile_path_dir):  # Check, if directory, defined in logfile path, exists
                self.logfile_path = os.path.abspath(logfile_path)
            elif not os.path.isdir(logfile_path_dir):
                # If directory for logfile does not exist or is not accessible, use current working directory
                self.logfile_path = os.path.abspath(logfile_path_filename)
                sys.stderr.write('\033[1m\033[93mWarning:\033[0m: Directory defined for logfile is not accessible! '
                                 'Logfile will be generated in the current working directory.\n')
            else:
                raise AttributeError('Unrecognized Error, while processing Argument "logfile_path", '
                                     'passed to class "Logging"')
        else:  # logfile_path points to existing file
            self.logfile_path = os.path.abspath(logfile_path)
        with open(self.logfile_path, 'a') as f:
            f.write(f'{"-" * 80}\n{datetime.now()}: Beginning run of dbGenerator\n')

    def _markdown(self, in_str: str) -> str:
        """
        Recursive method to change strings containing ascii formatting for stdout to plain ascii.
        :param in_str: String to be changed
        :return: String with changed formatting
        """
        if not isinstance(in_str, str):
            raise TypeError('_markdown takes only string type attributes')
        mark_left = '\033[1m'
        mark_left_len = len(mark_left)
        mark_right = '\033[0m'
        pos_open = in_str.find(mark_left)
        if pos_open != -1:
            if in_str.find('\33[9', pos_open + mark_left_len, pos_open + mark_left_len + 3) != -1:
                mark_left_len += len('\33[93m')
            pos_close = in_str.find(mark_right, pos_open + mark_left_len)
            if pos_close != -1:
                return self._markdown(in_str[:pos_open]
                                      + in_str[pos_open + mark_left_len:pos_close].upper()
                                      + in_str[pos_close + len(mark_right):])
            else:
                return in_str
        else:
            return in_str

    def write(self, log_message: str):
        """
        Writes to log file and stderr.
        :param log_message: Message to be written, formatted for stderr/stdout
        """
        if not isinstance(log_message, str):
            raise TypeError('Log takes only string type attributes')
        if log_message.find(AsciiFormat.warning) != -1:  # Check, if string contains warning tag
            sys.stderr.write(f'{log_message}\n')
            with open(self.logfile_path, 'a') as f:
                f.write(f'{datetime.now()}: {self._markdown(log_message)}\n')
        elif log_message.find(AsciiFormat.error) != -1:  # Check, if string contains error tag
            sys.stderr.write(f'{log_message}\n')
            with open(self.logfile_path, 'a') as f:
                f.write(f'{datetime.now()}: {self._markdown(log_message)}\n')
        else:  # When no tag is found
            sys.stdout.write(f'{log_message}\n')
            with open(self.logfile_path, 'a') as f:
                f.write(f'{datetime.now()}: {self._markdown(log_message)}\n')


class Table:
    """Container class for structured data in table format. Data added in rows, but can be accessed by column name."""

    def __init__(self,
                 column_names: Union[str, List[str]],
                 content_list: Union[List[List[str]], List[Dict[str, Any]], None] = None):
        """Constructor of Table object
        :param column_names: Headline, naming the columns of the table.
        :param content_list: Table content.
        """
        if not isinstance(column_names, (list, str)):  # Check type
            raise TypeError('The first attribute of table() has to be of type list or string!')
        if isinstance(column_names, str):  # Conversion to list type if it is string
            column_names = [column_names]
        elif not all(map(lambda x: isinstance(x, str), column_names)):  # Check for list content being string
            raise TypeError('The first attribute of table object has to be a list containing strings!')
        elif len(column_names) != len(set(column_names)):  # Check for duplicates
            raise AttributeError('The first attribute of table object can\'t contain duplicates!')
        else:
            self._head = column_names  # type: List[str]
        if content_list is not None:  # Process content given at initialization
            if not all(map(lambda x: isinstance(x, (list, dict)), content_list)):  # Check types
                raise TypeError('The second attribute of table() has to be None or a list of lists or dictionaries!')
            if any(map(lambda x: len(x) < len(column_names), content_list)):  # Check lengths of items
                raise AttributeError('The second attribute of table() has to be a list of lists or dictionaries, '
                                     'which are of the same length, as the first attribute!')
            if all(map(lambda x: isinstance(x, list), content_list)):  # Process list of lists
                for row in content_list:
                    # Check, if row has the required length
                    if len(row) != len(self._head):
                        raise AttributeError('At least one element of "content_list" has the wrong length!')
                    else:
                        # Convert list of uniform lists to list of uniform dictionaries
                        self.add(dict(zip(self._head, row)))
            elif all(map(lambda x: isinstance(x, dict), content_list)):  # Process list of dictionaries
                self._table = []
                for row_dict in content_list:  # type: Dict[str, Any]
                    self.add(row_dict)
            else:  # Something is very wrong, if we get here
                raise AttributeError('The attribute "content_list", if not None, has to be '
                                     'a list of ONLY lists or '
                                     'a list of ONLY dictionaries!')
        else:
            self._table = []

    def __repr__(self) -> str:
        """Magic method, called when Table object is printed
        :return: Object description
        """
        return f'Table object with {len(self._table)} entries.'

    def __str__(self) -> str:
        """Magic method, called by str()
        :return: Content of Table object in table-like format
        """
        output = [f'\033[1m{self._head}\033[0m']
        for table_row in self._table:
            row_list = []
            for col_name in self._head:
                row_list.append(table_row[col_name])
            output.append(str(row_list))
        return '\n'.join(output)

    def __getitem__(self, col: str) -> List[Any]:
        """Magic method, called by []-accessor
        :param col: Column name, has to be in "_head".
        :return: Content of column, which name is matching "col".
        """
        if col in self._head:
            output = []  # type: List[Any]
            for table_row in self._table:
                output.append(table_row[col])
            return output
        else:
            raise AttributeError(f'Table has no column named "{col}"')

    def __len__(self) -> int:
        """Magic method, called by len()
        :return: Number of rows (entries) in table
        """
        return len(self._table)

    def __iter__(self):
        """Iterator initialization"""
        self._index = 0
        self._row = None
        return self

    def __next__(self):
        """Iterator incrementation"""
        if self._index > len(self._table) - 1:
            del self._index
            del self._row
            raise StopIteration
        else:
            self._row = self._table[self._index]
            output = self._row
            self._index += 1
            return output

    @property
    def head(self):
        """Provides iterable over columns."""
        out = []
        for col_name in self._head:
            out.append(col_name)
        return out

    def add(self, row: Dict[str, Any]):
        """Method to add row to Table object.
        :param row: Row to be added to table. May have content beyond the needed keys.
        """
        if not isinstance(row, dict):  # Check Type
            raise TypeError('table.add() expects a dictionary as argument')
        if len(row) < len(self._head):  # Check length
            raise ValueError(f'The argument of add_row has to be a dictionary with the length of at least '
                             f'{len(self._head)}')
        new_row = {}
        for col in self._head:  # Add only keys defined in head to the table
            try:
                new_row[col] = row[col]
            except KeyError:  # If row misses a key
                raise AttributeError('The dictionary given to table.add() misses at least one key, '
                                     'defined in the first attribute of table()!')
        self._table.append(new_row)

    def remove_column(self, col_name: str):
        """Method to remove column by column name
        :param col_name: Name of the column to be removed.
        """
        if not isinstance(col_name, str):
            raise TypeError('Attribute "col_name" of method "remove_column" has to be of type string.')
        if col_name not in self._head:
            raise AttributeError('Attribute "col_name" of method "remove_column" is not a column in Table object.')
        self._head.remove(col_name)
        for entry in self._table:
            entry.pop(col_name, None)

    def query(self, pattern: Union[Dict[str, Any], str]) -> Union[List[Dict[str, Any]], None]:
        """Method to search the table for either all rows with a field matching pattern string or all rows where the
        content of column, defined in pattern dictionary, matches the value, associated in dictionary.
        :param pattern: Search pattern, either as string, searched in all columns,
        or dictionaries, defining column and object to be searched as key/value pairs.
        :return: List of dictionaries, holding the result of the query, or None, if nothing was found
        """
        result = []
        if not isinstance(pattern, (dict, str)):
            raise TypeError('table.query() takes a dict or a string as argument!')
        elif isinstance(pattern, dict):
            result += self._table
            for pattern_key in pattern:
                if pattern_key in self._head:
                    result = list(filter(lambda x: x[pattern_key] == pattern[pattern_key], result))
                else:
                    raise ValueError(f'{pattern_key} is not a column in table!')
        elif isinstance(pattern, str):
            for head_key in self._head:
                result += list(filter(lambda x: x[head_key] == pattern, self._table))
        if not result:
            return None
        else:
            return result


class DbFile(Table):
    """Container class for EPICS data. Includes db-file generation."""

    def __init__(self, dbfile_path: str, macro_reserve: int = 0, logging: Any = sys.stderr):
        """
        :param dbfile_path: Path to write db-file to.
        :param macro_reserve: Number of characters, reserved in PV name to be filled by macro-expansion
        :param logging: Object with 'write()' method, i.e. Logger or sys.stderr
        """
        super().__init__(['devicePath', 'pvName', 'recordType', 'fields'], None)
        if not callable(getattr(logging, 'write')):
            raise AttributeError('Attribute "logging" of PVDb object has to be an object with a "write" method!')
        else:
            self.log = logging
        if not isinstance(dbfile_path, str):
            raise TypeError('Argument "dbfile_path" of class DbFile has to be of type string')
        if not os.path.exists(os.path.dirname(os.path.abspath(dbfile_path))):
            raise AttributeError('Argument "dbfile_path" refers to a non-existing directory!')
        self.file_path = os.path.abspath(dbfile_path)
        if os.path.isfile(self.file_path):
            self.log.write(f'{AsciiFormat.warning}File "{self.file_path}" will be overwritten!')
        if not isinstance(macro_reserve, int):
            raise TypeError('Attribute "macro_reserve" has to be of type int!')
        self.macro_reserve = macro_reserve

    def __getitem__(self, pv_id: str) -> dict:
        """Magic method, accesses dataset (row) with the field 'devicePath' matching pv_id
        :param pv_id: Term to match in field 'devicePath'
        :return: Dataset with matching devicePath
        """
        if not isinstance(pv_id, str):  # Check Type
            raise TypeError('Attribute of PVDb[] has to be string.')
        query_result = super().query({'devicePath': pv_id})  # Find Entry
        if not query_result:  # Check existence
            self.log.write(f'{AsciiFormat.error}PV with device path {pv_id} does not exist in PVDb!')
        elif len(query_result) == 1:  # Usual case
            index = self._table.index(query_result[0])
            return self._table[index]
        elif len(query_result) > 1:  # Check Multiple Entries
            self.log.write(f'{AsciiFormat.error}Multiple PVs with device path {pv_id} found in PVDb!'
                           f' PVDb might be corrupted!')
            index = self._table.index(query_result[0])
            return self._table[index]
        else:  # For unforeseen cases
            raise RuntimeError('Something has gone wrong!')

    def _remove_macros(self, in_str: str) -> str:
        """Recursively remove Macros from input
        :param in_str: String to remove macros from.
        :return: String with macro found first, removed.
        """
        if not isinstance(in_str, str):
            raise TypeError('Attribute of method "_remove_macros" has to be of type string!')
        open_pos = in_str.find('$(')
        if open_pos == -1:  # End recursion
            return in_str
        else:
            close_pos = in_str.find(')', open_pos) + 1
            output = in_str[:open_pos] + in_str[close_pos:]
            return self._remove_macros(output)

    def add(self, record: Dict[str, Any]):
        """Adds EPICS record to database, including some checking for compliance with EPICS.
        :param record: EPICS record to be added to database
        """
        # Type check
        record_elements = {'devicePath': str, 'pvName': str, 'recordType': str, 'fields': dict}
        for entry in record_elements:
            try:  # pycharm mistakes dict-[] accessor for type hint -> using __getitem__ instead
                if not isinstance(record[entry], record_elements.__getitem__(entry)):
                    raise TypeError(f'{AsciiFormat.error}Type mismatch in "record"!')
            except KeyError:
                raise AttributeError(f'{AsciiFormat.error}Attribute "record" is missing at least one key!')
        # Check length of PV name
        pv_name_max = 39
        length_pv_name = len(self._remove_macros(record['pvName'])) + self.macro_reserve
        if length_pv_name > pv_name_max:
            self.log.write(f'{AsciiFormat.warning}PV name "{record["pvName"]}" is '
                           f'{length_pv_name - pv_name_max} characters too long!')
        # Check record type
        known_record_types = ['int64out',
                              'int64in',
                              'ao',
                              'ai',
                              'longout',
                              'longin',
                              'aao',
                              'aai',
                              'lso',
                              'lsi',
                              'stringin',
                              'stringout',
                              'bi',
                              'bo',
                              'mbbi',
                              'mbbo',
                              'mbbiDirect',
                              'mbboDirect',
                              'dfanout',
                              'fanout',
                              'calc',
                              'calcout',
                              'histogram',
                              'seq',
                              'sub',
                              'subArray',
                              'waveform',
                              'state',
                              'event',
                              'sel',
                              'compress',
                              'printf',
                              'aSub',
                              'permissive']
        if not record['recordType'] in known_record_types:
            self.log.write(f'{AsciiFormat.error}PV "{record["pvName"]}" '
                           f'has unknown record type: {record["recordType"]}')
            raise SkipLoop
        # Convert c-style variable types in EPICS counterparts
        type_conversion = {'int64': 'INT64',
                           'uint64': 'UINT64',
                           'int32': 'LONG',
                           'uint32': 'ULONG',
                           'int16': 'SHORT',
                           'uint16': 'USHORT',
                           'int8': 'CHAR',
                           'uint8': 'UCHAR',
                           'double': 'DOUBLE',
                           'float': 'FLOAT',
                           'string': 'STRING'}
        try:
            record_ftvl_field = record['fields']['FTVL']
        except KeyError:
            record_ftvl_field = None
            pass
        if record_ftvl_field in type_conversion:
            record['fields']['FTVL'] = type_conversion[record_ftvl_field]
        # Call add of class Table, to add
        super().add(record)

    def write_db_file(self, source: Optional[str] = None):
        """Generate EPICS db file from database
        :param source: Config file used for generation, for comment at head of file.
        """
        # Assemble file content as one string
        out_str = f'##mako -*- coding: utf-8 -*-\n# File generated by dbGenerator version {str(VERSION)}'
        if source is not None:
            out_str += f' from configuration file:\n# "{source}"\n'
        else:
            out_str += '.\n'
        out_str += '# Do not change the content of this file!\n\n'
        for pv in self._table:
            record_fields = '    field(' + '")\n    field('.join(list(map(', "'.join, pv['fields'].items()))) + '")'
            record_str = f'record({pv["recordType"]}, "{pv["pvName"]}"){{\n' \
                         f'{record_fields}\n' \
                         f'}}\n'
            out_str += record_str + '\n'
        # Write string to file
        with open(self.file_path, 'w') as db_file:
            db_file.write(out_str)


class XmlSource(Table):
    """Class to handle data from xml files, generated with <ChimeraTK-server>-xmlGenerator."""

    def __init__(self,
                 xml_filepath: str,
                 logger: Any = sys.stderr,
                 aliases: Optional[Dict[str, List[str]]] = None):
        """
        :param xml_filepath: Filename or path to xml file to be parsed
        :param logger: Object with "write" method, i.e. sys.stderr or Logging-class object
        :param aliases: Aliases for expansion
        """
        if not os.path.isfile(xml_filepath):
            raise AttributeError(str(xml_filepath) + ' is not an existing file!')
        if not callable(getattr(logger, 'write')):
            raise AttributeError('Attribute "logger" of class XmlSource has to have a callable method "write(str)"')
        self.logger = logger
        super().__init__(['address',  # Full XML path, basically VariablePath + VariableName, has to be unique
                          'variablePath',  # XML path to variable as "/"-separated string
                          'variableName',  # Variable name
                          'value_type',
                          'numberOfElements',
                          'direction',
                          'unit',
                          'description'])
        self.namespace = '{https://github.com/ChimeraTK/ApplicationCore}'
        self._index = []
        if aliases is None:
            self.aliases = {}
        else:
            self.aliases = aliases
        self.file = os.path.abspath(xml_filepath)
        try:
            self._tree = xmlEleTree.parse(self.file)
        except FileNotFoundError:
            raise SourceLoadError(f'{AsciiFormat.error}File "{self.file}" not found!')
        except xmlEleTree.ParseError:
            raise SourceLoadError(f'{AsciiFormat.error}File "{self.file}" can not be parsed! Corrupt/not xml file?')
        self._root = self._tree.getroot()
        if self._root.tag != f'{self.namespace}application':
            raise SourceLoadError(f'{AsciiFormat.error}File "{self.file}" seems not to be a ChimeraTK variable file!')
        self.application = self._root.get('name')
        self._make_index(self._root)
        # Extract Information from source xml
        for variable in self._index:
            var_path = variable['var_path']
            var_name = variable['var_name']
            var_data = {'value_type': None,
                        'unit': '',
                        'description': '',
                        'direction': None,
                        'numberOfElements': None}
            try:  # To catch SkipLoop
                for val_key in var_data:
                    try:
                        var_data[val_key] = variable['xml_address'].find(self.namespace + val_key).text
                    except AttributeError:
                        self.logger.write(f'{AsciiFormat.error}Attribute "{val_key}" not found in '
                                          f'{AsciiFormat.bold(var_path + var_name)}!')
                        if val_key in ['direction', 'numberOfElements']:
                            raise SkipLoop
            except SkipLoop:
                self.logger.write('Variable will be ignored')
                continue
            # Assembling content
            self.__add({
                'address': var_path + var_name,
                'variablePath': var_path,
                'variableName': var_name,
                'value_type': var_data['value_type'],
                'direction': var_data['direction'],
                'unit': var_data['unit'],
                'description': var_data['description'],
                'numberOfElements': int(var_data['numberOfElements'])
            })

    def __getitem__(self, search_str: str) -> Dict[str, Any]:
        """Magic method, provides []-accessor.
        :param search_str: String to be found in 'Alias'-column
        :return: Entry, whose 'Alias' column in matching 'search_str'
        """
        if not isinstance(search_str, str):  # Check Type
            raise TypeError('Attribute of XmlSource[] has to be string.')
        query_result = self.query({'address': search_str})  # Find Entry
        if query_result is None:  # Check existence
            self.logger.write(f'{AsciiFormat.error}Entry with Address {search_str} does not exist in XmlSource')
        elif len(query_result) == 1:  # Usual case
            index = self._table.index(query_result[0])
            return self._table[index]
        elif len(query_result) > 1:  # Check Multiple Entries
            self.logger.write(f'{AsciiFormat.error}Multiple entries with ID {search_str} found in XmlSource!'
                              f' Database is corrupted!')
            index = self._table.index(query_result[0])
            return self._table[index]
        else:  # For unforeseen cases
            raise RuntimeError('Something has gone wrong!')

    def _make_index(self, xml_node: Any, pv_path: str = ''):
        """Recursive method to iterate through the xml tree and isolate the 'variables'
        while maintaining the path in order to generate an index.
        :param xml_node: xml node to recurse over
        :param pv_path: Path to the node, from which the function is called.
        """
        for v in xml_node.findall(self.namespace + 'variable'):
            self._index.append({'xml_address': v, 'var_path': pv_path, 'var_name': v.get('name')})
        for d in xml_node.findall(self.namespace + 'directory'):
            self._make_index(d, pv_path=pv_path + d.get('name') + '/')
        return  # Break recursion, if no more directories found

    def __add(self, row: Dict[str, Any]):
        """To bend add method of parent class to hidden method"""
        super().add(row)

    def add(self, row):
        """To hide add method of parent class"""
        raise AttributeError("'XmlSource' object has no attribute 'add'")

    def column(self, column_head: str) -> List[Any]:
        """Replaces overridden []-accessor function from parent class.
        Returns content of column named "column_head".
        :param column_head: Name of column to be extracted
        :return: Content of column "column_head"
        """
        return super().__getitem__(column_head)


class EpicsCfg:
    """Class to read, process and generate EPICS config files"""

    def __init__(self, cfg_file_path: str, logger: Any = sys.stderr):
        """
        :param cfg_file_path: Valid path to file or directory
        :param logger: Where messages are written to
        """
        if not callable(getattr(logger, 'write')):
            raise AttributeError('Attribute "logger" of class XmlSource has to have a callable method "write(str)"')
        self.logger = logger
        if not isinstance(cfg_file_path, str):
            raise TypeError('Argument "cfg_path" has to be a string, preferably holding the path to a file!')
        self._cfg_abspath = os.path.abspath(cfg_file_path)
        self._cfg_dir, self._cfg_file = os.path.split(self._cfg_abspath)
        if not os.path.isdir(self._cfg_dir):
            raise AttributeError(f'{self._cfg_dir} is not a valid path to an existing directory!')
        self.file_path = cfg_file_path
        self._sources = {}
        self._remaining_source_entries = {}

    def load_source(self, source_path: str, source_label: str, source_type: str = 'xml-variables', **kwargs):
        """Adds content of source file to source-database
        :param source_path: Path to source file
        :param source_label: Label to access data in the source-database
        :param source_type: Type of source file
        :param kwargs: Various keyword arguments, depending on source file type
        """
        if not isinstance(source_path, str):
            raise TypeError('Argument "source_path" of function "load_source" has to be of type string')
        if not isinstance(source_type, str):
            raise TypeError('Argument "source_type" of function "load_source" has to be of type string')
        source_types = ['xml-variables']
        if source_type not in source_types:
            raise AttributeError(f'Argument "source_type" of function "load_source" has to be one of the following: '
                                 f'{", ".join(source_types)}')
        if source_type == 'xml-variables':
            try:
                source_aliases = kwargs['aliases']
            except KeyError:
                source_aliases = None
            try:
                # Generate source database
                self._sources[source_label] = XmlSource(source_path, logger=self.logger, aliases=source_aliases)
                # Populate _remaining_source_entries
                self._remaining_source_entries[source_label] = self._sources[source_label].column('address')
            except SourceLoadError as error:
                self.logger.write(error.message)
        else:
            raise AttributeError('Source type "' + str(source_type) + '" is unknown!')

    def generate_config_file(self, source_label: str, macro: Optional[str] = None, macro_length: Optional[int] = 0):
        """Method to generate simple config xml file as a blank.
        :param source_label: Label of the xml-source, to access it in self.sources-dictionary
        :param macro: Macro to be added to all PVs
        :param macro_length: Length to be reserved in pv name for macro
        """
        gen_log = Logging(source_label + 'CfgGen.log')  # Generate separate log file
        gen_log.write('Start of config file generation.')
        try:
            xml_source = self._sources[source_label]  # type: XmlSource
        except KeyError:
            gen_log.write(f'{AsciiFormat.error}Source label "{source_label}" does not refer to a loaded source!')
            return
        if not xml_source:
            self.logger.write(f'{AsciiFormat.error}Empty source! Config file not generated!')
            return
        if not isinstance(self._sources[source_label], XmlSource):
            raise TypeError('source_label has to refer to XmlSource object in self._sources member of class EpicsCfg!')
        if macro is not None:
            if not isinstance(macro, str):
                raise TypeError('Argument "macro" has to be a string!')
            if not isinstance(macro_length, int):
                raise TypeError('Argument "macro_length" has to be an integer!')
        # Prompt if existing file should be overwritten, and end function, if not
        if os.path.isfile(self._cfg_abspath) and not \
                input(f'File {self._cfg_abspath} exists! Overwrite? (y/n):').lower() in ['y', 'yes']:
            gen_log.write('Ending config file generation to not overwrite existing file!')
            return
        # Dictionary to convert c types into EPICS counterparts
        pv_type_conversion = {'int64': 'INT64',
                              'uint64': 'UINT64',
                              'int32': 'LONG',
                              'uint32': 'ULONG',
                              'int16': 'SHORT',
                              'uint16': 'USHORT',
                              'int8': 'CHAR',
                              'uint8': 'UCHAR',
                              'double': 'DOUBLE',
                              'float': 'FLOAT',
                              'string': 'STRING',
                              'Boolean': 'BOOL'}
        # Dictionary to convert "direction" to EPICS IN/OUT
        pv_direction_determination = {'control_system_to_application': 'OUT',
                                      'control_system_to_application_with_return': 'OUT',
                                      'application_to_control_system': 'INP',
                                      'application_to_control_system_with_return': 'INP'}
        # Dictionary to determine record type
        pv_type_determination = {'INPFalseINT64': 'int64in',
                                 'INPFalseUINT64': 'int64in',
                                 'INPFalseFLOAT': 'ai',
                                 'INPFalseDOUBLE': 'ai',
                                 'INPFalseSHORT': 'longin',
                                 'INPFalseUSHORT': 'longin',
                                 'INPFalseLONG': 'longin',
                                 'INPFalseULONG': 'longin',
                                 'INPFalseCHAR': 'longin',
                                 'INPFalseUCHAR': 'longin',
                                 'INPFalseSTRING': 'lsi',
                                 'INPFalseBOOL': 'bi',
                                 'INPTrueINT64': 'aai',
                                 'INPTrueUINT64': 'aai',
                                 'INPTrueFLOAT': 'aai',
                                 'INPTrueDOUBLE': 'aai',
                                 'INPTrueSHORT': 'aai',
                                 'INPTrueUSHORT': 'aai',
                                 'INPTrueLONG': 'aai',
                                 'INPTrueULONG': 'aai',
                                 'INPTrueCHAR': 'aai',
                                 'INPTrueUCHAR': 'aai',
                                 'INPTrueSTRING': 'aai',
                                 'INPTrueBOOL': 'mbbiDirect',
                                 'OUTFalseINT64': 'int64out',
                                 'OUTFalseUINT64': 'int64out',
                                 'OUTFalseFLOAT': 'ao',
                                 'OUTFalseDOUBLE': 'ao',
                                 'OUTFalseSHORT': 'longout',
                                 'OUTFalseUSHORT': 'longout',
                                 'OUTFalseLONG': 'longout',
                                 'OUTFalseULONG': 'longout',
                                 'OUTFalseCHAR': 'longout',
                                 'OUTFalseUCHAR': 'longout',
                                 'OUTFalseSTRING': 'lso',
                                 'OUTFalseBOOL': 'bo',
                                 'OUTTrueINT64': 'aao',
                                 'OUTTrueUINT64': 'aao',
                                 'OUTTrueFLOAT': 'aao',
                                 'OUTTrueDOUBLE': 'aao',
                                 'OUTTrueSHORT': 'aao',
                                 'OUTTrueUSHORT': 'aao',
                                 'OUTTrueLONG': 'aao',
                                 'OUTTrueULONG': 'aao',
                                 'OUTTrueCHAR': 'aao',
                                 'OUTTrueUCHAR': 'aao',
                                 'OUTTrueSTRING': 'aao',
                                 'OUTTrueBOOL': 'mbboDirect'}
        # Dictionary to determine autosave based on record type
        pv_autosave_determination = {'int64out': 'true',
                                     'int64in': 'false',
                                     'ao': 'true',
                                     'ai': 'false',
                                     'longout': 'true',
                                     'longin': 'false',
                                     'aao': 'false',
                                     'aai': 'false',
                                     'lso': 'true',
                                     'lsi': 'false',
                                     'bo': 'true',
                                     'bi': 'false',
                                     'mbboDirect': 'true',
                                     'mbbiDirect': 'false'}
        # Determine value of SCAN field, depending on record type
        pv_scan_determination = {'int64out': 'Passive',
                                 'int64in': '1 second',
                                 'ao': 'Passive',
                                 'ai': '1 second',
                                 'longout': 'Passive',
                                 'longin': '1 second',
                                 'aao': 'Passive',
                                 'aai': '1 second',
                                 'lso': 'Passive',
                                 'lsi': '1 second',
                                 'bo': 'Passive',
                                 'bi': '1 second',
                                 'mbboDirect': 'Passive',
                                 'mbbiDirect': '1 second'}
        pvs = Table(['pvName', 'devicePath', 'recordType', 'autosave', 'fields'])
        # Generate aliases from xml path
        gen_log.write('Generate aliases')

        # Prune all branches in the variable tree, which have less than 5 leafs.
        paths = []
        branches = xml_source.column('variablePath')
        for branch in list(set(branches)):  # list(set(list)) to remove duplicates
            number_of_branches = branches.count(branch)
            if number_of_branches > 4:
                paths.append(branch)

        aliases = {}
        for path in paths:
            words = path.strip('/').split('/')
            surrogate_parts = []
            for word in words:
                short_word = abbreviate(word.casefold())
                surrogate_parts.append(short_word.capitalize())
            gen_log.write(f'Alias for node {"/".join(words)}/: {"".join(surrogate_parts)}')
            # Make sure, the "path" conforms to: node1/node2/
            aliases[f'{"/".join(words)}/'] = ''.join(surrogate_parts)

        gen_log.write('Compile data from xml.')
        for entry in xml_source:  # Build database
            if entry['value_type'] in ['Void', 'unknown']:  # Skip Void-Type/Unknown Variables/Registers
                gen_log.write(f'{entry["variablePath"]}{entry["variableName"]} is of type {entry["value_type"]}: '
                              f'No record was created!')
                continue
            try:  # Try to resolve aliases
                pv_device_address = f'+\u007b{aliases[entry["variablePath"]]}\u007d{entry["variableName"]}'
            except KeyError:
                pv_device_address = entry['address']
            pv_recordtype = pv_type_determination[pv_direction_determination[entry['direction']]
                                                  + str(entry['numberOfElements'] > 1)
                                                  + pv_type_conversion[entry['value_type']]]
            pv_fields_determination = {
                'int64out': {'SCAN': pv_scan_determination[pv_recordtype],
                             'OUT': '@$(APP) +{:address}',
                             'EGU': '+{:unit}',
                             'PINI': '1'},
                'int64in': {'SCAN': pv_scan_determination[pv_recordtype],
                            'INP': '@$(APP) +{:address}',
                            'EGU': '+{:unit}'},
                'ao': {'SCAN': pv_scan_determination[pv_recordtype],
                       'OUT': '@$(APP) +{:address}',
                       'EGU': '+{:unit}',
                       'PINI': '1'},
                'ai': {'SCAN': pv_scan_determination[pv_recordtype],
                       'INP': '@$(APP) +{:address}',
                       'EGU': '+{:unit}'},
                'longout': {'SCAN': pv_scan_determination[pv_recordtype],
                            'OUT': '@$(APP) +{:address}',
                            'EGU': '+{:unit}',
                            'PINI': '1'},
                'longin': {'SCAN': pv_scan_determination[pv_recordtype],
                           'INP': '@$(APP) +{:address}',
                           'EGU': '+{:unit}'},
                'lso': {'SCAN': pv_scan_determination[pv_recordtype],
                        'OUT': '@$(APP) +{:address}',
                        'PINI': '1'},
                'lsi': {'SCAN': pv_scan_determination[pv_recordtype],
                        'INP': '@$(APP) +{:address}'},
                'aao': {'SCAN': pv_scan_determination[pv_recordtype],
                        'OUT': '@$(APP) +{:address}',
                        'EGU': '+{:unit}',
                        'FTVL': '+{:value_type}',
                        'NELM': '+{:numberOfElements}',
                        'PINI': '1'},
                'aai': {'SCAN': pv_scan_determination[pv_recordtype],
                        'INP': '@$(APP) ' + '+{:address}',
                        'EGU': '+{:unit}',
                        'FTVL': '+{:value_type}',
                        'NELM': '+{:numberOfElements}'},
                'bo': {'SCAN': pv_scan_determination[pv_recordtype],
                       'OUT': '@$(APP) +{:address}',
                       'ZNAM': 'False',
                       'ONAM': 'True',
                       'PINI': '1'},
                'bi': {'SCAN': pv_scan_determination[pv_recordtype],
                       'INP': '@$(APP) +{:address}',
                       'ZNAM': 'False',
                       'ONAM': 'True'},
                'mbboDirect': {'SCAN': pv_scan_determination[pv_recordtype],
                               'OUT': '@$(APP) +{:address}',
                               'NOBT': '+{:numberOfElements}'},
                'mbbiDirect': {'SCAN': pv_scan_determination[pv_recordtype],
                               'INP': '@$(APP) +{:address}',
                               'NOBT': '+{:numberOfElements}'}
            }
            # Construct macro
            pv_macro = f'$({macro})' if macro is not None else ''
            if entry['variablePath'] in aliases:
                pv_name_path = f'{aliases[entry["variablePath"]]}/'
            else:
                pv_name_path = entry['variablePath']
            pv_name = pv_name_path + entry['variableName']
            if len(pv_name) > 39 - macro_length:
                gen_log.write(f'PV name "{pv_macro}{pv_name}" is too long.')
            pvs.add({'devicePath': f'{xml_source.application}.{pv_device_address}',
                     'pvName': pv_macro + pv_name,
                     'recordType': pv_recordtype,
                     'autosave': pv_autosave_determination[pv_recordtype],
                     'fields': pv_fields_determination[pv_recordtype]})
        gen_log.write('Compile config file.')
        cfg_xmlns = 'https://github.com/ChimeraTK/ControlSystemAdapter-EPICS-IOC-Adapter'
        cfg_xml_root = xmlEleTree.Element('EPICSdb', xmlns=cfg_xmlns, application=xml_source.application)
        cfg_xml_source = xmlEleTree.SubElement(cfg_xml_root, 'sourcefile',
                                               type='xml-variables',
                                               path=xml_source.file,
                                               label=xml_source.application)
        # generate alias-entries
        for alias_path, alias_handle in aliases.items():
            xmlEleTree.SubElement(cfg_xml_source, 'alias', handle=alias_handle, surrogate=alias_path)
        if xml_source.file[-4:] == '.xml':
            db_path = xml_source.file[:-4] + '.db'
        else:
            db_path = xml_source.application + '.db'
        # Generate db file definition
        cfg_xml_output_db = xmlEleTree.SubElement(cfg_xml_root, 'outputfile',
                                                  path=db_path,
                                                  macroReserve=str(macro_length))
        # Set file generic 'fields'
        xmlEleTree.SubElement(cfg_xml_output_db, 'field', type='DTYP', value='ChimeraTK')
        for rec_type in list(set(pvs['recordType'])):
            cfg_xml_recordtype = xmlEleTree.SubElement(cfg_xml_output_db, 'recordgroup',
                                                       type=rec_type,
                                                       autosave=pv_autosave_determination[rec_type])
            # Extract records of same type
            records = Table(['devicePath', 'pvName', 'autosave', 'fields'],
                            content_list=pvs.query({'recordType': rec_type}))
            # Find default fields
            record_fields = Table(list(records['fields'][0].keys()), records['fields'])  # type: Table
            for field_name in record_fields.head:
                field_val = record_fields[field_name]  # type: List[Any]
                field_val_elements = list(set(field_val))
                if len(field_val_elements) == 1:
                    xmlEleTree.SubElement(cfg_xml_recordtype, 'field', type=field_name, value=field_val_elements[0])
                    for record in records:
                        record['fields'].pop(field_name, None)
            for record in records:
                cfg_xml_record = xmlEleTree.SubElement(cfg_xml_recordtype, 'record',
                                                       pvName=record['pvName'],
                                                       source=record['devicePath'])
                fields = record['fields']
                for field in fields:
                    xmlEleTree.SubElement(cfg_xml_record, 'field', type=field, value=fields[field])
        xml_list = []
        xml_list_item = ''
        for element in xmlEleTree.tostringlist(cfg_xml_root, encoding='unicode', method='xml'):
            xml_list_item += element
            if xml_list_item[-1] == '>':
                xml_list.append(xml_list_item)
                xml_list_item = ''
        indent_level = 0
        xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n'
        indent = '    '
        for tag in xml_list:
            if tag[:2] == '</':
                indent_level -= 1
            if indent_level < 0:
                indent_level = 0
            xml_str += indent_level * indent + tag + '\n'
            if tag[-2:] != '/>' and tag[:2] != '</':
                indent_level += 1
        gen_log.write('Writing file: ' + self.file_path)
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(xml_str)
        gen_log.write('Config file generation complete!')

    def _expand(self, in_str: str, aliases: Dict[str, str], source_link: Optional[Dict[str, Any]] = None) -> str:
        """Recursive method to replace strings, placed between "+{" and "}"
        :param in_str: String to be expanded
        :param aliases: Alias-dictionary
        :param source_link: Reference for :links
        :return: Expanded string
        """
        if not isinstance(in_str, str):
            raise TypeError('Attribute "in_str" of "_expand"-method has to be of type string')
        pos_open = in_str.find("+{")
        if pos_open != -1:
            pos_close = in_str.find("}", pos_open + 1)
            if pos_close == -1:
                return in_str
        else:
            return in_str
        try:
            if pos_close - pos_open == 0:  # Check for empty curly brackets
                self.logger.write(f'{AsciiFormat.warning}Empty Macro in string "{in_str}" will be ignored!')
                macro = ''
            elif in_str[pos_open + 2] == ':':  # Access source data
                if source_link is None:
                    raise AttributeError('Tried to expand source-link (+{:link}) without providing source!')
                macro = str(source_link[in_str[pos_open + 3:pos_close]])
            else:
                macro = aliases[in_str[pos_open + 2:pos_close]]
        except KeyError:
            self.logger.write(f'{AsciiFormat.warning}Macro {in_str[pos_open:pos_close + 1]} not defined, and will be ignored!')
            macro = ''
        out = self._expand(in_str[:pos_open] + macro + in_str[pos_close + 1:], aliases, source_link)
        return out

    @staticmethod
    def _process_field_element(xml_address: xmlEleTree.Element) -> Dict[str, str]:
        """Extracting type and value from field element, while checking their existence.
        :param xml_address: xml address of field element
        :return: Field type and value
        """
        if xml_address.tag.split('}')[-1] != 'field':
            raise XmlNodeError(xml_address, 'XML element not "field"!')
        field_type = xml_address.get('type')
        if field_type is None:
            raise XmlNodeError(xml_address, '"field"-element misses "type"-attribute!')
        field_value = xml_address.get('value')
        if field_value is None:
            raise XmlNodeError(xml_address, '"field"-element misses "value"-attribute!')
        return {field_type: field_value}

    def process_cfg_file(self) -> None:
        """Process config file and trigger db file creation."""
        try:
            cfg_file_tree = xmlEleTree.parse(self.file_path)
        except FileNotFoundError:
            self.logger.write(f'{AsciiFormat.error}File "{self.file_path}" not found!')
            return
        except xmlEleTree.ParseError as msg:
            self.logger.write(f'{AsciiFormat.error}File "{self.file_path}" can not be parsed! Corrupt/not xml file?')
            self.logger.write(f'Parser message: {msg}')
            return
        cfg_file_root = cfg_file_tree.getroot()
        ns = {'ns': cfg_file_root.tag.split(sep='{')[1].split(sep='}')[0]}
        # Load sources
        cfg_sourcefiles = cfg_file_root.findall('ns:sourcefile', ns)
        if not cfg_sourcefiles:
            self.logger.write(f'{AsciiFormat.warning}No sources are defined in {self.file_path}')
        else:
            for sourcefile in cfg_sourcefiles:
                # Check if sourcefile exists
                if not os.path.isfile(sourcefile.get('path')):
                    self.logger.write(f'{AsciiFormat.warning}{os.path.abspath(sourcefile.get("path"))} '
                                      f'does not point to an existing file!')
                    continue
                # Parse source file according to type
                sourcefile_label = sourcefile.get('label')
                self.logger.write(f'Source {sourcefile_label} is loaded from "{sourcefile.get("path")}".')
                if sourcefile.get('type') == 'xml-variables':
                    # parse aliases
                    self.logger.write('...Processing aliases.')
                    aliases = {}
                    for sourcefile_alias in sourcefile.findall('ns:alias', ns):
                        alias_attributes = sourcefile_alias.attrib
                        try:
                            aliases[alias_attributes['handle']] = alias_attributes['surrogate']
                        except KeyError:
                            self.logger.write(f'{AsciiFormat.warning}Non-conform alias element: '
                                              f'Missing "handle" and/or "surrogate" attribute!')
                            continue
                    # parse xmlfile
                    self.logger.write('...Loading source xml file.')
                    self.load_source(sourcefile.get('path'), sourcefile_label, aliases=aliases)
                else:
                    self.logger.write(f'{AsciiFormat.warning}Source file type {sourcefile.get("type")} is unknown. '
                                      f'Source file {sourcefile.get("path")} labeled '
                                      f'{sourcefile.get("label")} will be ignored!\n')
                    continue
        # Process output files
        cfg_outputfiles = cfg_file_root.findall('ns:outputfile', ns)
        if not cfg_outputfiles:
            self.logger.write(f'{AsciiFormat.error}No output files are defined in {self.file_path}')
            sys.exit(1)
        for output_file in cfg_outputfiles:
            if output_file.get('path') is None:
                self.logger.write(f'{AsciiFormat.error}No path is defined for an outputfile. File omitted!')
                continue
            self.logger.write('Compiling EPICS database.')
            database = DbFile(output_file.get('path'), logging=self.logger)
            file_autosave = str(output_file.get('autosave')).lower in ['true', '1']
            autosave_list = []
            doc_list = []
            file_tier_fields = {}
            for field in output_file.findall('ns:field', ns):
                try:
                    file_tier_fields.update(self._process_field_element(field))
                except XmlNodeError as inst:
                    self.logger.write(f'{AsciiFormat.error}{inst.Message} It will be ignored!')
                    continue
            for recordgroup in output_file.findall('ns:recordgroup', ns):
                record_type = recordgroup.get('type')
                if record_type is None:
                    self.logger.write(f'{AsciiFormat.error}"recordgroup"-element of "outputfile"-element '
                                      f'"{output_file.get("path")}" misses "type"-attribute! It will be ignored!')
                    continue
                recordgroup_tier_fields = dict(file_tier_fields)  # Copy file tier fields in new dict
                for field in recordgroup.findall('ns:field', ns):
                    try:
                        recordgroup_tier_fields.update(self._process_field_element(field))
                    except XmlNodeError as inst:
                        self.logger.write(f'{AsciiFormat.error}{inst.Message} It will be ignored!')
                        continue
                if str(recordgroup.get('autosave')).lower() in ['true', '1']:
                    recordgroup_autosave = True
                elif str(recordgroup.get('autosave')).lower() in ['false', '0']:
                    recordgroup_autosave = False
                else:
                    recordgroup_autosave = file_autosave
                for record in recordgroup.findall('ns:record', ns):
                    # Check mandatory attributes for record element
                    if record.get('pvName') is None:
                        self.logger.write(f'{AsciiFormat.error}"record"-element of "outputfile"-element '
                                          f'"{output_file.get("path")}" misses "pvName"-attribute! It will be ignored!')
                        continue
                    if record.get('source') is None:
                        self.logger.write(f'{AsciiFormat.error}"record"-element of "outputfile"-element '
                                          f'"{output_file.get("path")}" misses "source"-attribute! It will be ignored!')
                        continue
                    # Read field elements of record
                    record_fields = dict(recordgroup_tier_fields)
                    for field in record.findall('ns:field', ns):
                        try:
                            record_fields.update(self._process_field_element(field))
                        except XmlNodeError as inst:
                            self.logger.write(f'{AsciiFormat.error}{inst.Message} It will be ignored!')
                            continue
                    # Process source attribute
                    try:
                        source_label, source_path = record.get('source').split('.', 1)
                    except ValueError:
                        source_label = None
                        source_path = record.get('source')
                    if source_label is None:  # No string expansion without defined source
                        for key in record_fields:
                            record_fields[key] = self._expand(record_fields[key], {},
                                                              {'source': record.get('source'), 'pvName': record.get('pvName')})
                        database.add({
                            'devicePath': source_path,
                            'pvName': record.get('pvName'),
                            'recordType': record_type,
                            'fields': record_fields
                        })
                    else:  # Expanding device path and field values
                        source_aliases = self._sources[source_label].aliases
                        device_path = self._expand(source_path, source_aliases)
                        source_link = self._sources[source_label][device_path]
                        for key in record_fields:
                            record_fields[key] = self._expand(record_fields[key], source_aliases, source_link)
                        database.add({
                            'devicePath': device_path,
                            'pvName': record.get('pvName'),
                            'recordType': record_type,
                            'fields': record_fields
                        })
                        try:  # Remove source entry from list of remaining entries.
                            self._remaining_source_entries[source_label].remove(device_path)
                        except ValueError:
                            self.logger.write(f'{AsciiFormat.warning}No entry for {device_path} in list of remaining entries! '
                                              f'Either not present in source file or already used.')
                        doc_list_entry = '/'.join(self._expand("+{:description}", source_aliases, source_link).split(' - ')[-2:])
                        doc_list.append(f'{record.get("pvName")} ({record_type}): {doc_list_entry}')
                    if str(record.get('autosave')).lower() in ['true', '1']:
                        record_autosave = True
                    elif str(record.get('autosave')).lower() in ['false', '0']:
                        record_autosave = False
                    else:
                        record_autosave = recordgroup_autosave
                    if record_autosave:  # Add pv name to autosave list
                        autosave_list.append(record.get('pvName'))
            # Write db-file
            self.logger.write(f'Writing file: "{database.file_path}".')
            database.write_db_file(self.file_path)  # file_path for comment in db-file, not path to db-file itself.
            # Write autosave .req-file
            if output_file.get('autosavePath') is None:
                autosave_path = os.path.abspath(f'{output_file.get("path").rsplit(".", 1)[0]}.req')
            else:
                autosave_path = os.path.abspath(output_file.get('autosavePath'))
            if autosave_list:
                self.logger.write(f'Writing autosave file: "{autosave_path}".')
                with open(autosave_path, 'w') as autosave_file:
                    autosave_file.write('\n'.join(autosave_list) + '\n')
            # Generate documentation for PVs
            docfile_path = os.path.abspath(f'{output_file.get("path").rsplit(".", 1)[0]}_descriptions.txt')
            if doc_list:
                self.logger.write(f'Writing PV descriptions to file: "{docfile_path}".')
                doc_list_compiled = '\n'.join(sorted(doc_list))
                with open(docfile_path, 'w') as docfile:
                    docfile.write(f'Descriptions for PVs defined in "{self.file_path}"\n\n{doc_list_compiled}')
        # Process ignore section
        cfg_ignore = cfg_file_root.find('ns:ignore', ns)
        if cfg_ignore:
            cfg_ignore_records = cfg_ignore.findall('ns:record', ns)
            for ignore_record in cfg_ignore_records:
                source_label, source_path = ignore_record.get('source').split('.', 1)
                source_aliases = self._sources[source_label].aliases
                device_path = self._expand(source_path, source_aliases)
                try:
                    self._remaining_source_entries[source_label].remove(device_path)
                except ValueError:
                    self.logger.write(f'{AsciiFormat.warning}No entry for {device_path} in remaining entries! '
                                      f'Either not present in source file or already used.')
            cfg_ignore_masks = cfg_ignore.findall('ns:mask', ns)
            for ignore_mask in cfg_ignore_masks:
                source_label = ignore_mask.get('sourceLabel')
                filtered = [entry for entry in self._remaining_source_entries[source_label] if not re.match(ignore_mask.get('regex'), entry)]
                self._remaining_source_entries[source_label] = filtered
        # Compile list of unused source entries to log
        list_unprocessed = []
        for label, content in self._remaining_source_entries.items():
            header = AsciiFormat.colored('Sourcefile label: ', 'green') + AsciiFormat.bold(label)
            address_list = '\n'.join(content)
            list_unprocessed.append(f'\n{header}\n{address_list}')
        unprocessed = '\n'.join(list_unprocessed)
        self.logger.write(f'Processing config file complete!\n\n'
                          f'{AsciiFormat.colored("The following entries in the sourcefiles were not processed:", "BoldCyan")}\n'
                          f'{unprocessed}')


CLAP = argparse.ArgumentParser(
    description='Generates EPICS PV database for every \'PV\' defined in ChimeraTK-xml file to EPICS database file.')
CLAP.add_argument('config_file',
                  help='Path to configuration file. Defaults to "mapConfig.xml"')
CLAP.add_argument('-l',
                  help='Define path to logfile. Defaults to dbGen.log in CWD.',
                  metavar='logfile',
                  default='dbGen.log')
CLAP.add_argument('-g',
                  help='Generates config file from xml-variables file, specified in "path".',
                  metavar='variable_file')
# Parse Command Line Arguments
CLA = CLAP.parse_args()

# initiate logging
log = Logging(CLA.l)

if CLA.g is not None:  # generate config file
    config = EpicsCfg(os.path.abspath(CLA.config_file), logger=log)
    config.load_source(CLA.g, 'xmlLabel')
    config.generate_config_file('xmlLabel')
else:  # Load config file
    config = EpicsCfg(os.path.abspath(CLA.config_file), logger=log)
    config.process_cfg_file()
