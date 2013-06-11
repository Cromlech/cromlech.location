# -*- coding: utf-8 -*-

from zope.location import ILocation


def lineage(item):
    while item is not None:
        yield item
        try:
            item = item.__parent__
        except AttributeError:
            # We try an adaptation. If it fails, this time, we let it
            # bubble up.
            item = ILocation(item)
            item = item.__parent__


def lineage_chain(item):
    chain = []
    for node in lineage(item):
        if node in chain:
            raise LookupError(
                'The lineage chain could not be completed. ' +
                'An infinite loop as been detected')
        chain.append(node)
    return chain
