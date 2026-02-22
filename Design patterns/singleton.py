from threading import Thread, Lock

class Singleton(type):
    __instances = {}
    __lock = Lock()
    
    def __call__(cls, *args, **kwargs):
        with cls.__lock:
            if cls not in cls.__instances:
                cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]

class NetworkManager(metaclass = Singleton):
    ...
    
def create_singleton():
    network_manager = NetworkManager()
    print(network_manager)
    return network_manager


t1 = Thread(target=create_singleton)
t2 = Thread(target=create_singleton)
t1.start()
t2.start()





