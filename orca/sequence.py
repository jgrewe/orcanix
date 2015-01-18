# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from __future__ import print_function, division
from util import *
import nix
from IPython import embed

class Sequence(object):

    def __init__(self, nix_block, sequence_section):
        self.block = nix_block
        self.section = sequence_section

    @property
    def description(self):
        return get_property(self.section, 'description')

    @description.setter
    def description(self, value):
        set_property(self.section, 'description', value)

    @description.deleter
    def description(self):
        del self.section['description']

    @property
    def ancestry(self):
        return self.section.type

    @property
    def filter(self):
        return get_property(self.section, 'filter')

    @filter.setter
    def filter(self, value):
        set_property(self.section, 'filter', value)

    @filter.deleter
    def filter(self):
        del self.section['filter']


class Position(Sequence):
    def __init__(self, nix_block, section):
        super(Position, self).__init__(nix_block, section)
        self.__name = section.name
        self.__data_array = None
        if section.name + '_positions' in nix_block.data_arrays:
            self.__data_array = nix_block.data_arrays[section.name + '_positions']
        self.__lost_intervals = None
        if section.name + '_lost_intervals' in nix_block.data_arrays:
            self.__lost_intervals = nix_block.data_arrays[section.name + '_lost_intervals']
        
    @classmethod
    def new(cls, nix_file, nix_block, name):
        s = nix_file.create_section(name, 'orca.sequence.position')
        return cls(nix_block, s)

    @classmethod
    def open(cls, nix_block, section):
        return cls(nix_block, section)
        
    @property
    def name(self):
        return self.__name

    @property
    def positions(self):
        return self.__data_array[:]
        
    def data(self, data, labels, unit, sampling_rate, time_axis=None):
        """
        Set the data of the Position entity. 
        @param data The data, numpy array
        @param unit the unit of the sampled data
        @param sampling_rate the rate with which the data was sampled.
        @param time_axis and samplingrate are mutually exclusive. If time_axis given it has the higher
        priority.
        """
        self.__data_array = self.block.create_data_array(self.name + '_positions', 'orca.sequence.position',
                                                         data=data)
        self.__data_array.unit = unit
        if sampling_rate is None and time_axis is None:
            raise ValueError("Sequence.Position: require either sampling_rate or time_interval.")
        if time_axis is None and sampling_rate is not None:
            dim = self.__data_array.append_sampled_dimension(1./sampling_rate)
        if time_axis is not None:
            if len(time_axis) != data.shape[0]:
                raise ValueError("Length of time axis must match first number of elements in the first dimension of the data.")
            dim = self.__data_array.append_range_dimension(time_axis)
        dim.label = 'time'
        dim.unit = 's'
        set_dim = self.__data_array.append_set_dimension()
        set_dim.labels = labels
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
            self.__lost_intervals = self.block.create_data_array(self.name + '_lost_intervals',
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


class Neurolynx(Sequence):
    pass


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