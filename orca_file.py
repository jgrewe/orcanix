# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from __future__ import print_function, division

import os
import nix
import time
import uuid
import numpy as np
from IPython import embed
import orca_general as og
import orca_epochs as oe

"""
FIXME:
 Unclear whether there are more than one sessions in a single file?

 What is the difference between the file identifier and the session id?

 How are links between entities established?
"""


class OrcaFile(object):
    
    def __init__(self):
        self.__nix_file = None
        self.__section = None
        self.__block = None
        self.__general_info = None
        self.__epochs = {}

    """
    TODO
    def open(self, filename, mode='read_only'):
        if "read_only" in mode:
            file_mode = nix.FileMode.ReadOnly
        elif "read_write" in mode:
            file_mode = nix.FileMode.ReadWrite
        elif "overwrite" in mode:
            file_mode = nix.FileMode.Overwrite
        
        if not os.path.exists(filename) or file_mode == nix.FileMode.Overwrite:
            self.new(filename)
        else:
            self.nix_file = nix.File.open(filename, file_mode)
            self.__section = self.nix_file.sections['orca file']
            self.__general_info =
            self.__block =
    """
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
        self.__general_info = og.OrcaGeneral(self.__nix_file, self.__block, session_id)

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
    print(epoch.start_time)


    embed()