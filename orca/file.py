# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from __future__ import print_function, division

import time
import uuid
import numpy as np
from IPython import embed

import nix

import sequence as seq
import general as og
import epochs as oe


"""
FIXME:
 Unclear whether it is intended to have  more than one sessions in a single file?

 What is the difference between the file identifier and the session id?

 How are links between entities established?

 Naming of entities? So far only a few entities have names. If there are to be more than one, this is confusing.

 Positions:
            Axis information is difficult. How should this be solved?
            Unit of time axis always in seconds?
            What about the other axes in the nD case?
  Sequences in general:
            Sample rate and t_intervals can be contradictory/in conflict!
            Regarding the time information I would argue to define separate classes for the Neurolynx kind of data and
            regular as well as irregularly sampled data. If handled in the wrong way using the combination of
            timestamps, intervals and samplerate can easily lead to a terrible mess.
            Conversion and resolution in Sequence appear redundant!
            Not sure if I understand ancestry correctly. Handled this as the type of the sequence
"""


class OrcaFile(object):
    
    def __init__(self):
        self.__nix_file = None
        self.__section = None
        self.__block = None
        self.__general_info = None
        self.__epochs = {}
        self.__data = {}

    def open(self, filename, file_mode=nix.FileMode.Overwrite):        
        self.nix_file = nix.File.open(filename, file_mode)
        self.__section = self.nix_file.sections['orca file']
        # self.__general_info =
        # self.__block =
    
    def new(self, filename, identifier=None, experiment_start_time=None):
        self.__nix_file = nix.File.open(filename, nix.FileMode.Overwrite)
        identifier = identifier if identifier else str(uuid.uuid4())
        self.__section = self.__nix_file.create_section('orca file', 'orca.file')
        self.__section['orca_version'] = 0.2
        self.__section['identifier'] = identifier
        self.__section['experiment_start_time'] = experiment_start_time if experiment_start_time else time.ctime()
        self.__block = self.__nix_file.create_block(identifier, 'orca.file')

    @property
    def general_info(self):
        return self.__general_info

    @general_info.setter
    def general_info(self, session_id):
        self.__general_info = og.OrcaGeneral.create_new(self.__nix_file, self.__block, session_id)

    @property
    def file_info(self):
        return self.__nix_file.sections['orca file']

    def add_epoch(self, name, start_time, end_time=None):
        if name in self.__epochs.keys():
            raise KeyError('An epoch with this name already exists!')
        self.__epochs[name] = oe.OrcaEpoch(self.__block, name, start_time, end_time)
        return self.__epochs[name]

    def epochs(self):
        return self.__epochs

    def add_position_data(self, name, data, labels, sampling_rate, lost_intervals=None):
        if 'position_data' not in self.__data:
            self.__data['position_data'] = []
        self.__data['position_data'].append(seq.Position(self.__nix_file, self.__block, name))
        self.__data['position_data'][-1].data(data, labels, 'mV', sampling_rate)
        #        self.__data['position_data'][-1].lost_intervals(lost_intervals)


if __name__ == '__main__':
    of = OrcaFile()
    of.new('test.orca', 'test_session')
    of.general_info = 'session_1'
    of.general_info.animal = 'animal_1'
    of.general_info.animal.species = 'C.  Elegans'
    of.general_info.animal.birthdate = '2014-12-10'
    of.general_info.device = 'Amplifier_1'
    of.general_info.device.attributes = {'a' : 100, 'b' : 200}
    of.general_info.electrical = 'magic array'
    of.general_info.electrical.electrode_map = np.arange(10, 0.5)
    epoch = of.add_epoch('test', 0.0, 10.2)
    epoch.description = 'A test epoch'
    epoch.ignore_intervals = [(0.0, 1.1), (1.5, 2.7), (7.5, 7.6)]
    of.add_position_data('test data', ['x', 'y'], np.random.randn((100,2)), 100)

    embed()
