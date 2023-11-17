import socket
import threading

def handle_client(client_socket, addr):
    print(f"New connection from {addr}")

    while True:
        data_received = client_socket.recv(128).decode("UTF-8")
        if not data_received:
            print(f"{addr} disconnected")
            break
        print(f"Received from {addr}: {data_received}")

    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 9002))
    server.listen()

    print("Server is listening for connections...")

    while True:
        client_socket, addr = server.accept()
        print(f"New connection from {addr}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    main()