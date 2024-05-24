import socket

HOST = '127.0.0.1'
PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def create_group():
    group_name = input("Enter group name: ")
    username = input("Enter your username: ")
    client_socket.send(f'create_group,{group_name},{username}'.encode('utf-8'))
    print(client_socket.recv(1024).decode('utf-8'))

def join_group():
    group_name = input("Enter group name to join: ")
    username = input("Enter your username: ")
    client_socket.send(f'join_group,{group_name},{username}'.encode('utf-8'))
    print(client_socket.recv(1024).decode('utf-8'))

def send_message():
    group_name = input("Enter group name to send message: ")
    message = input("Enter message: ")
    client_socket.send(f'send_message,{group_name},{message}'.encode('utf-8'))

def get_recent_messages():
    group_name = input("Enter group name to get recent messages: ")
    client_socket.send(f'get_recent_messages,{group_name}'.encode('utf-8'))
    print(client_socket.recv(1024).decode('utf-8'))

def exit_client():
    client_socket.send('exit'.encode('utf-8'))
    client_socket.close()
    print("Exiting...")
    exit()

while True:
    print("1. Create Group")
    print("2. Join Group")
    print("3. Send Message")
    print("4. Get Recent Messages")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        create_group()
    elif choice == '2':
        join_group()
    elif choice == '3':
        send_message()
    elif choice == '4':
        get_recent_messages()
    elif choice == '5':
        exit_client()
    else:
        print("Invalid choice. Please enter a valid option.")
