import grpc
import stock_trading_pb2
import stock_trading_pb2_grpc
import random
import time

def run_update():
    channel = grpc.insecure_channel('localhost:50051')
    stub = stock_trading_pb2_grpc.StockTradingStub(channel)
    stock_names = ["GameStart", "FishCo", "BoarCo", "MenhirCo"]
    while True:
        stock_name = random.choice(stock_names)
        new_price = round(random.uniform(10.0, 30.0), 2)
        response = stub.Update(stock_trading_pb2.UpdateRequest(stock_name=stock_name, price=new_price))
        print(f"Update Response: Status = {response.status}")
        time.sleep(random.randint(1, 5))

if __name__ == '__main__':
    run_update()
