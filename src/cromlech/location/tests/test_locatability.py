# -*- coding: utf-8 -*-
"""dolmen.location tests
"""
import pytest
from crom import testing

import crom
import cromlech.location
from cromlech.browser import IPublicationRoot
from cromlech.browser.testing import TestRequest as Request
from zope.interface import directlyProvides
from zope.location import Location


def setup_module(module):
    testing.setup()
    crom.configure(cromlech.location)


def teardown_module(module):
    testing.teardown()


def test_locatability():
    """For a simple scenario : /obj:grandfather/obj:father/obj:me
    """
    request = Request(path='/somepath')
    grandfather = Location()
    father = Location()
    me = Location()

    me.__parent__ = father
    me.__name__ = 'Grok'

    father.__parent__ = grandfather
    father.__name__ = 'Krao'

    grandfather.__name__ = 'Ghran'

    with pytest.raises(LookupError) as e:
        """The Publication root is not defined
        """
        cromlech.location.get_absolute_url(me, request)

    assert str(e.value) == (
        "The path of the application root could not be resolved.")

    # We define a publication root.
    directlyProvides(grandfather, IPublicationRoot)
    assert cromlech.location.get_absolute_url(me, request) == (
        "http://localhost/Krao/Grok")


def test_lineage_chain():

   elder = Location()
   
   old = Location()
   old.__parent__ = elder

   mature = Location()
   mature.__parent__ = old

   young = Location()
   young.__parent__ = mature
   
   baby = Location()
   baby.__parent__ = young

   from types import GeneratorType
   iterable = cromlech.location.lineage(baby)
   assert type(iterable) == GeneratorType

   chain = list(iterable)
   assert chain == [baby, young, mature, old, elder]
   assert chain == cromlech.location.lineage_chain(baby)


def test_lineage_infinite_loop():

    paul = Location()
    isabel = Location()
    juliana = Location()

    # Love triangle !
    juliana.__parent__ = paul
    paul.__parent__ = isabel
    isabel.__parent__ = paul
    
    with pytest.raises(LookupError) as e:
        cromlech.location.lineage_chain(juliana)
    assert str(e.value) == (
        'The lineage chain could not be completed. ' +
        'An infinite loop as been detected')
