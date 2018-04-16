import socket
import sys
import traceback
from threading import Thread

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


def start_server(port1 = 8888, back_port1 = 0):
    host = "127.0.0.1"
    port = port1         # arbitrary non-privileged port
    back_port = back_port1
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state, without waiting for its natural timeout to expire
    print("Socket created")

    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    soc.listen(5)       # queue up to 5 requests
    print("Socket now listening")

    # infinite loop- do not reset for every requests
    while True:
        connection = 0
        ip = 0
        port = 0
        try:
            connection, address = soc.accept()
            ip, port = str(address[0]), str(address[1])
            print("Connected with " + ip + ":" + port)
        except:
            print("client broken")
        try:
            Thread(target=client_thread, args=(connection, ip, port, back_port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()

    soc.close()


def client_thread(connection, ip, port, back_port, max_buffer_size = 5120):
    is_active = True

    while is_active:
        client_input = receive_input(connection, max_buffer_size)
        try:
            if "--QUIT--" in client_input:
                print("Client is requesting to quit")
                connection.close()
                print("Connection " + ip + ":" + port + " closed")
                is_active = False
            else:
                print("Processed result: {}".format(client_input))
                print("back port = " + str(back_port))
                # connection.send(bytes("TakBlet", 'UTF-8'))
                connection.sendall(bytes("TakBlet2", 'UTF-8'))
                if back_port != 0:
                    send_to_port(back_port, client_input)
                # connection.sendall("-".encode("utf8"))
        except:
            print("broken pipe")
            is_active = False


def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)

    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))

    decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
    result = process_input(decoded_input)

    return result


def process_input(input_str):
    print("Processing the input received from client")

    return "" + str(input_str).upper()


if __name__ == "__main__":
    print("Input port:")
    port = input()
    print("Input backport:")
    backport = input()
    start_server(int(port), int(backport))