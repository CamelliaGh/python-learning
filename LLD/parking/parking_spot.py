"""
Low-Level Design: Parking Spot

This module implements a parking spot system.

Entities:
    - ParkingSpot: Represents a parking spot
    - ParkingSpotType: Represents the type of parking spot
"""
import logging
from enum import Enum

from car import Car

logger = logging.getLogger(__name__)

class ParkingSpotType(Enum):
    """
    Represents the type of parking spot.

    Attributes:
        SMALL (str): Represents a small parking spot
        MEDIUM (str): Represents a medium parking spot
        LARGE (str): Represents a large parking spot
    """
    SMALL = 0
    MEDIUM = 1
    LARGE = 2



class ParkingSpot:
    """
    Represents a parking spot.
    
    Attributes:
        spot_id (int): The unique identifier for the parking spot
        is_occupied (bool): Whether the parking spot is occupied
        spot_type (ParkingSpotType): The type of parking spot
    """
    def __init__(self, spot_id: int, spot_type: ParkingSpotType):
        self.spot_id = spot_id
        self.is_occupied = False
        self.spot_type = spot_type
        self.car = None
        logger.debug("Created parking spot spot_id=%s spot_type=%s", spot_id, spot_type.name)

    def assign_car(self, car: Car) -> None:
        """Assign a car to the parking spot."""
        self.car = car
        self.is_occupied = True
        logger.debug("Car assigned to parking spot spot_id=%s car_id=%s", self.spot_id, car.car_id)

    def release_car(self, car: Car) -> None:
        """Release a car from the parking spot."""
        if self.car != car:
            raise ValueError(f"Car {car.car_id} not assigned to this parking spot")
        self.car = None
        self.is_occupied = False
        logger.debug("Car released from parking spot spot_id=%s car_id=%s", self.spot_id, car.car_id)