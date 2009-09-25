# encoding: utf-8

"""A basic XML-RPC controller class for YAPWF."""

import inspect, xmlrpclib

from web.core import Dialect, response
from webob.exc import *


__all__ = ['XMLRPCController']
log = __import__('logging').getLogger(__name__)

MAPPING = [
        (str, 'string'),
        (basestring, 'string'),
        (unicode, 'string'),
        (list, 'array'),
        (bool, 'boolean'),
        (int, 'int'),
        (float, 'double'),
        (dict, 'struct'),
        (xmlrpclib.DateTime, 'dateTime.iso8601'),
        (xmlrpclib.Binary, 'base64')
    ]

FORWARD_MAPPING = dict(MAPPING)
REVERSE_MAPPING = dict([(j, i) for i, j in MAPPING])



class XMLRPCController(Dialect):
    __allow_none__ = False
    __max_body_length__ = 4194304
    
    def _fault(self, code, message, *args):
        """Return a formatted XMLRPC Fault response."""
        
        fault = xmlrpclib.Fault(code, message % args)
        return xmlrpclib.dumps(fault, methodresponse=True)
    
    def _route(self, method):
        last = None
        part = self
        parts = method.split('.')
        parts.reverse()
        
        while True:
            last = part
            part = parts[-1]
            
            log.debug("Looking for %r attribute of %r.", part, last)
            
            if part.startswith('_'):
                log.error("An attempt was made to route a private object: %s", method)
                raise HTTPNotImplemented('An attempt was made to call a method that can not be routed.')
            
            part = getattr(last, part, None)
            
            if not isinstance(part, XMLRPCController) and isinstance(part, Dialect):
                log.error("Context switching to another dilect from XML-RPC is not allowed.")
                raise HTTPNotImplemented('An attempt was made to call a method that can not be routed.')
            
            if isinstance(part, XMLRPCController):
                log.debug("Continuing descent through controller structure.")
                parts.pop()
                continue
            
            if callable(part) and parts[1:]:
                log.error("Callable method found before reaching the end of the call tree.")
                raise HTTPNotImplemented('An attempt was made to call a method that can not be routed.')
            
            if callable(part):
                parts.pop()
                return part
            
            log.error("An attmpt as made to call an unroutable method: %s", method)
            raise HTTPNotImplemented('An attempt was made to call a method that can not be routed.')
    
    def __call__(self, request):
        """Parse an XML-RPC body and dispatch."""
        
        length = int(request.headers.get('Content-Length', 0))
        
        if not length:
            log.debug("No content length specified, returning 411 HTTPLengthRequired error.")
            raise HTTPLengthRequired()
        
        if not length or length > self.__max_body_length__:
            log.debug("Content length larger than allowed maximum of %d bytes, returning 413 HTTPRequestEntityTooLarge error.", self.__max_body_length__)
            raise HTTPRequestEntityTooLarge("XML body too large.")
        
        args, method = xmlrpclib.loads(request.body, True)
        
        log.debug("XML-RPC Call: %s%r", method, args)
        
        func = self._route(method)
        
        log.debug("Found methd: %r", func)
        
        result = func(*args)
        
        log.debug("Got result: %r", result)
        
        response.content_type = 'text/xml'
        
        return xmlrpclib.dumps((result, ), methodresponse=True, allow_none=self.__allow_none__)
