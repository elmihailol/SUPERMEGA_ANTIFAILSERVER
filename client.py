import socket
import sys


def send_to_port(port1, msg):
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = port1

    try:
        soc.connect((host, port))
    except:
        print("Connection error")
        sys.exit()

    print("Enter 'quit' to exit")
    message = msg
    soc.sendall(message.encode("utf8"))
    soc.close()
    # soc.send(b'--quit--')

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8889

    try:
        soc.connect((host, port))
    except:
        print("Connection error")
        sys.exit()

    print("Enter 'quit' to exit")
    message = input(" -> ")

    while message != 'quit':
        soc.sendall(message.encode("utf8"))
        if soc.recv(5120).decode("utf8") == "-":
            pass        # null operation

        message = input(" -> ")

    soc.send(b'--quit--')

if __name__ == "__main__":
    #main()
    port = 9000
    while True:
        m = input()
        flag = 0
        while flag == 0:
            try:
                send_to_port(port, m)
                flag = 1
            except:
                port+=1
                continue

