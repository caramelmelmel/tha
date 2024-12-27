from abc import ABC, abstractmethod
from enums import SeatStatus
from seating_map import SeatingMap
from model import Seat
from typing import Optional, List

class SeatSelectionStrategy(ABC):
    @abstractmethod
    def select_seats(self, seating_map: 'SeatingMap', num_tickets: int, start_position: Optional[str] = None) -> Optional[List[Seat]]:
        pass

class DefaultSeatSelectionStrategy(SeatSelectionStrategy):
    def _get_middle_column(self, seats_per_row: int) -> int:
        return seats_per_row // 2

    def _get_seat_key(self, row: str, col: int) -> str:
        return f"{row}{col:02d}"

    def _is_valid_seat(self, row: str, col: int, seating_map: 'SeatingMap') -> bool:
        if col < 1 or col > seating_map.seats_per_row:
            return False
        key = self._get_seat_key(row, col)
        seat = seating_map.seats.get(key, None)
        return seat is not None and seat.status == SeatStatus.AVAILABLE

    def _get_consecutive_available_seats(self, row: str, start_col: int, seating_map: 'SeatingMap') -> List[int]:
        available_cols = []
        col = start_col
        while col <= seating_map.seats_per_row:
            if self._is_valid_seat(row, col, seating_map):
                available_cols.append(col)
                col += 1
            else:
                break
        return available_cols

    def select_seats(self, seating_map: 'SeatingMap', num_tickets: int, start_position: Optional[str] = None) -> Optional[List[Seat]]:
        print(seating_map)
        selected_seats: List[Seat] = []
        
        if start_position:
            start_row = start_position[0]
            start_col = int(start_position[1:])
            
            current_row = start_row
            remaining_tickets = num_tickets
            
            while remaining_tickets > 0 and current_row >= 'A':
                if start_col > seating_map.seats_per_row:
                    current_row = chr(ord(current_row) - 1)
                    start_col = self._get_middle_column(seating_map.seats_per_row)
                    continue

                available_cols = self._get_consecutive_available_seats(current_row, start_col, seating_map)
                seats_to_take = min(len(available_cols), remaining_tickets)
                
                if seats_to_take > 0:
                    for col in available_cols[:seats_to_take]:
                        selected_seats.append(Seat(
                            row=current_row,
                            column=col,
                            status=SeatStatus.SELECTED
                        ))
                    remaining_tickets -= seats_to_take
                
                if remaining_tickets > 0:
                    current_row = chr(ord(current_row) - 1)
                    start_col = self._get_middle_column(seating_map.seats_per_row)
                
            if remaining_tickets > 0:
                return None
                
        else:
            rows = [chr(65 + i) for i in range(seating_map.rows)]
            remaining_tickets = num_tickets
            
            for row in rows:
                if remaining_tickets == 0:
                    break
                    
                middle_col = self._get_middle_column(seating_map.seats_per_row)
                
                start_col = max(1, middle_col - (remaining_tickets // 2))
                
                available_cols = self._get_consecutive_available_seats(row, start_col, seating_map)
                seats_to_take = min(len(available_cols), remaining_tickets)
                
                if seats_to_take > 0:
                    
                    for col in available_cols[:seats_to_take]:
                        selected_seats.append(Seat(
                            row=row,
                            column=col,
                            status=SeatStatus.SELECTED
                        ))
                    remaining_tickets -= seats_to_take
            
            if remaining_tickets > 0:
                return None

        return selected_seats if selected_seats else None

    def _select_seats_from_position(
        self, seating_map: 'SeatingMap', num_tickets: int, start_row: str, start_col: int
    ) -> Optional[List[Seat]]:
        selected_seats: List[Seat] = []
        current_row = start_row
        current_col = start_col

        while len(selected_seats) < num_tickets:
            if current_row < 'A':
                return None

            if (current_col > seating_map.seats_per_row or
                not self._is_valid_seat(current_row, current_col, seating_map)):
                current_row = chr(ord(current_row) - 1)
                current_col = self._get_middle_column(seating_map.seats_per_row)
                continue

            key = self._get_seat_key(current_row, current_col)
            seat = seating_map.seats[key]
            selected_seats.append(Seat(
                row=seat.row,
                column=seat.column,
                status=SeatStatus.SELECTED
            ))
            current_col += 1

        return selected_seats