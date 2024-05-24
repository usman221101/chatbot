import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 5555

groups = {}


def handle_client(client_socket):
    user_name = None

    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        parts = data.split(',')
        command = parts[0]

        if command == 'create_group':
            group_name = parts[1]
            groups[group_name] = []
            user_name = parts[2]
            groups[group_name].append((user_name, client_socket))  # Store user_name and client_socket as a tuple
            client_socket.send(f'Group "{group_name}" created. You are now in group "{group_name}".'.encode('utf-8'))

        elif command == 'join_group':
            group_name = parts[1]
            if group_name in groups:
                user_name = parts[2]
                groups[group_name].append((user_name, client_socket))
                client_socket.send(f'Joined group "{group_name}". You are now in group "{group_name}".'.encode('utf-8'))
            else:
                client_socket.send(f'Group "{group_name}" does not exist.'.encode('utf-8'))

        elif command == 'send_message':
            group_name = parts[1]
            message = parts[2]
            if group_name in groups:
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                message_data = f'{timestamp} - {user_name}: {message}'
                for member_name, member_socket in groups[group_name]:
                    if member_socket != client_socket and not member_socket._closed:
                        member_socket.send(message_data.encode('utf-8'))  # Send message to all members in the group
            else:
                client_socket.send(f'Group "{group_name}" does not exist.'.encode('utf-8'))

    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f'Server listening on {HOST}:{PORT}')

    while True:
        client_socket, client_address = server.accept()
        print(f'Accepted connection from {client_address}')

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


def main():
    server_thread = threading.Thread(target=start_server)
    server_thread.start()


if __name__ == "__main__":
    main()
