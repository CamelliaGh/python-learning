"""
Low-Level Design: Parking Ticket

This module implements a parking ticket system.

Entities:
    - Ticket: Represents a parking ticket
    - Car: Represents a car
    - ParkingSpot: Represents a parking spot
"""
import logging
from datetime import datetime

from car import Car
from parking_spot import ParkingSpot

logger = logging.getLogger(__name__)

class Ticket:
    """
    Represents a parking ticket.

    Attributes:
        ticket_id (int): The unique identifier for the ticket
        car (Car): The car that the ticket is for
        parking_spot (ParkingSpot): The parking spot that the car is parked in
        entry_time (datetime): The time the car entered the parking spot
        exit_time (datetime): The time the car exited the parking spot
    """
    def __init__(self, ticket_id: int, car: Car, parking_spot: ParkingSpot):
        self.ticket_id = ticket_id
        self.car = car
        self.parking_spot = parking_spot
        self.entry_time = datetime.now()
        self.exit_time = None
        logger.debug("Ticket issued ticket_id=%s car_id=%s spot_id=%s", ticket_id, car.car_id, parking_spot.spot_id)

    def __str__(self) -> str:
        return f"Ticket ID: {self.ticket_id}, Car: {self.car.car_id}, Parking Spot: {self.parking_spot.spot_id}, Entry Time: {self.entry_time}, Exit Time: {self.exit_time}"
