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


class OrcaFile(object):
    
    def __init__(self):
        self.nix_file = None
        self.__section = None
        self.__block = None
        self.__general_info = None

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
        self.nix_file = nix.File.open(filename, nix.FileMode.Overwrite)
        identifier = identifier if identifier else str(uuid.uuid4())
        self.__section = self.nix_file.create_section('orca file', 'orca.file')
        self.__section['orca_version'] = 0.2
        self.__section['identifier'] = identifier
        self.__section['experiment_start_time'] = experiment_start_time if experiment_start_time else time.ctime()
        self.__block = self.__nix_file.create_block(identifier, 'orca.file')

    @property
    def general_info(self):
        return self.__general_info

    @general_info.setter
    def general_info(self, info):
        if isinstance(info, og.OrcaGeneral.__class__):
            self.__general_info = info
        else:
            raise Exception('Info parameter must be of type OrcaGeneral')

    def file_info(self):
        return self.nix_file.sections['orca file']


if __name__ == '__main__':
    of = OrcaFile()
    of.new('test.orca')
    general = og.OrcaGeneral(of.nix_file, 'session_1')
    general.animal = 'animal_1'
    general.animal.species = 'C.  Elegans'
    general.animal.birthdate = '2014-12-10'
    general.device = 'Amplifier_1'
    general.device.attributes = {'a' : 100, 'b' : 200}
    general.electrical = 'magic array'
    general.electrical.electrode_map = np.arange(10, 0.5)
    embed()