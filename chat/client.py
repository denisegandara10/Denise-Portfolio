import sys
import socket

MAX_LINE = 256

# Global Variables
socket_id = None
port = None
# END Global Variables


def connectToSocket(host):
    global socket_id, port
    # active open
    socket_id = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_id.connect((host, port))
    return socket_id


def printUsage():
    print("usage: client <server-hostname> <portnum>")
    print("  Ex: client localhost 12345")
    print("    Connect to a server running on the localhost at port 12345")


def main():
    global socket_id, port
    # Read in Command Line Args
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = int(sys.argv[2])
    else:
        printUsage()
        sys.exit(1)

    connectToSocket(host)

    message1 = "Hello, welcome to my chat!\n"
    print(message1, end="")
    message2 = "Please enter your username:"
    print(message2, end="")

    # Get Username from User and send it to server
    username = input()
    socket_id.sendall(username.encode())

    # main loop: get and send lines of text
    while True:
        message = input()
        socket_id.sendall(message.encode())
        if message == "logout":
            break
        response = bytearray(MAX_LINE)
        buf_len = socket_id.recv_into(response)
        print(response[:buf_len].decode(), end="")

    socket_id.close()


if __name__ == '__main__':
    main()
