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


def find_sections(parent_section, section_type):
    secs = parent_section.find_sections(filtr=lambda x: section_type in x.type, limit=1)
    return secs   
