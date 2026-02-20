from enum import Enum

class RequestType(Enum):
    EXTERNAL = 'EXTERNAL'
    INTERNAL = 'INTERNAL'

class Request:
    def __init__(self, origin, target, type_request, direction):
        self.target = target
        self.type_request = type_request
        self.origin = origin
        self.direction = direction
