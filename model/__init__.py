from dataclasses import dataclass
from enums.seat_status import SeatStatus
from typing import Optional, List

@dataclass
class Seat:
    row: str
    column: int
    status: SeatStatus
    booking_id: Optional[str] = None

@dataclass
class Booking:
    id: str
    movie_title: str
    seats: List[Seat]