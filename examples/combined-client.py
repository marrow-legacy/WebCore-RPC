import logging

from pyamf.remoting.client import RemotingService
from xmlrpclib import ServerProxy, Error

path = 'http://127.0.0.1:8080/gateway'
gw = RemotingService(path)#, logger=logging) #, debug=True)
service = gw.getService('test')

print service.hello('AMF')
print service.hello()


server = ServerProxy("http://127.0.0.1:8080/rpc")

print server.test.hello()
print server.test.hello('XML-RPC')
