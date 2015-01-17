# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from __future__ import print_function, division
import uuid
import numpy as np


def set_property(section, prop, value):
    if section is not None:
        section[prop] = value
    else:
        raise ValueError('Section not initialized!')


def get_property(section, name):
    if section.has_property_by_name(name):
        return section[name]
    else:
        return None

def find_sections(parent_section, section_type):
    secs = parent_section.find_sections(filtr=lambda x: section_type in x.type, limit=1)
    return secs   

class OrcaGeneral(object):
    
    def __init__(self, nix_file, nix_block, general_section):
        self.__block = nix_block
        self.__nix_file = nix_file
        self.__animals = {}
        self.__devices = {}
        self.__electricals = {}
        self.__section = general_section
        for s in find_sections(self.__section, 'orca.animal'):
            self.__animals[s.name] = OrcaAnimal.from_section(s)
        for s in find_sections(self.__section, 'orca.devices'):
            self.__devices[s.name] = OrcaDevice.open(s)
        for s in find_sections(self.__section, 'orca.electrical'):
            self.__electricals[s.name] = OrcaElectrical.open(self.__block, s)

    @classmethod
    def open(cls, nix_file, nix_block, general_section):
        return cls(nix_file, nix_block, general_section)

    @classmethod
    def new(cls, nix_file, nix_block, session_id):
        secs = nix_file.find_sections(filtr=lambda x: 'session_id' in x.name, limit=1)
        if len(secs) > 0:
            section = secs[0]
        else:
            section = nix_file.create_section(session_id, 'orca.general')
        return cls(nix_file, nix_block, section)

    @property
    def session_id(self):
        return self.__section.name
        
    @property
    def experiment(self):
        return get_property(self.__section, 'experiment')

    @experiment.setter
    def experiment(self, value):
        set_property(self.__section, 'experiment', value)

    @experiment.deleter
    def experiment(self):
        del self.__section['experiment']

    @property
    def lab(self):
        return get_property(self.__section, 'lab')

    @lab.setter
    def lab(self, value):
        set_property(self.__section, 'lab', value)

    @lab.deleter
    def lab(self):
        del self.__section['lab']

    @property
    def protocol(self):
        return get_property(self.__section, 'protocol')

    @protocol.setter
    def protocol(self, value):
        set_property(self.__section, 'protocol', value)

    @protocol.deleter
    def protocol(self):
        del self.__section['protocol']

    @property
    def notes(self):
        return get_property(self.__section, 'notes')

    @notes.setter
    def notes(self, value):
        set_property(self.__section, 'notes', value)

    @notes.deleter
    def notes(self):
        del self.__section['notes']

    @property
    def animals(self):
        return self.__animals

    def add_animal(self, animal_id):
        if animal_id not in self.__animals.keys():
            self.__animals[animal_id] = OrcaAnimal.create_new(self.__section, animal_id)
        else:
            print("Animal with that id already exists in the file.")

    @property
    def devices(self):
        return self.__devices

    def add_device(self, device_name):
        if device_name not in self.__devices.keys():
            self.__devices[device_name] = OrcaDevice.new(self.__section, device_name)
        else:
            print("Device with that name already exists in the file.")

    @property
    def electricals(self):
        return self.__electricals

    def add_electrical(self, hardware):
        if hardware not in self.__electricals.keys():
            self.__electricals[hardware] = OrcaElectrical.new(self.__block, self.__section, hardware)
        else:
            print("Electrical with that name already exists in the file.")
            

class OrcaAnimal(object):

    def __init__(self, animal_section):
        self.__section = animal_section

    @classmethod
    def from_section(cls, animal_section):
        return cls(animal_section)

    @classmethod
    def create_new(cls, general_section, animal_id):
        return cls(general_section.create_section(animal_id, 'orca.animal'))
        
    @property
    def animal_id(self):
        return self.__section.name

    @animal_id.setter
    def animal_id(self, value):
        self.__section.name = value

    @animal_id.deleter
    def animal_id(self):
        del self.__section['animal_id']

    @property
    def age(self):
        return get_property(self.__section, 'age')

    @age.setter
    def age(self, value):
        set_property(self.__section, 'age', value)

    @age.deleter
    def age(self):
        del self.__section['age']

    @property
    def birthdate(self):
        return get_property(self.__section, 'birthdate')

    @birthdate.setter
    def birthdate(self, value):
        set_property(self.__section, 'birthdate', value)

    @birthdate.deleter
    def birthdate(self):
        del self.__section['birthdate']

    @property
    def species(self):
        return get_property(self.__section, 'species')

    @species.setter
    def species(self, value):
        set_property(self.__section, 'species', value)

    @species.deleter
    def species(self):
        del self.__section['species']

    @property
    def genotype(self):
        return get_property(self.__section, 'genotype')

    @genotype.setter
    def genotype(self, value):
        set_property(self.__section, 'genotype', value)

    @genotype.deleter
    def genotype(self):
        del self.__section['genotype']

    @property
    def area(self):
        return get_property(self.__section, 'area')

    @area.setter
    def area(self, value):
        set_property(self.__section, 'area', value)

    @area.deleter
    def area(self):
        del self.__section['area']


