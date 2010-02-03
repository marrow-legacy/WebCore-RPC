# encoding: utf-8

"""A basic AMF Dialect class for YAPWF."""

import inspect

from web.core import Dialect, response
from web.extras.rpc.common import route
from webob.exc import *


__all__ = ['AMFController']
log = __import__('logging').getLogger(__name__)


try:
    import pyamf
    import pyamf.remoting.gateway

except ImportError:
    log.error("If you want to use the AMFController class, you must install PyAMF.")
    raise



class AMFController(Dialect):
    __context__ = pyamf.AMF0
    __gateway__ = dict()
    
    def __init__(self):
        self._gateway = pyamf.remoting.gateway.BaseGateway(logger=log, *self.__gateway__)
        self._context = pyamf.get_context(self.__context__)
    
    def __call__(self, request):
        pyamf_request = pyamf.remoting.decode(request.body, self._context)
        pyamf_response = pyamf.remoting.Envelope(pyamf_request.amfVersion, pyamf_request.clientType)
        
        for name, message in pyamf_request:
            # Dynamically build mapping.  This introduces a performance hit on the first request of each method.
            if message.target not in self._gateway.services:
                fn, parent = route(self, message.target, AMFController)
                self._gateway.addService(fn, message.target)
            
            pyamf_response[name] = self._gateway.getProcessor(message)(message)
        
        response.headers['Content-Type'] = pyamf.remoting.CONTENT_TYPE
        return pyamf.remoting.encode(pyamf_response, self._context).getvalue()
