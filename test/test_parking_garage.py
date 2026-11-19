from datetime import datetime
from unittest import TestCase
from unittest.mock import patch
from unittest.mock import MagicMock

import mock.GPIO as GPIO
from mock.SDL_DS3231 import SDL_DS3231
from src.parking_garage import ParkingGarage
from src.parking_garage import ParkingGarageError

class TestParkingGarage(TestCase):

    @patch.object(GPIO, "setup")
    def test_detection_sensors_config(self, mock_setup: MagicMock):
        parking_garage = ParkingGarage()
        mock_setup.assert_any_call(ParkingGarage.INFRARED_PIN1, GPIO.IN)
        mock_setup.assert_any_call(ParkingGarage.INFRARED_PIN2, GPIO.IN)
        mock_setup.assert_any_call(ParkingGarage.INFRARED_PIN3, GPIO.IN)

    @patch.object(GPIO, "input")
    def test_check_occupancy_car_detected(self, mock_input: MagicMock):
        mock_input.return_value(True)
        parking_garage = ParkingGarage()
        occupied = parking_garage.check_occupancy(parking_garage.INFRARED_PIN2)
        self.assertFalse(occupied)

    @patch.object(GPIO, "input")
    def test_check_occupancy_car_not_detected(self, mock_input: MagicMock):
        mock_input.return_value(True)
        parking_garage = ParkingGarage()
        occupied=parking_garage.check_occupancy(parking_garage.INFRARED_PIN2)
        self.assertFalse(occupied)

    def test_check_occupancy_wrong_pin(self):
        parking_garage = ParkingGarage()
        self.assertRaises(ParkingGarageError, parking_garage.check_occupancy, parking_garage.SERVO_PIN)

    @patch.object(GPIO, "input")
    def test_check_occupied_spots_full(self, mock_input: MagicMock):
        mock_input.side_effect=[False,False,False]
        parking_garage = ParkingGarage()
        occupied_spots=parking_garage.get_number_occupied_spots()
        self.assertEqual(occupied_spots,3)

    @patch.object(SDL_DS3231, "__init__",return_value=None)
    def test_RTC_config(self, mock_rtc_setup: MagicMock):
        parking_garage = ParkingGarage()
        mock_rtc_setup.assert_called_once()

    @patch.object(SDL_DS3231, "read_datetime")
    def test_calculate_fee_2h(self, mock_read_datetime: MagicMock):
        mock_read_datetime.return_value=datetime(2026,11,19,10,11)
        parking_garage = ParkingGarage()
        fee=parking_garage.calculate_parking_fee(datetime(2026,11,19,8,11))
        self.assertEqual(fee,5)

    @patch.object(SDL_DS3231, "read_datetime")
    def test_calculate_fee_fraction_hours(self, mock_read_datetime: MagicMock):
        mock_read_datetime.return_value=datetime(2026,11,19,10,12)
        parking_garage = ParkingGarage()
        fee=parking_garage.calculate_parking_fee(datetime(2026,11,19,8,11))
        self.assertEqual(fee,7.5)


