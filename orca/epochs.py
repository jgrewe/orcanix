# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from __future__ import print_function, division
import nix
import numpy as np


class OrcaEpoch(object):

    def __init__(self, nix_block, tag):
        self.__block = nix_block
        self.__tag = tag
        self.__ignore_intervals = None
        if tag.name + '_ignore_intervals' in nix_block.multi_tags:
            self.__ignore_intervals = nix_block.multi_tags[tag.name + '_ignore_intervals']

    @classmethod
    def new(cls, nix_block, name, start_time, end_time=None):
        tag = nix_block.create_tag(name, 'orca.epoch', [start_time])
        if end_time is not None:
            tag.extent = [end_time - start_time]
        return cls(nix_block, tag)
    
    @classmethod
    def open(cls, nix_block, tag):
        return cls(nix_block, tag)

    @property
    def name(self):
        return self.__tag.name

    @property
    def start_time(self):
        return self.__tag.position

    @property
    def end_time(self):
        return self.start_time + self.__tag.extent

    @end_time.setter
    def end_time(self, end_time):
        self.__tag.extent = end_time - self.start_time

    @property
    def description(self):
        return self.__tag.definition

    @description.setter
    def description(self, description):
        self.__tag.definition = description

    @property
    def ignore_intervals(self):
        if self.__ignore_intervals is None:
            return None
        else:
            return zip(self.__ignore_intervals.positions[:],
                       self.__ignore_intervals.positions[:] + self.__ignore_intervals.extents[:])

    @ignore_intervals.setter
    def ignore_intervals(self, intervals):
        if len(intervals) == 0:
            return
        if not isinstance(intervals, list) or not isinstance(intervals[0], tuple):
            raise TypeError('Intervals not a list of tuples!')
        starts, ends = map(list, zip(*intervals))
        extents = np.squeeze(np.asarray(ends)) - np.squeeze(np.asarray(starts))
        positions_da = self.__block.create_data_array(self.name + '_ignore_starts', 'orca.epoch.ignore_interval.start', data=starts)
        extents_da = self.__block.create_data_array(self.name + '_ignore_ends', 'orca.epoch.ignore_interval.extents', data=extents)
        self.__ignore_intervals = self.__block.create_multi_tag(self.name + '_ignore_intervals', 'orca.epoch.ignore_interval', positions_da)
        self.__ignore_intervals.extents = extents_da
