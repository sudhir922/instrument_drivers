from typing import Any
from qcodes.instrument.base import Instrument
import serial
import time

from qcodes import VisaInstrument, validators as vals
from qcodes.utils.helpers import create_on_off_val_mapping


class SG22000PRO(Instrument):
    """
    Written By Sudhir: driver for DS instrumnets LO
    """
    def __init__(self, name, address = 'COM4', baudrate=115200, timeout=1, **kwargs):
        super().__init__(name, **kwargs)
        self.ser = serial.Serial(address, baudrate=baudrate, timeout=timeout)
        time.sleep(2) 

        self.add_parameter(name='frequency',
                           label='Frequency',
                           unit='Hz',
                           set_cmd="FREQ:CW {:.0f}HZ\n".encode('utf-8'),
                           get_parser=float,
                           vals=vals.Numbers(1e6, 24e9))
        self.add_parameter(name='power',
                           label='Power',
                           unit='dBm',
                           set_cmd="POWER {:.1f}\n".encode('utf-8'),
                           get_parser=float,
                           vals=vals.Numbers(-120, 20))
        self.add_parameter('status',
                           label='RF Output',
                           set_cmd="OUTP:STAT {}\n".encode('utf-8'),
                           val_mapping=create_on_off_val_mapping(on_val='ON',
                                                                 off_val='OFF'))
        # self.add_parameter('ref_osc_source',
        #                    label='Reference Oscillator Source',
        #                    get_cmd='SOUR:ROSC:SOUR?',
        #                    set_cmd='SOUR:ROSC:SOUR {}',
        #                    vals=vals.Enum('INT', 'EXT', 'int', 'ext'))
        # # Define LO source INT/EXT (Only with K-90 option)
        # self.add_parameter('LO_source',
        #                    label='Local Oscillator Source',
        #                    get_cmd='SOUR:LOSC:SOUR?',
        #                    set_cmd='SOUR:LOSC:SOUR {}',
        #                    vals=vals.Enum('INT', 'EXT', 'int', 'ext'))
        # # Define output at REF/LO Output (Only with K-90 option)
        # self.add_parameter('ref_LO_out',
        #                    label='REF/LO Output',
        #                    get_cmd='CONN:REFL:OUTP?',
        #                    set_cmd='CONN:REFL:OUTP {}',
        #                    vals=vals.Enum('REF', 'LO', 'OFF', 'ref', 'lo',
        #                                   'off', 'Off'))
        # # Frequency mw_source outputs when used as a reference
        # self.add_parameter('ref_osc_output_freq',
        #                    label='Reference Oscillator Output Frequency',
        #                    get_cmd='SOUR:ROSC:OUTP:FREQ?',
        #                    set_cmd='SOUR:ROSC:OUTP:FREQ {}',
        #                    vals=vals.Enum('10MHz', '100MHz', '1000MHz'))
        # # Frequency of the external reference mw_source uses
        # self.add_parameter('ref_osc_external_freq',
        #                    label='Reference Oscillator External Frequency',
        #                    get_cmd='SOUR:ROSC:EXT:FREQ?',
        #                    set_cmd='SOUR:ROSC:EXT:FREQ {}',
        #                    vals=vals.Enum('10MHz', '100MHz', '1000MHz'))

        # # IQ impairments
        # self.add_parameter('IQ_impairments',
        #                    label='IQ Impairments',
        #                    get_cmd=':SOUR:IQ:IMP:STAT?',
        #                    set_cmd=':SOUR:IQ:IMP:STAT {}',
        #                    val_mapping=create_on_off_val_mapping(on_val='1',
        #                                                          off_val='0'))
        # self.add_parameter('I_offset',
        #                    label='I Offset',
        #                    get_cmd='SOUR:IQ:IMP:LEAK:I?',
        #                    set_cmd='SOUR:IQ:IMP:LEAK:I {:.2f}',
        #                    get_parser=float,
        #                    vals=vals.Numbers(-10, 10))
        # self.add_parameter('Q_offset',
        #                    label='Q Offset',
        #                    get_cmd='SOUR:IQ:IMP:LEAK:Q?',
        #                    set_cmd='SOUR:IQ:IMP:LEAK:Q {:.2f}',
        #                    get_parser=float,
        #                    vals=vals.Numbers(-10, 10))
        # self.add_parameter('IQ_gain_imbalance',
        #                    label='IQ Gain Imbalance',
        #                    get_cmd='SOUR:IQ:IMP:IQR?',
        #                    set_cmd='SOUR:IQ:IMP:IQR {:.2f}',
        #                    get_parser=float,
        #                    vals=vals.Numbers(-1, 1))
        # self.add_parameter('IQ_angle',
        #                    label='IQ Angle Offset',
        #                    get_cmd='SOUR:IQ:IMP:QUAD?',
        #                    set_cmd='SOUR:IQ:IMP:QUAD {:.2f}',
        #                    get_parser=float,
        #                    vals=vals.Numbers(-8, 8))

    #     self.add_function('reset', call_cmd='*RST')
    #     self.add_function('run_self_tests', call_cmd='*TST?')

    #     self.connect_message()

    # def on(self) -> None:
    #     self.status('on')

    # def off(self) -> None:
    #     self.status('off')
