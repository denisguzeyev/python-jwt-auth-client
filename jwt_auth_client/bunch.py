# -*- coding: utf-8 -*-
"""local variables for tests"""

from __future__ import print_function

from io import BytesIO

NESTED = 'nested'
DOTTED = 'dotted'


class Bunch(dict):
    """Collector of model fixtures"""

    def __init__(self, initial_dict={}, **kw):
        """Init"""
        dict.__init__(self, kw)
        self.__dict__ = self
        self.update(initial_dict)

    def __getstate__(self):
        """Get state"""
        return self

    def __setstate__(self, state):
        """Set state"""
        self.update(state)
        self.__dict__ = self

    def __str__(self):
        """Stringify"""
        attr = ["%s=%r" % (a, v) for (a, v) in self.__dict__.items()]
        return '<Bunch(' + " ".join(attr) + ')>'

    __repr__ = __str__

    def _dump_nested(self, writer, level=0):
        indent = "  " * level
        for k, v in self.items():
            if isinstance(v, Bunch):
                writer("%s%s = {" % (indent, k))
                v._dump_nested(writer, level=level + 1)
                writer("%s}" % indent)
            else:
                writer("%s%s = '%s';" % (indent, k, v))

    def _dump_dotted(self, writer, prefix=()):
        for k, v in self.items():
            if isinstance(v, Bunch):
                v._dump_dotted(writer, prefix=prefix + (k,))
            else:
                writer("%s = '%s';" % ('.'.join(prefix + (k,)), v))

    def dump(self, writer=print, mode=NESTED, name=None):
        """Dump data"""
        if mode == NESTED:
            self._dump_nested(writer, level=0)
        else:
            if name:
                prefix = (name,)
            else:
                prefix = ()
            self._dump_dotted(writer, prefix=prefix)

    def dumps(self, mode=NESTED, name=None):
        """Return dumps"""
        s = BytesIO()
        self.dump(writer=print, mode=mode, name=name)
        return s.getvalue()
