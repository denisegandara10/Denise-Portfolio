import socket
import sys

MAX_PENDING = 5
MAX_LINE = 256

# Global Variables
passive_open_socket = None
port = None
# END Global Variables


def performPassiveOpen():
    global passive_open_socket, port
    # setup passive open
    passive_open_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    passive_open_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    passive_open_socket.bind(('127.0.0.1', port))
    passive_open_socket.listen(MAX_PENDING)


def printUsage():
    print("Usage: server <portnum>")
    print("  Ex: server 12345")
    print("    Start the server connected to port 12345")


def main():
    global passive_open_socket, port
    buf = bytearray(MAX_LINE)
    username = bytearray(MAX_LINE)
    # Read in port number
    if len(sys.argv) == 2:
        port = int(sys.argv[1])
    else:
        printUsage()
        sys.exit(1)

    performPassiveOpen()

    while True:
        new_s, addr = passive_open_socket.accept()

        buf_len = new_s.recv_into(buf)
        username = buf[:buf_len].decode()
        print(username, "has connected to chat")

        while True:
            buf_len = new_s.recv_into(buf)
            if buf_len <= 0:
                break
            print(username + ": " + buf[:buf_len].decode())
            if buf[:buf_len].decode() == "logout\n":
                print(username, "has disconnected from the chat")
                break

            message = input("Message to client: ")
            new_s.sendall(message.encode())

        new_s.close()


if __name__ == '__main__':
    main()
