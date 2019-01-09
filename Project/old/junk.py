#client example
import socket
import re

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



# hackIP = 'localhost'
# timeout = 10
# port = 80

# #client_socket.shutdown(2)
# client_socket.close()

# hack_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Communicator:
    
    def __init__(self, host, port, other=None):
        self.host = host
        self.other = other
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


    def sendHTMLPageRequest(self, pageAddress):
        request = "GET " + page + " HTTP/1.1\r\n" \
        + "Host: localhost\r\n" \
        + "Accept: text/html,text/php,text/css,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n" \
        + "Connection: keep-alive\r\n" \
        + "Cookie: security_level=0; PHPSESSID=0\r\n"
        if self.other:
            request = request + self.other
        request = request + "\r\n"
        self.sock.send(request)
        return self.sock.recv(8000)

    def postHTMLForm(self, form, fieldDict):



    def close(self):
        self.sock.close()



def find_input_fields(page):
    #p1 = re.compile('.*(?<!http).*')
    #p2 = re.compile('http://' + domain + '*')
    print(page)
    #matches = fieldPattern.search(page)
    matches = re.findall(r'label for=.*">', page)
    fields = [m[11:-2] for m in matches]

    return fields


def login(host, page, username, password):


c = Communicator("127.0.0.1", 80)
page = c.generateHttpPageRequest("/bWAPP/login.php")
c.other = "Referer: http://localhost/bWAPP/portal.php\r\n" \
        + "Upgrade-Insecure-Requests: 0\r\n" \
        + "Cache-Control: max-age=0\r\n"
 #
#page = c.sendHTMLPageRequest("bWAPP/sqli_1.php")
fields = find_input_fields(page)
print(fields)


# request = "GET /bWAPP/login.php HTTP/1.1\r\n" \
#         + "Host: localhost\r\n" \
#         + "Accept: text/html,text/php,text/css,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n" \
#         + "Connection: keep-alive\r\n" \
#         + "Cookie: security_level=0; PHPSESSID=0\r\n\r\n"

# hack_socket.connect(('localhost', port))
# hack_socket.send(request)
# data = hack_socket.recv(2048)
# print(data)

# def something():
#     while 1:
#         data = client_socket.recv(512)
#         if ( data == 'q' or data == 'Q'):
#             client_socket.close()
#             break;
#         else:
#             print "RECIEVED:" , data
#             data = raw_input ( "SEND( TYPE q or Q to Quit):" )
#             if (data != 'Q' and data != 'q'):
#                 client_socket.send(data)
#             else:
#                 client_socket.send(data)
#                 client_socket.close()
#                 break;