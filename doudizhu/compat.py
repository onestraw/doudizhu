# -*- coding: utf-8 -*-

"""copy from requests
requests.compat
~~~~~~~~~~~~~~~

This module handles import compatibility issues between Python 2 and
Python 3.
"""
import sys


# Syntax sugar.
_ver = sys.version_info

#: Python 2.x?
is_py2 = (_ver[0] == 2)

#: Python 3.x?
is_py3 = (_ver[0] == 3)


if is_py3:
    from functools import cmp_to_key
elif is_py2:
    cmp_to_key = None
