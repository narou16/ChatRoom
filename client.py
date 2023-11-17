import socket
import threading

def send_message(client_socket):
     name = input("what's your name ?")
     while True:
        msg = input(f"{name}> ")
        client_socket.send(f"{name}>{msg}".encode("UTF-8"))

def receive_messages(client_socket):
    while True:
        data_received = client_socket.recv(128).decode("UTF-8")
        if not data_received:
            print("Server disconnected")
            break
        print(f"Received from server: {data_received}")

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host, port = '127.0.0.1', 9002
    client.connect((host, port))

    send_thread = threading.Thread(target=send_message, args=(client,))
    receive_thread = threading.Thread(target=receive_messages, args=(client,))

    send_thread.start()
    receive_thread.start()

    send_thread.join()
    receive_thread.join()

if __name__ == '__main__':
    num_clients = 2  # Change this to the number of clients you want
    for _ in range(num_clients):
        threading.Thread(target=start_client).start()
