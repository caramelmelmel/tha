import unittest
from unittest.mock import MagicMock
from model import Seat
from seating_map import SeatingMap

class TestSeatAllocation(unittest.TestCase):
    def test_seat_should_have_immutable_properties(self):
        pass

    def test_seat_should_be_comparable(self):
        pass

    def test_seat_location_forma(self):
        pass

class MockSeatingMap:
    def __init__(self):
        self.seats = {}
        self.rows = 5
        self.seats_per_row = 10

    def add_seat(self, seat):
        self.seats[seat.row + str(seat.column).zfill(2)] = seat

# Create a mock SeatingMap object
mock_seating_map = MockSeatingMap()

# Add some mock seats to the seating map
for row in range(mock_seating_map.rows):
    for column in range(1, mock_seating_map.seats_per_row + 1):
        seat = MagicMock()
        seat.row = chr(65 + row)
        seat.column = column
        seat.status = "AVAILABLE"
        mock_seating_map.add_seat(seat)

class TestSeatMap(unittest.TestCase):
    def test_exceed_number_of_rows(self):
        with self.assertRaises(ValueError):
            SeatingMap(30, 40)
    
    def test_exceed_number_of_seats_per_row(self):
        with self.assertRaises(ValueError):
            SeatingMap(20, 61)
    
    def test_no_seats_per_col_or_row(self):
        with self.assertRaises(ValueError):
            SeatingMap(0, 0)
        
    def test_seat_map_should_have_correct_number_of_seats(self):
        num_rows = 20
        num_cols = 20
        seating_map = SeatingMap(20, 20)
        self.assertEqual(len(seating_map.seats), num_cols * num_rows)

    
class TestSeatSelectionStrategy:
    def test_seat_select_only_available_ones(self):
        pass

    def test_seat_select_only_valid_seat_format(self):
        pass

class TestCinemaBookingSystem:
    pass

    