import socket
import threading
import json

clients = {}  # Dictionnaire pour stocker les sockets des clients et leurs noms d'utilisateur

def broadcast(message, sender_socket):
    for client_socket, (username, _) in clients.items():
        try:
            # Envoyer le message JSON à tous les clients sauf à l'expéditeur
            if client_socket != sender_socket:
                client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error broadcasting message to {username}: {e}")

def handle_client(client_socket, username):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                print(f"Client {username} disconnected.")
                break

            # Convertir le message JSON en un dictionnaire
            message_data = json.loads(message)

            # Extraire les informations du message
            content = message_data.get('content', '')

            if content.lower() == 'exit':
                print(f"Client {username} disconnected.")
                client_socket.close()
                break

            # Diffuser le message à tous les clients
            broadcast(f"{username}: {content}", client_socket)
        except Exception as e:
            print(f"Error: {e}")
            break

def start_server():
    host = '127.0.0.1'
    port = 9007

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"Server listening on {host}:{port}")

    while True:
        client, addr = server.accept()
        print(f"Accepted connection from {addr}")

        username = client.recv(1024).decode('utf-8')
        print(f"{addr} set username to {username}")

        client.send(f"Welcome to the chatroom, {username}!".encode('utf-8'))

        # Stocker le socket client et le nom d'utilisateur dans le dictionnaire
        clients[client] = (username, addr)

        # Démarrer un thread distinct pour gérer chaque client
        client_handler = threading.Thread(target=handle_client, args=(client, username))
        client_handler.start()

if __name__ == "__main__":
    start_server()
    main()
