"""
Low-Level Design: Elevator System

This module implements a console-based elevator system with proper OOP design.

Entities:
    - Elevator: Elevator for the elevator system
    - Direction: Enumeration of possible elevator directions
    - Request: Request for the elevator
"""

from enum import Enum
from heapq import heappop, heappush
import logging
import threading
import time

from request import Request, RequestType

logger = logging.getLogger("elevator")


class Direction(Enum):
    """Enumeration of possible elevator directions."""

    UP = "UP"
    DOWN = "DOWN"
    IDLE = "IDLE"


class Elevator:
    """Elevator for the elevator system."""

    def __init__(self, elevator_id, current_floor):
        self.elevator_id = elevator_id
        self.direction = Direction.IDLE
        self.current_floor = current_floor
        self.up_stops = []
        self.down_stops = []
        self._lock = threading.Lock()
        self._work_available = threading.Condition(self._lock)

    def send_up_request(self, up_request):
        """Send an up request to the elevator. Thread-safe; wakes the elevator if it was waiting."""
        with self._work_available:
            if up_request.type_request == RequestType.EXTERNAL:
                heappush(self.up_stops, (up_request.origin, up_request.origin))
            heappush(self.up_stops, (up_request.target, up_request.origin))
            logger.info(
                "[%s] UP request added: origin=%s target=%s (up_stops=%s)",
                self.elevator_id, up_request.origin, up_request.target, len(self.up_stops),
            )
            self._work_available.notify()

    def send_down_request(self, down_request):
        """Send a down request to the elevator. Thread-safe; wakes the elevator if it was waiting."""
        with self._work_available:
            if down_request.type_request == RequestType.EXTERNAL:
                heappush(self.down_stops, (-down_request.origin, down_request.origin))
            heappush(self.down_stops, (-down_request.target, down_request.origin))
            logger.info(
                "[%s] DOWN request added: origin=%s target=%s (down_stops=%s)",
                self.elevator_id, down_request.origin, down_request.target, len(self.down_stops),
            )
            self._work_available.notify()

    def run(self):
        """Run the elevator. Blocks when idle; wakes when a request is added."""
        logger.info("[%s] thread started, floor=%s", self.elevator_id, self.current_floor)
        while True:
            with self._work_available:
                while not (self.up_stops or self.down_stops):
                    logger.debug("[%s] idle, waiting for request", self.elevator_id)
                    self._work_available.wait()
                logger.info("[%s] woke up, processing requests (up=%s down=%s)", self.elevator_id, len(self.up_stops), len(self.down_stops))
                time.sleep(2)
                self.process_requests()

    def process_requests(self):
        """Process the requests for the elevator."""
        if self.direction in [Direction.UP, Direction.IDLE]:
            self.process_up_requests()
            self.process_down_requests()
        else:
            self.process_down_requests()
            self.process_up_requests()

    def process_up_requests(self):
        """Process the up requests for the elevator."""
        while self.up_stops:
            target, origin = heappop(self.up_stops)

            self.current_floor = target

            if target == origin:
                logger.info("[%s] floor %s: pick up", self.elevator_id, target)
            else:
                logger.info("[%s] floor %s: let people out", self.elevator_id, target)

        if self.down_stops:
            self.direction = Direction.DOWN
        else:
            self.direction = Direction.IDLE

    def process_down_requests(self):
        """Process the down requests for the elevator."""
        while self.down_stops:
            target, origin = heappop(self.down_stops)
            # target is stored as negative for min-heap; actual floor is abs(target)
            self.current_floor = abs(target)

            if abs(target) == origin:
                logger.info("[%s] floor %s: pick up", self.elevator_id, abs(target))
            else:
                logger.info("[%s] floor %s: let people out", self.elevator_id, abs(target))

        if self.up_stops:
            self.direction = Direction.UP
        else:
            self.direction = Direction.IDLE


if __name__ == "__main__":
    elevator = Elevator("1", 0)
    up_request1 = Request(elevator.current_floor, 5, RequestType.INTERNAL, Direction.UP)
    up_request2 = Request(elevator.current_floor, 3, RequestType.INTERNAL, Direction.UP)

    down_request1 = Request(
        elevator.current_floor, 1, RequestType.INTERNAL, Direction.DOWN
    )
    down_request2 = Request(
        elevator.current_floor, 2, RequestType.INTERNAL, Direction.DOWN
    )

    up_request3 = Request(4, 8, RequestType.EXTERNAL, Direction.UP)
    down_request3 = Request(6, 3, RequestType.EXTERNAL, Direction.DOWN)

    elevator.send_up_request(up_request1)
    elevator.send_up_request(up_request2)

    elevator.send_down_request(down_request1)
    elevator.send_down_request(down_request2)

    elevator.send_up_request(up_request3)
    elevator.send_down_request(down_request3)

    elevator.run()
