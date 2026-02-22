"""
Low-Level Design: Parking Payment

This module implements a payment system for a parking ticket.

Entities:
    - Payment: Represents a payment for a parking ticket
    - Ticket: Represents a parking ticket
"""
import logging

from ticket import Ticket

logger = logging.getLogger(__name__)

HOUR_RATE = 10

class Payment:
    """
    Represents a payment for a parking ticket.

    Attributes:
        ticket (Ticket): The ticket that the payment is for
        amount (float): The amount of the payment
    """
    def __init__(self, ticket: Ticket):
        """
        Initialize a payment for a parking ticket.
        """
        self.ticket = ticket
        self.amount = 0

    def calculate_amount(self) -> float:
        """
        Calculate the amount of the payment.
        """
        duration_seconds = (self.ticket.exit_time - self.ticket.entry_time).total_seconds()
        self.amount = duration_seconds / 3600 * HOUR_RATE
        logger.info(
            "Payment calculated ticket_id=%s duration_hours=%.2f amount=%.2f",
            self.ticket.ticket_id, duration_seconds / 3600, self.amount,
        )
        return self.amount
