# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from __future__ import print_function, division

import os
import nix
import time
import numpy as np
import uuid

from IPython import embed

class OrcaFile(object):
    
    def __init__(self):
        self.nix_file = None
        self.file_info = None

    def open(self, filename, identifier=None, mode='read_only'):
        if "read_only" in mode:
            file_mode = nix.FileMode.ReadOnly
        elif "read_write" in mode:
            file_mode = nix.FileMode.ReadWrite
        elif "overwrite" in mode:
            file_mode = nix.FileMode.Overwrite
        
        if not os.path_exists(filename) or file_mode == nix.FileMode.Overwrite: 
            self.nix_file = new(filename)
        else:
            self.nix_file = nix.File.open(filename, file_mode)
        
    def new(self, filename, identifier=None, experiment_start_time=None):
        self.nix_file = nix.File.open(filename, nix.FileMode.Overwrite)
        self.file_info = self.nix_file.create_section('orca file', 'orcanix.file')
        self.file_info['orca_version'] = 0.2
        self.orce_info['identifier'] = identifier if identifier else str(uuid.uuid4())
        self.file_info['experiment_start_time'] = experiment_start_time if experiment_start_time else time.ctime() 
        
    
    def file_info():
        return self.nix_file.sections['orca file']


if __name__ == '__main__':
    of = OrcaFile()
    of.new('test.orca')
    print (of.file_info())
