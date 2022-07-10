from socketserver import StreamRequestHandler, TCPServer

SYSLOG_IP = "0.0.0.0"
SYSLOG_TCP_PORT = 514


class TCPServerHandler(StreamRequestHandler):

    def handle(self):
        try:
            # self.request is the TCP socket connected to the client
            self.data = self.rfile.readline()
            print(f"Received: Client IP: {self.client_address[0]}")
            print(f"Received: Data From Client(RAW): {self.data}")
        except Exception as except_me:
            print("Oops! Caught Exception", except_me)


if __name__ == "__main__":

    # Create Server
    server = TCPServer((SYSLOG_IP, SYSLOG_TCP_PORT), TCPServerHandler)

    # SHow that Log Server has Started
    print(f"Starting TCP Log Server @ {SYSLOG_IP}:{SYSLOG_TCP_PORT} ")

    # Activate the server, This will keep running until Ctrl-C
    server.serve_forever()
