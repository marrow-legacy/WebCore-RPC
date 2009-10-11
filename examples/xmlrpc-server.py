#!/usr/bin/env python2.5
# encoding: utf-8

"""A basic hello world application.

This can be simplified down to 5 lines in total; two import lines, two
controller lines, and one line to serve it.
"""

from web.extras.rpc.xml import XMLRPCController



class TestService(XMLRPCController):
    def hello(self, name="world"):
        return "Hello, %(name)s!" % dict(name=name)


class RootController(XMLRPCController):
    test = TestService()



if __name__ == '__main__':
    import logging
    from paste import httpserver
    from web.core import Application
    
    logging.basicConfig(level=logging.INFO)
    
    app = Application.factory(root=RootController, debug=False, **{
            'web.sessions': False,
            'web.widgets': False,
            'web.beaker': False,
            'web.profile': False,
            'web.static': False,
            'web.compress': False
        })
    
    httpserver.serve(app, host='127.0.0.1', port='8080')
