"""
Low-Level Design: Elevator System

This module implements a console-based elevator system with proper OOP design.

Entities:
    - ElevatorController: Controller for the elevator system
    - Elevator: Elevator for the elevator system
    - Direction: Enumeration of possible elevator directions
"""

import logging
import threading

from elevator import Direction, Elevator
from request import Request

logger = logging.getLogger("elevator.controller")


class ElevatorController:
    """Controller for the elevator system."""

    def __init__(self, max_floor=10):
        self.elevators: list[Elevator] = [
            Elevator("Elevator 1", max_floor),
            Elevator("Elevator 2", max_floor),
            Elevator("Elevator 3", max_floor),
        ]
        self.max_floor = max_floor
        logger.info(
            "controller init: max_floor=%s, elevators=%s",
            max_floor,
            [e.elevator_id for e in self.elevators],
        )

    def select_best_elevator(self, floor: int, direction: Direction) -> Elevator:
        """Select the best elevator: same direction or IDLE if any, else closest (handled when it reverses).
        When distance is tied, prefer the elevator with fewer queued stops to spread load."""
        best_same_direction = None
        min_distance_same = float("inf")
        for elev in self.elevators:
            if elev.direction in (direction, Direction.IDLE):
                distance = abs(elev.current_floor - floor)
                queue_size = len(elev.up_stops) + len(elev.down_stops)
                if distance < min_distance_same or (
                    distance == min_distance_same
                    and (
                        best_same_direction is None
                        or queue_size
                        < len(best_same_direction.up_stops)
                        + len(best_same_direction.down_stops)
                    )
                ):
                    min_distance_same = distance
                    best_same_direction = elev
        if best_same_direction is not None:
            logger.debug(
                "select_best_elevator floor=%s dir=%s -> %s (same direction)",
                floor,
                direction.value,
                best_same_direction.elevator_id,
            )
            return best_same_direction
        # All moving opposite: assign to closest; elevator will handle it when it reverses
        fallback = min(self.elevators, key=lambda e: abs(e.current_floor - floor))
        logger.debug(
            "select_best_elevator floor=%s dir=%s -> %s (fallback, will reverse)",
            floor,
            direction.value,
            fallback.elevator_id,
        )
        return fallback

    def add_request(self, request: Request) -> None:
        """Assign the request to the best elevator; that elevator will wake and process it."""
        best = self.select_best_elevator(request.origin, request.direction)
        logger.info(
            "add_request origin=%s target=%s dir=%s -> assigned to %s",
            request.origin,
            request.target,
            request.direction.value,
            best.elevator_id,
        )
        if request.direction == Direction.UP:
            best.send_up_request(request)
        else:
            best.send_down_request(request)

    def start(self):
        """Start the elevator controllers."""
        logger.info("starting %s elevator threads", len(self.elevators))
        for elev in self.elevators:
            threading.Thread(
                target=elev.run, daemon=True, name=elev.elevator_id
            ).start()
