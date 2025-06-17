from functools import partial
from typing import Optional, Union, Any
from time import sleep
import numpy as np

from qcodes.instrument.parameter import DelegateParameter
from qcodes.instrument.visa import VisaInstrument
from qcodes import VisaInstrument, validators as vals
from qcodes.instrument.channel import InstrumentChannel
from qcodes.utils.validators import Numbers, Bool, Enum, Ints


class Yokogawa7651(VisaInstrument):
    """
    This is the QCoDeS driver for the Yokogawa GS200 voltage and current source.

    Args:
      name: What this instrument is called locally.
      address: The GPIB or USB address of this instrument
      kwargs: kwargs to be passed to VisaInstrument class
      terminator: read terminator for reads/writes to the instrument.
    """

    def __init__(self, name: str, address: str, terminator: str = "\n",
                 **kwargs: Any) -> None:
        super().__init__(name, address, terminator=terminator, **kwargs)

        self.add_parameter(name = 'status',
                           label='status',
                           get_cmd='OC;<GET>',
                           set_cmd='O{};E',
                           vals = vals.Enum("off","on", False, True),
                           val_mapping={'off': 0, 'on': 1, False: 0, True: 1},)

        self.add_parameter(name= 'source_mode',
                           label='Source Mode',
                           set_cmd='F{};E',
                           vals = vals.Enum("Voltage","Current"),
                           val_mapping={'Voltage': 1, 'Current': 5})
        
        self.add_parameter('voltage',
                    label='Voltage',
                    get_cmd='OD;<GET>',
                    set_cmd= 'S{};E',
                    unit='V')
        
        self.add_parameter('Current',
                    label='Current',
                    get_cmd='OD;<GET>',
                    set_cmd= 'S{};E')

        self.add_parameter('voltage_range',
                           label='Voltage Source Range',
                           unit='V',
                           set_cmd='R{};E',
                           vals=vals.Enum("10mV", "100mV", "1V", "10V","100V"),
                           val_mapping={
                               "10mV": 2,"100mV": 3, "1V": 4 ,"10V": 5, "100V": 6})
        
        self.add_parameter('current_range',
                    label='Current Source Range',
                    unit='A',
                    set_cmd='R{};E',
                    vals=vals.Enum("1mA", "10mA","100mA"),
                    val_mapping={"1mA": 4 ,"10mA": 5, "100mA": 6})
        
        self.add_parameter('compliance_voltage',
                    label='Compliance Voltage',
                    unit='V',
                    set_cmd="LV{};E",
                    vals=vals.Enum(1, 30))
        self.add_parameter('compliance_current',
            label='Compliance Current',
            unit='A',
            set_cmd="LA{};E",
            vals=vals.Enum(5e-3, 120e-3))

    def ramp_to_voltage(self, volt, steps=25, duration=0.5):
        """ Ramps the voltage to a value in Volts by traversing a linear spacing
        of voltage steps over a duration, defined in seconds.

        :param steps: A number of linear steps to traverse
        :param duration: A time in seconds over which to ramp
        """
        start_volt = float(self.voltage()[5:-1])
        stop_volt = volt
        pause = duration / steps
        if (start_volt != stop_volt):
            volts = np.linspace(start_volt, stop_volt, steps)
            for volt in volts:
                self.voltage(volt)
                sleep(pause)

    def ramp_to_current(self, current, steps=25, duration=0.5):
        """ Ramps the current to a value in Amps by traversing a linear spacing
        of current steps over a duration, defined in seconds.

        :param steps: A number of linear steps to traverse
        :param duration: A time in seconds over which to ramp
        """
        start_current = self.source_current
        stop_current = current
        pause = duration / steps
        if (start_current != stop_current):
            currents = np.linspace(start_current, stop_current, steps)
            for current in currents:
                self.source_current = current
                sleep(pause)
    