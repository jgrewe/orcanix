# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from __future__ import print_function, division
import nix


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


class Sequence(object):

    def __init__(self, nix_file, nix_block, name, sequence_type):
        self.block = nix_block
        self.__nix_file = nix_file
        secs = self.__nix_file.find_sections(filtr=lambda x: name in x.name, limit=1)
        if len(secs) > 0:
            self.__section = secs[0]
        else:
            self.__section = nix_file.create_section(name, 'orca.sequence' + '.' + sequence_type)

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
    def ancestry(self):
        return get_property(self.__section, 'ancestry')

    @ancestry.setter
    def ancestry(self, value):
        set_property(self.__section, 'ancestry', value)

    @ancestry.deleter
    def ancestry(self):
        del self.__section['ancestry']

    @property
    def filter(self):
        return get_property(self.__section, 'filter')

    @filter.setter
    def filter(self, value):
        set_property(self.__section, 'filter', value)

    @filter.deleter
    def filter(self):
        del self.__section['filter']


class Position(Sequence):
    def __init__(self, nix_file, nix_block, name):
        super(Position, self).__init__(nix_file, nix_block, name, 'position')
        self.__data_array = None
        self.__lost_intervals = None
        self.__name = name

    def data(self, data, unit, sampling_rate, time_axis=0):
        self.__data_array = self.block.create_data_array(self.__name + '_positions', 'orca.sequence.position',
                                                         data=data)
        self.__data_array.unit = unit
        dim = self.__data_array.append_sampled_dimension(1./sampling_rate)
        dim.label = 'time'
        dim.unit = 's'
        # FIXME working with 2D (nD?) data

    @property
    def lost_intervals(self):
        if self.__lost_intervals is not None:
            return self.__lostintervals[:]
        else:
            return None

    @lost_intervals.setter
    def lost_intervals(self, value):
        if not isinstance(value, np.ndarray) or len(value.shape) is not 2:
            raise ValueError('Lost_intervals must be 2D numpy nd-array')
        if self.__lost_intervals is None:
            self.__lost_intervals = self.block.create_data_array(self.__name + '_lost_intervals',
                                                                 'orca.sequence.lost_intervals', data=value)
        else:
            self.__lost_intervals.extent = value.shape
            self.__lost_intervals.data = value

    @lost_intervals.deleter
    def lost_intervals(self):
        if self.__lost_intervals is not None:
            del self.block.data_arrays[self.__lost_intervals.name]
            self.__lost_intervals = None

    @property
    def conversion(self):
        print (self.__data_array.polynom_coefficients)
        if len(self.__data_array.polynom_coefficients) > 0:
            return self.__data_array.polynom_coefficients[-1]
        else:
            return 1

    @property
    def sampling_rate(self):
        dim = [d for d in self.__data_array.dimensions if d.dimension_type == nix.DimensionType.Sample][0]
        return 1./dim.sampling_interval


class Electrical(Sequence):
    pass


class PatchClamp(Sequence):
    pass


class SpikeEvents(Sequence):
    pass


class Image(Sequence):
    pass


class Optical(Image):
    pass


class TwoPhoton(Optical):
    pass