# -*- coding: utf-8 -*-

import urllib
from zope.location import ILocation
from zope.interface import Interface, implementer
from cromlech.browser import IPublicationRoot, IRequest, IURL

_safe = '@+'  # Characters that we don't want to have quoted


@implementer(IURL)
def resolve_url(context, request):
    # first try to get the __parent__ of the object, no matter whether
    # it provides ILocation or not. If this fails, look up an ILocation
    # adapter. This will always work, as a general ILocation adapter
    # is registered for interface in zope.location (a LocationProxy)
    # This proxy will return a parent of None, causing this to fail
    # More specific ILocation adapters can be provided however.
    try:
        container = context.__parent__
    except AttributeError:
        # we need to assign to context here so we can get
        # __name__ from it below
        context = ILocation(context)
        container = context.__parent__

    if container is None:
        if IPublicationRoot.providedBy(context):
            return request.application_url
        raise LookupError(
            'The path of the application root could not be resolved.')

    url = IURL(container, request)

    name = getattr(context, '__name__', None)
    if name is None:
        raise KeyError(context, '__name__')

    if name:
        url += '/' + urllib.quote(name.encode('utf-8'), _safe)

    return url


try:
    import crom

    @crom.adapter
    @crom.sources(Interface, IRequest)
    @crom.target(IURL)
    def get_absolute_url(context, request):
        return resolve_url(context, request)
except ImportError:
    pass
