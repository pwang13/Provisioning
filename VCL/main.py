import xmlrpclib
import getpass
import socket


# We're connecting over SSL so subclass SafeTransport
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
 
try:
    f = open("inventory","w")
    f.write("[myServers]\n")
    res = server.XMLRPCgetRequestIds ()
    # # print res
    for line in res["requests"]:
        requestid = line["requestid"]
        response = server.XMLRPCgetRequestConnectData (requestid, "172.16.22.198")
        if (response["status"] != "notready"):
            f.write(response["serverIP"] + " ansible_ssh_private_key_file=~/.ssh/id_rsa" + " ansible_ssh_user=pwang13")
    f.close


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
