""" All Important Libs & Packages that are required """
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import ssl
import time
import os
import sys
from urllib.parse import urlparse
import traceback

# Threaded HTTP Server
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass


""" Custom Request Handler """
class CustomHTTPRequestHandler(BaseHTTPRequestHandler):

    # Support HTTP/1.1
    protocol_version = "HTTP/1.1"

    ''' Testing Purpose Func To Enable Pause Between Request Received & Sent back to Client'''

    def do_sleep(self, sleep_time=0):
        print(f"Sleeping for {sleep_time} Seconds..")
        time.sleep(sleep_time)

    def get_url_parms(self):
        url_path = urlparse(self.path)
        try:
            url_params = dict([one_url_param.split('=')
                               for one_url_param in url_path[4].split('&')])
        except Exception as except_me:
            print(except_me)
            traceback.print_exc()  # Print StackTrace
            url_params = {}

        return url_params

    def check_to_sleep(self):
        if "sleep" in self.path:
            url_params = self.get_url_parms()
            sleep_time = 6  # default 6
            if url_params.get('sleep', None):
                try:
                    sleep_time = int(url_params['sleep'])
                except Exception as except_me:
                    print(except_me)
                    traceback.print_exc()  # Print StackTrace
                    print('sleep_time is not Int...')
            else:
                print("No 'sleep' param Found Using Default Value...")

            self.do_sleep(sleep_time=sleep_time)

    def set_and_send_response_headers(self, content_length):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.send_header('Content-Length', content_length)
        self.end_headers()  # Send Headers to Client

    def create_response_body(self, request_body=None):
        content_to_send = f"Received Request By Server: [{self.server.server_address}]\n"
        content_to_send += f"Request Line: \n{self.requestline}\n\n"
        content_to_send += f"Headers: \n{self.headers}\n"
        if request_body:
            content_to_send += f"Request Body: \n{request_body}\n"

        print(content_to_send)
        content_to_send = content_to_send.encode('utf-8')
        return content_to_send

    def send_response_body(self, content_to_send):
        try:
            self.wfile.write(content_to_send)
        except Exception as except_me:
            print(except_me)
            traceback.print_exc()  # Print StackTrace
            print("Problem!!!!! Not Able to Send the Response Body [Check Error]")

    def do_GET(self):
        self.check_to_sleep()  # Check If We have to Sleep
        content_to_send = self.create_response_body()
        self.set_and_send_response_headers(len(content_to_send)) # Send Across the Response Headers Back to Client
        self.send_response_body(content_to_send) # Send Across the Response Body Back to Client

    def do_POST(self):

        # Gets Post Data Content-Length
        content_recieved = ''

        if self.headers['Content-Length']:
            # Gets Post Data Using Content-Length
            content_length = int(self.headers['Content-Length'])
            content_recieved = self.rfile.read(content_length)
            content_recieved = content_recieved.decode("utf-8")  # Convert Bytes to String

        elif "chunked" in self.headers.get("Transfer-Encoding", ""):

            # Refer Detailed Analysis of Chunk Reading from Top
            while True:
                # Reading the Chunk Length Number From Chunked Data
                # Will Read with \n & strip will remove \n
                size_line = self.rfile.readline().strip()
                # We will use Hexadecimal Format Conversion
                chunk_length = int(size_line, 16)

                # If Chunk_size is 0 means all data has been read we can break off the Infinite Loop
                if chunk_length == 0:
                    break
                else:
                    # Read the Data till the Size
                    chunk_data = self.rfile.read(chunk_length)
                    # Convert Bytes to String, Add it to a String After Converting to String
                    content_recieved += chunk_data.decode("utf-8")
                    # print(f"This Chunk with Length: {chunk_length} Holds Data: ", content_recieved)

                # After the Chunk Data is Received, Since a \n is at End we will use readline() to read it (Not Need to Store or Use it This is just to skip it)
                self.rfile.readline()

        else:
            content_recieved = "In Request Header Neither Content-Length NOR Transfer-Encoding: Chunked Received"

        self.check_to_sleep()  # Check If We have to Sleep

        content_to_send = self.create_response_body(
            request_body=content_recieved)

        # Send Across the Response Headers Back to Client
        self.set_and_send_response_headers(len(content_to_send))

        # Send Across the Response Body Back to Client
        self.send_response_body(content_to_send)

    # Do Same Function For PUT, PATCH Same as POST
    do_PUT = do_POST
    do_PATCH = do_POST


def get_cert_and_key_file():
    cert_dir = '../certs/'
    cert_file = None
    key_file = None

    try:
        file_list = os.listdir(cert_dir)
    except Exception as exception:
        print(exception)
        print("Certs Dir Not Present, HTTPS Server will not Run")
        return cert_file, key_file

    for one_file in file_list:
        if one_file.endswith('Server_Cert.pem'):
            cert_file = cert_dir + one_file
            if key_file:
                break
        if one_file.endswith('Server_Key.pem'):
            key_file = cert_dir + one_file
            if cert_file:
                break
    if cert_file is None or key_file is None:
        print(
            "Files are Not Present Please Run: [bash generate_certs.sh] Files [Cert_File: " + str(cert_file) + "], [Key_File: " + str(key_file) + "]")
        cert_file = None  # So Incomplete Cert do not Create Problem
        key_file = None  # So Incomplete Cert do not Create Problem
        return cert_file, key_file
    return cert_file, key_file


if __name__ == '__main__':

    # Standard Port Set
    HTTP_PORT = 80
    HTTPS_PORT = 443

    print("All Arguments: ", sys.argv)

    # Code Does Not handles Proper CLI Options UX (Will be Later Handled)
    if len(sys.argv) > 1:
        HTTP_PORT = int(sys.argv[1])

    if len(sys.argv) > 2:
        HTTPS_PORT = int(sys.argv[2])

    # Certificate Setup: Fetch Certificate from Dir
    cert_file, key_file = get_cert_and_key_file()
    print(f'CertFile:[{cert_file}], KeyFile:[{key_file}]')

    # If Cert File Present Start HTTPS Server
    if cert_file:
        HTTPS_SOCKET = ('0.0.0.0', HTTPS_PORT)
        https_server = ThreadedHTTPServer(
            HTTPS_SOCKET, CustomHTTPRequestHandler)
        https_server.socket = ssl.wrap_socket(
            https_server.socket,  keyfile=key_file, certfile=cert_file, server_side=True)
        print("[+] Starting HTTPS Server on Socket: [ " + str(HTTPS_SOCKET) + " ]")
        https_server.serve_forever()  # Start HTTPS Server

    # HTTP Server
    HTTP_SOCKET = ('0.0.0.0', HTTP_PORT)
    http_server = ThreadedHTTPServer(HTTP_SOCKET, CustomHTTPRequestHandler)
    print("[+] Starting HTTP Server on Socket: [ " + str(HTTP_SOCKET) + " ]")
    http_server.serve_forever()  # Start HTTP Server