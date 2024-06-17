import socket

def lookup_stock(stock_name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8888))
    request = f"Lookup {stock_name}"
    client_socket.send(request.encode())

    response = client_socket.recv(1024).decode()
    client_socket.close()
    return response

if __name__ == "__main__":
    stocks = ["GameStart", "FishCo", "UnknownStock"]
    for stock in stocks:
        price = lookup_stock(stock)
        print(f"Price of {stock}: {price}")
