from xmlrpclib import ServerProxy, Error

server = ServerProxy("http://127.0.0.1:8080")

print server.test.hello()
print server.test.hello('XML-RPC')
