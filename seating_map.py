from enums import SeatStatus
from model import Seat
from typing import Dict

MAX_NUMBER_OF_ROWS = 26
MAX_NUMBER_OF_SEATS_PER_ROW = 50

class SeatingMap:
    def __init__(self, rows: int, seats_per_row: int):
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.seats: Dict[str, Seat] = {}
        self.valid_seat_map(self.rows, self.seats_per_row)
        self._initialize_seats()
    
    def valid_seat_map(self, rows: int, seats_per_row: int):
        if rows <= 0 or seats_per_row <= 0 or rows > MAX_NUMBER_OF_ROWS or seats_per_row > MAX_NUMBER_OF_SEATS_PER_ROW:
            raise ValueError("Maximum Number of rows is 26 and maximum number of seats per row is 50")

    def _initialize_seats(self):
        for row in range(self.rows):
            row_letter = chr(65 + row)
            for col in range(1, self.seats_per_row + 1):
                key = f"{row_letter}{col:02d}"
                self.seats[key] = Seat(
                    row=row_letter,
                    column=col,
                    status=SeatStatus.AVAILABLE)
                