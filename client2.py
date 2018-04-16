import socket
host = '127.0.0.1'
port = 9005
message = ""

while message != 'q':
    message = input()
    # Отправка изменоного поля на сервер
    mySocket = socket.socket()
    mySocket.connect((host, port))
    mySocket.send(message.encode())
    data = mySocket.recv(1024).decode()
    print('Received from server: ')
    print(data)