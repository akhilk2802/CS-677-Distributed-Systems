from concurrent import futures
import grpc
import stock_trading_pb2
import stock_trading_pb2_grpc
import threading

# In-memory stock catalog
stock_catalog = {
    "GameStart": {"price": 15.99, "volume": 0, "max_volume": 1000},
    "FishCo": {"price": 9.99, "volume": 0, "max_volume": 1000},
    "BoarCo": {"price": 20.00, "volume": 0, "max_volume": 1000},
    "MenhirCo": {"price": 25.00, "volume": 0, "max_volume": 1000}
}

catalog_lock = threading.Lock()

class StockTradingServicer(stock_trading_pb2_grpc.StockTradingServicer):
    def Lookup(self, request, context):
        with catalog_lock:
            if request.stock_name in stock_catalog:
                stock = stock_catalog[request.stock_name]
                return stock_trading_pb2.LookupResponse(price=stock["price"], volume=stock["volume"])
            else:
                return stock_trading_pb2.LookupResponse(price=-1, volume=0)

    def Trade(self, request, context):
        with catalog_lock:
            if request.stock_name not in stock_catalog:
                return stock_trading_pb2.TradeResponse(status=-1)
            
            stock = stock_catalog[request.stock_name]
            if stock["volume"] >= stock["max_volume"]:
                return stock_trading_pb2.TradeResponse(status=0)  # trading suspended due to volume

            if request.type == "buy":
                stock["volume"] += request.quantity
            elif request.type == "sell":
                stock["volume"] -= request.quantity
            return stock_trading_pb2.TradeResponse(status=1)

    def Update(self, request, context):
        with catalog_lock:
            if request.stock_name not in stock_catalog:
                return stock_trading_pb2.UpdateResponse(status=-1)
            if request.price < 0:
                return stock_trading_pb2.UpdateResponse(status=-2)

            stock_catalog[request.stock_name]["price"] = request.price
            return stock_trading_pb2.UpdateResponse(status=1)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    stock_trading_pb2_grpc.add_StockTradingServicer_to_server(StockTradingServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
