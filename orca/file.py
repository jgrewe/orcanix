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

 Here are some comments/questions regaring the schema:

    Unclear whether it is intended to have  more than one sessions in a single file?

    What is the difference between the file identifier and the session id?

    Naming of entities? So far only a few entities have names. If there are to be more than one, this is confusing.

 General:
            This seems to me to be meant as an entity to represent sessions.  I named it session instead of general.

 Positions:
            Axis information is difficult. How should this be solved? I put in the labels e.g. for x-position and y-position

            Unit of time axis always in seconds?

            Is it always a time axis?

            Are the positions expected to work with nD or rather limited to 2D? So far implemented to work correctly with 2D

            Ignore intervals are implemented as start and extents (the nix apporach) but the object takes and returns starts and ends.

 Sequences in general:
            Sample rate and t_intervals can be contradictory/in conflict!

            Regarding the time information I would argue to define separate classes for the Neurolynx kind of data and
            regular as well as irregularly sampled data. If handled in the wrong way using the combination of
            timestamps, intervals and samplerate can easily lead to a terrible mess.

            Conversion and resolution in Sequence appear redundant.

            Not sure if I understand ancestry correctly. Handled this as the type of the sequence. Is this the intended behavior?

"""


class OrcaFile(object):
    
    def __init__(self, nix_file, section):
        self.__nix_file = nix_file
        self.__section = section
        self.__nix_file.sections 
        self.__epochs = {}
        self.__sequences = {}
        self.__session = None
        for b in self.__nix_file.blocks:
            if "orca.session" in b.type:
                self.__session =  og.OrcaGeneral.open(self.__nix_file, b)
                break;
        if self.__session is not None:
            epochs = [t for t in self.__session._block().tags if 'orca.epoch' in t.type]
            for e in epochs:
                self.__epochs[e.name] = oe.OrcaEpoch.open(self.__session._block(), e)
            seqs = self.__nix_file.find_sections(filtr=lambda x: 'orca.sequence' in x.type, limit=2)
            self.__open_sequences(seqs)
    
    @classmethod
    def open(cls, filename, file_mode=nix.FileMode.ReadWrite):
        nix_file = nix.File.open(filename, file_mode)
        section = nix_file.sections['orca file']
        return cls(nix_file, section)
    
    @classmethod
    def new(cls, filename, identifier=None, experiment_start_time=None):
        nix_file = nix.File.open(filename, nix.FileMode.Overwrite)
        identifier = identifier if identifier else str(uuid.uuid4())
        section = nix_file.create_section('orca file', 'orca.file')
        section['orca_version'] = 0.2
        section['identifier'] = identifier
        section['experiment_start_time'] = experiment_start_time if experiment_start_time else time.ctime()
        return cls(nix_file, section)

    def __open_sequences(self, sequence_sections):
        for s in sequence_sections:
            print ("open sequences")
            print (sequence_sections)
            sequence_type = s.type.split('.')[-1]
            if sequence_type not in self.__sequences.keys():
                self.__sequences[sequence_type] = []
            sequence = None
            if sequence_type == 'position':
                sequence = seq.Position.open(self.__session._block(), s)
            # elif sequence_type == 'electrical':
            #    seq = seq.Electrical.open(self.__session, s)
            # TODO other types
            if sequence is not None:
                print (sequence_type)
                self.__sequences[sequence_type].append(sequence)
            
    @property
    def session(self):
        return self.__session

    @session.setter
    def session(self, session_id):
        self.__session = og.OrcaGeneral.new(self.__nix_file, session_id)

    @property
    def file_info(self):
        return self.__nix_file.sections['orca file']

    def add_epoch(self, name, start_time, end_time=None):
        if name in self.__epochs.keys():
            raise KeyError('An epoch with this name already exists!')
        self.__epochs[name] = oe.OrcaEpoch.new(self.__session._block(), name, start_time, end_time)
        return self.__epochs[name]
    
    @property
    def epochs(self):
        return self.__epochs

    def add_position_data(self, name, data, labels, sampling_rate, lost_intervals=None):
        if 'position_data' not in self.__sequences:
            self.__sequences['position'] = []
        self.__sequences['position'].append(seq.Position.new(self.__nix_file, self.__session._block(), name))
        self.__sequences['position'][-1].data(data, labels, 'mV', sampling_rate)
        if lost_intervals is not None:
            self.__sequences['position'][-1].lost_intervals(lost_intervals)
        return self.__sequences['position'][-1]

    @property
    def sequences(self):
        return self.__sequences

    def close(self):
        self.__nix_file.close()


if __name__ == '__main__':
    print('... create new file...')
    of = OrcaFile.new('test.orca', 'session_1')
    of.session = 'session_1'
    of.session.add_animal('animal_1')
    of.session.animals['animal_1'].species = 'C.  Elegans'
    of.session.animals['animal_1'].birthdate = '2014-12-10'
    of.session.add_device('Amplifier_1')
    of.session.devices['Amplifier_1'].model = 'Amplifier'
    of.session.devices['Amplifier_1'].attributes = {'a' : 100, 'b' : 200}
    of.session.add_electrical('electrode array')
    of.session.electricals['electrode array'].electrode_map = np.arange(10, 0.5)
    epoch = of.add_epoch('epoch_1', 0.0, 10.2)
    epoch.description = 'An epoch in some data'
    epoch.ignore_intervals = [(0.0, 1.1), (1.5, 2.7), (7.5, 7.6)]
    p = of.add_position_data('position data', np.random.randn(100, 2), ['x', 'y'], 100)
    p.description = "description of the position data"
    embed()
    of.close()
    print('... close file!')

    print('... Reopen file and read some stuff...')
    of = None # set to none when reusing variable
    of = OrcaFile.open('test.orca', nix.FileMode.ReadWrite)
    print (of.sequences.keys())
    pos = of.sequences['position'][0]
    print(pos.name)
    print(pos.ancestry)
    print(pos.positions)
    
    of.close()
    print('...done!')
