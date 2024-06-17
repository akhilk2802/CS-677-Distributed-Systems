import grpc
import stock_trading_pb2
import stock_trading_pb2_grpc
import random
import time

def run_lookup():
    channel = grpc.insecure_channel('localhost:50051')
    stub = stock_trading_pb2_grpc.StockTradingStub(channel)
    for _ in range(10):
        response = stub.Lookup(stock_trading_pb2.LookupRequest(stock_name="GameStart"))
        print(f"Lookup Response: Price = {response.price}, Volume = {response.volume}")
        time.sleep(1)

def run_trade():
    channel = grpc.insecure_channel('localhost:50051')
    stub = stock_trading_pb2_grpc.StockTradingStub(channel)
    for _ in range(10):
        trade_type = "buy" if random.choice([True, False]) else "sell"
        response = stub.Trade(stock_trading_pb2.TradeRequest(stock_name="GameStart", quantity=10, type=trade_type))
        print(f"Trade Response: Status = {response.status}")
        time.sleep(1)

if __name__ == '__main__':
    run_lookup()
    run_trade()
