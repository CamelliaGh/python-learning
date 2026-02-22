"""
Low-Level Design: Parking Lot

This module implements a parking lot system.

Entities:
    - ParkingLot: Represents a parking lot
    - ParkingSpot: Represents a parking spot
    - Car: Represents a car
    - Ticket: Represents a ticket
    - Payment: Represents a payment
"""

import logging
from datetime import datetime

from parking_spot import ParkingSpot, ParkingSpotType

from car import Car, CarType
from ticket import Ticket
from payment import Payment

logger = logging.getLogger(__name__)


class ParkingLot:
    """
    Represents a parking lot.

    Attributes:
        lot_id (int): The unique identifier for the parking lot
        name (str): The name of the parking lot
        address (str): The address of the parking lot
        parking_spots (list[ParkingSpot]): The parking spots in the parking lot
        tickets (list[Ticket]): The tickets for the parking spots
    """

    def __init__(
        self, lot_id: int, name: str, address: str, parking_spots: list[ParkingSpot]
    ):
        self.lot_id = lot_id
        self.name = name
        self.address = address
        self.parking_spots = parking_spots
        self.tickets = []
        logger.info(
            "Parking lot initialized lot_id=%s name=%s spots=%s",
            lot_id, name, len(parking_spots),
        )

    def park_car(self, car: Car) -> Ticket:
        """
        Park a car in the parking spot.
        """
        logger.info("Park request car_id=%s car_type=%s", car.car_id, car.car_type.name)
        for parking_spot in self.parking_spots:
            if not parking_spot.is_occupied and self._spot_fits_car(
                parking_spot.spot_type, car.car_type
            ):
                parking_spot.assign_car(car)
                ticket = Ticket(
                    ticket_id=len(self.tickets) + 1, car=car, parking_spot=parking_spot
                )
                self.tickets.append(ticket)
                logger.info(
                    "Car parked car_id=%s spot_id=%s ticket_id=%s",
                    car.car_id, parking_spot.spot_id, ticket.ticket_id,
                )
                return ticket
        logger.warning("No available spot for car_id=%s car_type=%s", car.car_id, car.car_type.name)
        raise ValueError(f"No available parking spots for this car type {car.car_type}")

    def unpark_car(self, ticket: Ticket) -> None:
        """
        Unpark a car from the parking spot.
        """
        logger.info("Unpark request ticket_id=%s spot_id=%s", ticket.ticket_id, ticket.parking_spot.spot_id)
        for parking_spot in self.parking_spots:
            if parking_spot.spot_id == ticket.parking_spot.spot_id:
                parking_spot.release_car(ticket.car)
                ticket.exit_time = datetime.now()
                self.tickets.remove(ticket)
                logger.info("Car unparked ticket_id=%s spot_id=%s car_id=%s", ticket.ticket_id, parking_spot.spot_id, ticket.car.car_id)
                return
        logger.error("Unpark failed: spot not found ticket_id=%s spot_id=%s", ticket.ticket_id, ticket.parking_spot.spot_id)
        raise ValueError("Parking spot not found")

    def exit_car(self, ticket: Ticket) -> None:
        """
        Exit a car from the parking spot.
        """
        logger.info("Exit request ticket_id=%s", ticket.ticket_id)
        self.unpark_car(ticket)
        payment = Payment(ticket)
        payment.calculate_amount()
        logger.info("Exit complete ticket_id=%s amount=%.2f", ticket.ticket_id, payment.amount)
        return payment.amount

    def _spot_fits_car(self, spot_type: ParkingSpotType, car_type: CarType) -> bool:
        """Return True if spot can fit this car type (spot size >= car size)."""
        return spot_type.value >= car_type.value


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    parking_lot = ParkingLot(
        lot_id=1,
        name="Parking Lot 1",
        address="123 Main St, Anytown, USA",
        parking_spots=[
            ParkingSpot(spot_id=1, spot_type=ParkingSpotType.SMALL),
            ParkingSpot(spot_id=2, spot_type=ParkingSpotType.MEDIUM),
            ParkingSpot(spot_id=3, spot_type=ParkingSpotType.LARGE),
        ],
    )

    try:
        car1 = Car(car_id=1, car_type=CarType.SMALL)
        ticket1 = parking_lot.park_car(car1)
        print(ticket1)
        amount_to_pay = parking_lot.exit_car(ticket1)
        print(f"Amount to pay: {amount_to_pay}")
    except ValueError as e:
        print(f"Error while parking or exiting car1: {e}")

    try:
        car2 = Car(car_id=2, car_type=CarType.LARGE)
        ticket2 = parking_lot.park_car(car2)
    except ValueError as e:
        print(f"Error while parking car2: {e}")

    try:
        car3 = Car(car_id=3, car_type=CarType.LARGE)
        ticket3 = parking_lot.park_car(car3)
    except ValueError as e:
        print(f"Error while parking car3: {e}")