class OrcaDevice(object):

    def __init__(self, section):
        self.__section = section
    
    @classmethod
    def new(cls, general_section, device_name):
        return cls(general_section.create_section(device_name, 'orca.device'))

    @classmethod
    def open(cls, device_section):
        return cls(device_section)

    @property
    def make(self):
        return get_property(self.__section, 'make')

    @make.setter
    def make(self, value):
        set_property(self.__section, 'make', value)

    @make.deleter
    def make(self):
        del self.__section['make']

    @property
    def model(self):
        return get_property(self.__section, 'model')

    @model.setter
    def model(self, value):
        set_property(self.__section, 'model', value)

    @model.deleter
    def model(self):
        del self.__section['model']

    @property
    def serial_number(self):
        return get_property(self.__section, 'serial_number')

    @serial_number.setter
    def serial_number(self, value):
        set_property(self.__section, 'serial_number', value)

    @serial_number.deleter
    def serial_number(self):
        del self.__section['serial_number']

    @property
    def description(self):
        return get_property(self.__section, 'description')

    @description.setter
    def description(self, value):
        set_property(self.__section, 'description', value)

    @description.deleter
    def description(self):
        del self.__section['description']

    @property
    def attributes(self):
        try:
            attribs = self.__section.sections['attributes'].props
        except KeyError:
            attribs = None
        return attribs

    @attributes.setter
    def attributes(self, values):
        if isinstance(values, dict):
            try:
                del self.__section.sections['attributes']
            except KeyError:
                pass
            attr = self.__section.create_section('attributes', 'orca.device.attributes')
            for a in values.items():
                attr[a[0]] = a[1]
        else:
            raise TypeError('Values of attributes must be a dictionary of name and value')

    @attributes.deleter
    def attributes(self):
        del self.__section.sections['attributes']


class OrcaElectrical(object):

    def __init__(self, nix_block, section):
        self.__section = section
        self.__block = nix_block

    @classmethod
    def new(cls, nix_block, general_section, name):
        return cls(nix_block, general_section.create_section(name, 'orca.electrical'))

    @classmethod
    def open(cls, nix_block, electrical_section):
        return cls(nix_block, electrical_section)

    @property
    def definition(self):
        return get_property(self.__section, 'definition')

    @definition.setter
    def definition(self, definition):
        set_property(self.__section, 'definition', definition)

    @definition.deleter
    def definition(self):
        del self.__section['definition']

    @property
    def num_electrodes(self):
        return get_property(self.__section, 'num_electrodes')

    @num_electrodes.setter
    def num_electrodes(self, num_electrodes):
        set_property(self.__section, 'num_electrodes', num_electrodes)

    @num_electrodes.deleter
    def num_electrodes(self):
        del self.__section['num_electrodes']

    @property
    def hardware(self):
        return get_property(self.__section, 'hardware')

    @hardware.setter
    def hardware(self, hardware):
        set_property(self.__section, 'hardware', hardware)

    @hardware.deleter
    def hardware(self):
        del self.__section['hardware']

    @property
    def electrode_map(self):
        da = [d for d in self.__block.data_arrays if d.name == 'electrode map']
        if len(da) > 0:
            return da[0][:]
        else:
            return None

    @electrode_map.setter
    def electrode_map(self, electrode_map):
        if not isinstance(electrode_map, np.ndarray):
            raise TypeError('Electrode map must be numpy ndarray.')
        da = [d for d in self.__block.data_arrays if d.name == 'electrode map']
        if len(da) > 0:
            array = da[0]
            array.extent = electrode_map.shape
            array.data = electrode_map
        else:
            array = self.__block.create_data_array('electrode_map', 'orca.electrical.electrode_map', data=electrode_map)
            for _ in electrode_map.shape:
                array.append_set_dimension()
            array.metadata = self.__section

    @electrode_map.deleter
    def electrode_map(self):
        da = [d for d in self.__block.data_arrays if d.name == 'electrode map']
        if len(da) > 0:
            del self.__block.data_arrays[da[0]]

    @property
    def impedance(self):
        da = [d for d in self.__block.data_arrays if d.name == 'impedance']
        if len(da) > 0:
            return da[0][:]
        else:
            return None

    @impedance.setter
    def impedance(self, impedance):
        if not isinstance(impedance, np.ndarray):
            raise TypeError('Impedance must be numpy ndarray.')
        da = [d for d in self.__block.data_arrays if d.name == 'impedance']
        if len(da) > 0:
            array = da[0]
            array.extent = impedance.shape
            array.data = impedance
        else:
            array = self.__block.create_data_array('impdeance', 'orca.electrical.impedance', data=impedance)
            for _ in impedance.shape:
                array.append_set_dimension()
            array.metadata = self.__section

    @impedance.deleter
    def impedance(self):
        da = [d for d in self.__block.data_arrays if d.name == 'impedance']
        if len(da) > 0:
            del self.__block.data_arrays[da[0]]
