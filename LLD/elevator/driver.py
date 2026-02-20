"""
Low-Level Design: Elevator System Driver

This module implements a driver for the elevator system.

Entities:
    - Driver: Driver for the elevator system
    - ElevatorController: Controller for the elevator system
"""

import logging
import random

from elevator import Direction
from elevator_controller import ElevatorController
from request import Request, RequestType

# Configure logging for testing (timestamps + level + message)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)


class Driver:
    """Driver for the elevator system."""

    def __init__(self, elevator_controller: ElevatorController):
        self.elevator_controller = elevator_controller

    def run(self):
        """Run the driver."""
        logging.getLogger("elevator.driver").info("driver starting, sending test requests")
        self.elevator_controller.start()
        # send random requests to the elevator controller
        random_requests = [
            Request(random.randint(0, 10), random.randint(0, 10), RequestType.INTERNAL, Direction.UP),
            Request(random.randint(0, 10), random.randint(0, 10), RequestType.INTERNAL, Direction.DOWN),
            Request(random.randint(0, 10), random.randint(0, 10), RequestType.EXTERNAL, Direction.UP),
            Request(random.randint(0, 10), random.randint(0, 10), RequestType.EXTERNAL, Direction.DOWN),
        ]
        for i, request in enumerate(random_requests):
            self.elevator_controller.add_request(request)
        logging.getLogger("elevator.driver").info("all %s requests submitted", len(random_requests))




driver = Driver(ElevatorController())
driver.run()
