import unittest
from unittest.mock import MagicMock
from model import Seat
from seating_map import SeatingMap

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

    