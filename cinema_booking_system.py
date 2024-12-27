from typing import Optional, Dict
from seat_selection_strategy import SeatSelectionStrategy, DefaultSeatSelectionStrategy
from seating_map import SeatingMap, SeatStatus
from model import Booking, Seat

class CinemaBookingSystem:
    def __init__(
        self,
        movie_title: str,
        rows: int,
        seats_per_row: int,
        strategy: Optional[SeatSelectionStrategy] = None
    ):
        self._validate_dimensions(rows, seats_per_row)
        self.movie_title = movie_title
        self.seating_map = SeatingMap(rows, seats_per_row)
        self.bookings: Dict[str, Booking] = {}
        self.next_booking_id = 1
        self.seat_selection_strategy = strategy or DefaultSeatSelectionStrategy()

    def _validate_dimensions(self, rows: int, seats_per_row: int):
        if rows > 26:
            raise ValueError("Maximum number of rows is 26")
        if seats_per_row > 50:
            raise ValueError("Maximum number of seats per row is 50")

    def get_available_seats(self) -> int:
        return sum(1 for seat in self.seating_map.seats.values()
                  if seat.status == SeatStatus.AVAILABLE)

    def clear_booking(self, booking_id: str):
        for key, seat in self.seating_map.seats.items():
            if seat.booking_id == booking_id:
                self.seating_map.seats[key] = Seat(
                    row=seat.row,
                    column=seat.column,
                    status=SeatStatus.AVAILABLE
                )

    def book_tickets(self, num_tickets: int, start_position: Optional[str] = None, booking_id: Optional[str] = None) -> Optional[Booking]:
        if num_tickets > self.get_available_seats():
            return None

        
        if booking_id:
            self.clear_booking(booking_id)
        
        selected_seats = self.seat_selection_strategy.select_seats(
            self.seating_map, num_tickets, start_position
        )

        if not selected_seats:
            return None

        
        if not booking_id:
            booking_id = f"GIC{self.next_booking_id:04d}"
            self.next_booking_id += 1

       
        for seat in selected_seats:
            key = f"{seat.row}{seat.column:02d}"
            self.seating_map.seats[key] = Seat(
                row=seat.row,
                column=seat.column,
                status=SeatStatus.BOOKED,
                booking_id=booking_id
            )

        booking = Booking(
            id=booking_id,
            movie_title=self.movie_title,
            seats=selected_seats
        )

        self.bookings[booking_id] = booking
        return booking

    def get_booking(self, booking_id: str) -> Optional[Booking]:
        return self.bookings.get(booking_id)

    def get_seating_map_display(self, highlight_booking_id: Optional[str] = None) -> str:
        display = "\n          S C R E E N\n"
        display += "--------------------------------\n"

        for row in range(self.seating_map.rows - 1, -1, -1):
            row_letter = chr(65 + row)
            display += f"{row_letter} "

            for col in range(1, self.seating_map.seats_per_row + 1):
                key = f"{row_letter}{col:02d}"
                seat = self.seating_map.seats[key]

                if seat.status == SeatStatus.AVAILABLE:
                    display += ".  "
                elif seat.status == SeatStatus.BOOKED:
                    display += "o  " if seat.booking_id == highlight_booking_id else "#  "
                else:
                    display += "o  "

            display += "\n"

        display += "  "
        for col in range(1, self.seating_map.seats_per_row + 1):
            display += f"{col:2d} "
        display += "\n"

        return display