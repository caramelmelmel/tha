from enum import Enum

class SeatStatus(Enum):
    AVAILABLE = "available"
    SELECTED = "selected"
    BOOKED = "booked"