"""
Low-Level Design: Car

This module implements a car system.

Entities:
    - Car: Represents a car
    - CarType: Represents the type of car
"""

import logging
from enum import Enum

logger = logging.getLogger(__name__)


class CarType(Enum):
    """
    Represents the type of car.

    Attributes:
        SMALL (str): Represents a small car
        MEDIUM (str): Represents a medium car
        LARGE (str): Represents a large car
    """

    SMALL = 0
    MEDIUM = 1
    LARGE = 2


class Car:
    """
    Represents a car.
    Attributes:
        car_id (int): The unique identifier for the car
        car_type (CarType): The type of car
    """

    def __init__(self, car_id: int, car_type: CarType):
        self.car_id = car_id
        self.car_type = car_type
        logger.debug("Car created car_id=%s car_type=%s", car_id, car_type.name)
    def __str__(self) -> str:
        return f"Car ID: {self.car_id}, Car Type: {self.car_type}"
