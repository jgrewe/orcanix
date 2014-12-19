# !/usr/bin/env python
#  -*- coding: utf-8 -*-
from __future__ import print_function, division
import nix
import numpy as np


class OrcaEpoch(object):

    def __init__(self, nix_block, name, start_time, end_time=None):
        self.__block = nix_block
        self.__tag = self.__block.create_tag(name, 'orca.epoch', [start_time])
        self.__ignore_interval_starts = None
        self.__ignore_interval_ends = None
        if end_time is not None:
            self.__tag.extent = [end_time - start_time]

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
            return zip(self.__ignore_interval_starts[:],
                       self.__ignore_interval_ends[:] - self.__ignore_interval_starts[:])

    @ignore_intervals.setter
    def ignore_intervals(self, intervals):
        if not isinstance(intervals, list):
            raise TypeError('Intervals must be list of tuples!')
        if len(intervals) is 0 or not isinstance(intervals[0], tuple):
            raise TypeError('Intervals is empty or not a list of tuples!')
        starts, ends = map(list, zip(*intervals))
        self.__block.create_data_array(self.name + '_ignore_starts', 'orca.epoch.ignore_interval.start', data=starts)
        self.__block.create_data_array(self.name + '_ignore_ends', 'orca.epoch.ignore_interval.end', data=ends)
