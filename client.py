import socket
import threading
import json
import sys

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except Exception as e:
            print(f"Error: {e}")
            break

def send_client():
    host = '127.0.0.1'  
    port = 9007

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    username = input("Enter your username: ")
    client.send(username.encode('utf-8'))

    welcome_message = client.recv(1024).decode('utf-8')
    print(welcome_message)

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    try:
        while True:
            message = input(f" ")
            if message.lower() == 'exit':
                # Envoyer un message spécial pour indiquer la déconnexion
                client.send(json.dumps({'content': 'exit'}).encode('utf-8'))
                break

            # Créer un message JSON avec le contenu et l'expéditeur
            message_data = {
                'content': message,
                'sender': username
            }

            # Convertir le message en format JSON
            message_json = json.dumps(message_data)

            # Envoyer le message JSON au serveur
            client.send(message_json.encode('utf-8'))
    except KeyboardInterrupt:
        # Si l'utilisateur interrompt avec Ctrl+C, fermez proprement la connexion
        client.send(json.dumps({'content': 'exit'}).encode('utf-8'))
        sys.exit()

if __name__ == "__main__":
    send_client()
