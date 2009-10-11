import logging

from pyamf.remoting.client import RemotingService

	
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s'
)


path = 'http://127.0.0.1:8080/'
gw = RemotingService(path, logger=logging) #, debug=True)
service = gw.getService('test')

print service.hello('AMF')
print service.hello()
