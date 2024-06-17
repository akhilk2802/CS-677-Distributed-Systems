import socket
import threading
from thread_pool import ThreadPool

# In-memory stock catalog
stock_catalog = {
    "GameStart": 15.99,
    "FishCo": 9.99
}

def handle_client_connection(client_socket):
    request = client_socket.recv(1024).decode()
    parts = request.split()
    if len(parts) != 2 or parts[0] != "Lookup":
        client_socket.send(b"Invalid request")
        client_socket.close()
        return

    stock_name = parts[1]
    if stock_name not in stock_catalog:
        client_socket.send(b"-1")
    else:
        price = stock_catalog[stock_name]
        client_socket.send(str(price).encode())

    client_socket.close()

def start_server(host, port, num_threads):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    thread_pool = ThreadPool(num_threads)

    while True:
        client_socket, addr = server_socket.accept()
        thread_pool.add_task(handle_client_connection, client_socket)

if __name__ == "__main__":
    start_server('0.0.0.0', 8888, 4)
