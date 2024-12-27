import unittest
from unittest.mock import Mock, patch, MagicMock
from typing import List, Optional
from dataclasses import dataclass
from enums import SeatStatus
from seating_map import SeatingMap
from model import Seat
from cinema_booking_system import CinemaBookingSystem
from seat_selection_strategy import DefaultSeatSelectionStrategy, SeatSelectionStrategy

class StubSeatSelectionStrategy(SeatSelectionStrategy):
    def select_seats(self, seating_map: 'SeatingMap', num_tickets: int, 
                    start_position: Optional[str] = None) -> Optional[List[Seat]]:
        return [
            Seat(row="A", column=i, status=SeatStatus.SELECTED)
            for i in range(1, num_tickets + 1)
        ]

class FakeSeatingMap:
    def __init__(self, rows: int, seats_per_row: int):
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.seats = {
            "A01": Seat(row="A", column=1, status=SeatStatus.AVAILABLE),
            "A02": Seat(row="A", column=2, status=SeatStatus.AVAILABLE),
            "B01": Seat(row="B", column=1, status=SeatStatus.BOOKED)
        }

class TestWithMocks(unittest.TestCase):
    def setUp(self):
        self.mock_strategy = Mock(spec=SeatSelectionStrategy)
        self.cinema = CinemaBookingSystem(
            "Test Movie", 3, 5, strategy=self.mock_strategy
        )

    def test_strategy_called_with_correct_args(self):
        self.mock_strategy.select_seats.return_value = [
            Seat(row="A", column=1, status=SeatStatus.SELECTED)
        ]
        self.cinema.book_tickets(1, "A1")
        self.mock_strategy.select_seats.assert_called_once_with(
            self.cinema.seating_map, 1, "A1"
        )

    def test_booking_with_failed_strategy(self):
        self.mock_strategy.select_seats.return_value = None
        result = self.cinema.book_tickets(1)
        self.assertIsNone(result)

class TestWithStubs(unittest.TestCase):
    def setUp(self):
        self.stub_strategy = StubSeatSelectionStrategy()
        self.cinema = CinemaBookingSystem(
            "Test Movie", 3, 5, strategy=self.stub_strategy
        )

    def test_booking_with_stub_strategy(self):
        booking = self.cinema.book_tickets(2)
        self.assertEqual(len(booking.seats), 2)
        self.assertEqual(booking.seats[0].row, "A")
        self.assertEqual(booking.seats[0].column, 1)

class TestWithFakes(unittest.TestCase):
    def setUp(self):
        self.fake_seating_map = FakeSeatingMap(2, 2)
        self.strategy = DefaultSeatSelectionStrategy()

    def test_select_seats_with_fake_map(self):
        seats = self.strategy.select_seats(self.fake_seating_map, 2)
        self.assertIsNotNone(seats)
        self.assertEqual(len(seats), 2)

@patch('seating_map.SeatingMap')
class TestWithPatching(unittest.TestCase):

    def test_booking_system_with_mocked_map(self, mock_seating_map_class):
        mock_map = MagicMock()
        mock_map.seats = {
            "A01": Seat(row="A", column=1, status=SeatStatus.AVAILABLE)
        }
        mock_seating_map_class.return_value = mock_map
        
        cinema = CinemaBookingSystem("Test Movie", 1, 1)
        cinema.book_tickets(1)
        self.assertEqual(len(cinema.bookings), 1)