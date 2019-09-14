# -*- coding: utf-8 -*-
"""module represents common pattern solutions
that can be used in project
"""


def singleton(cls):
    """Return one instance of provided object
    in case of object invalidation -- recreate instance
    """
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance
