# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from __future__ import print_function, division
import uuid
from IPython import embed

def set_property(section, prop, value):
    if section is not None:
        section[prop] = value
    else:
        raise Exception('section not initialized!')


def get_property(section, name):
    if section.has_property_by_name(name):
        return section[name]
    else:
        return None


class OrcaGeneral(object):
    
    def __init__(self, nix_file, session_id=None):
        self.__nix_file = nix_file
        self.__animal = None
        self.__device = None
        self.__electric = None
        if session_id is None:
            session_id = str(uuid.uuid4())
        self.__section = nix_file.create_section(session_id, 'orca.general')
        set_property(self.__section, 'session_id', session_id)

    @property
    def session_id(self):
        return get_property(self.__section, 'session_id')

    @session_id.deleter
    def session_id(self):
        del self.__section['session_id']

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
    def animal(self):
        return self.__animal

    @animal.setter
    def animal(self, animal_id):
        self.__animal = OrcaAnimal(self.__nix_file, self.session_id)
        self.__animal.animal_id = animal_id

    @property
    def device(self):
        return self.__device

    @device.setter
    def device(self, model):
        self.__device = OrcaDevice(self.__nix_file, self.session_id)
        self.__device.model= model


class OrcaAnimal(object):

    def __init__(self, nix_file, session_id):
        try:
            s = nix_file.sections[session_id]
        except:
            raise Exception('Invalid session ID.')
        self.__section = s.create_section('Animal', 'orca.animal')

    @property
    def animal_id(self):
        return get_property(self.__section, 'animal_id')

    @animal_id.setter
    def animal_id(self, value):
        set_property(self.__section, 'animal_id', value)

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

    def __init__(self, nix_file, session_id):
        try:
            s = nix_file.sections[session_id]
        except:
            raise Exception('Invalid session ID.')
        self.__section = s.create_section('Device', 'orca.device')

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
        except:
            attribs = None
        return attribs

    @attributes.setter
    def attributes(self, values):
        if isinstance(values, dict):
            try:
                del self.__section.sections['attributes']
            except:
                pass
            attr = self.__section.create_section('attributes', 'orca.device.attributes')
            for a in values.items():
                attr[a[0]] = a[1]
        else:
            raise Exception('Values of attributes must be a dictionary of name and value')

    @attributes.deleter
    def attributes(self):
        del self.__section.sections['attributes']
