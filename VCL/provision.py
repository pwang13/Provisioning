import xmlrpclib
import getpass
import socket

class AuthenticatedTransport(xmlrpclib.SafeTransport): 
 
    def __init__(self, username, password):
        xmlrpclib.SafeTransport.__init__(self)
        self.password = password
        self.username = username

    def send_content(self, connection, request_body):
        # X- headers are user-defined in HTTP
        # These next few are used by VCL
        connection.putheader("X-User", self.username)
        connection.putheader("X-Pass", self.password)
        connection.putheader("X-APIVERSION: 2")
        # That's the end of the VCL-specific headers
 
        xmlrpclib.SafeTransport.send_content(self, connection, request_body)


username = "pwang13"
password = getpass.getpass("Password: ")

auth_transport = AuthenticatedTransport(username, password)
server = xmlrpclib.Server("https://vcl.ncsu.edu/scheduling/index.php?mode=xmlrpccall", transport=auth_transport)

#create ubuntu image 
try:
	res = server.XMLRPCaddRequest(4070, "now", 480)


except xmlrpclib.ProtocolError as e:
    print "URL: {}".format(e.url)
    print "Headers: {}".format(e.headers)
    print "Error code: {}".format(e.errcode)
    print "Error message: {}".format(e.errmsg)
except xmlrpclib.Fault as f:
    print "Fault Code: {}".format(f.faultCode)
    print "Fault: {}".format(f.faultString)
    print "Args: {}".format(f.args)
    print "Message: {}".format(f.message)
else:
	print res