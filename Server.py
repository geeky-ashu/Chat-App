import socket
import select

HEADER_LENGTH = 10
PORT = 1234
IP = "127.0.0.1"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()

socket_list = [server_socket]
clients = {}

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_header = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False

while True:
    read_sockets, _ , exceptions_sockets = select.select(socket_list, [], socket_list)

    for notified_sockets in read_sockets:
        if notified_sockets == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)

            if user is False:
                continue
            socket_list.append(client_socket)
            clients[client_socket] = user

            print(f"Accepted connection from {client_address[0]} : {client_address[1]} username: {user['data'].decode('utf-8')}")

        else:
            message = receive_message(notified_sockets)

            if message is False:
                print("Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                socket_list[notified_sockets].remove()
                del clients[notified_sockets]
                continue

            user = clients[notified_sockets]
            print("Received message from {user['data'].decode('utf-8')} : {message['data'].decode('utf-8')}")

            # Share this received message with everyone
            for client_socket in clients:
                if client_socket != notified_sockets:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    # Remove the sockets with exceptions from sockets list and clients socket
    for notified_sockets in exceptions_sockets:
        socket_list.remove(notified_sockets)
        del clients[notified_sockets]



