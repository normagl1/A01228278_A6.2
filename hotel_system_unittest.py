import unittest
from unittest.mock import patch
from hotel_system import Hotel, Reservation, Customer  
import os

class TestHotel(unittest.TestCase):

    def setUp(self):
        self.hotel_name = "TestHotel"
        self.location = "TestLocation"
        self.rooms = 5
        self.rooms_data_mock = {"1": "available", "2": "available", "3": "available", "4": "available", "5": "available"}
        self.hotel = Hotel(self.hotel_name, self.location, self.rooms)
        self.hotel.save_to_file()

    def tearDown(self):
        if os.path.exists(f"{self.hotel_name}.json"):
            os.remove(f"{self.hotel_name}.json") 

    def test_file_save(self):
        self.assertTrue(os.path.exists(f"{self.hotel_name}.json"))

    def test_file_creation(self):
        self.hotel.create_hotel(self.hotel_name, self.location, self.rooms)
        self.assertTrue(os.path.exists(f"{self.hotel_name}.json"))        

    def test_load_from_file(self):
        """Prueba que el método load_from_file carga correctamente los datos del hotel desde un archivo."""
        hotel = Hotel.load_from_file(f"{self.hotel_name}.json")
        self.assertEqual(hotel.name, self.hotel_name)
        self.assertEqual(hotel.location, self.location)
        self.assertEqual(hotel.rooms, self.rooms_data_mock)
        self.assertEqual(len(hotel.rooms), len(self.rooms_data_mock))        

    @patch('sys.stdout')
    def test_display_hotel_information(self, mock_stdout):
        """Prueba que verifica si la información del hotel se muestra correctamente."""
        Hotel.display_hotel_information(self.hotel_name)
        expected_output = f"Hotel Name: {self.hotel_name}, Location: {self.location}, Rooms: {self.rooms_data_mock}"
        mock_stdout.write.assert_any_call(expected_output)

    def test_hotel_deletion(self):
        Hotel.delete_hotel(self.hotel_name)  
        self.assertFalse(os.path.exists(f"{self.hotel_name}.json"))        

class TestReservation(unittest.TestCase):
    def setUp(self):
        self.customer_id = "1"
        self.hotel_name = "TestHotel"
        self.room_number = "5"
        self.start_date = "2024-03-03"
        self.end_date = "2024-04-04"
        self.location = "TestLocation"
        self.rooms = 5
        self.reservation = Reservation(self.customer_id, self.hotel_name, self.room_number, self.start_date, self.end_date )
        self.reservation.save_to_file()

    def tearDown(self):
        if os.path.exists(f"reservation_{self.customer_id}_{self.hotel_name}_{self.room_number}.json"):
            os.remove(f"reservation_{self.customer_id}_{self.hotel_name}_{self.room_number}.json") 

    def test_save_to_file(self):
        self.assertTrue(os.path.exists(f"reservation_{self.customer_id}_{self.hotel_name}_{self.room_number}.json"))

    def test_file_creation(self):
        Reservation.create_reservation(self.customer_id,self.hotel_name, self.room_number, self.start_date, self.end_date)
        self.assertTrue(os.path.exists(f"reservation_{self.customer_id}_{self.hotel_name}_{self.room_number}.json"))      

    def test_cancel_reservation(self):
        self.hotel = Hotel(self.hotel_name, self.location, self.rooms)
        self.hotel.save_to_file()
        Reservation.cancel_reservation(self.customer_id, self.hotel_name, self.room_number)
        self.assertFalse(os.path.exists(f"reservation_{self.customer_id}_{self.hotel_name}_{self.room_number}.json"))
        
class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.customer_id = "10"
        self.customer_name = "Juan"
        self.contact = "0123456789"
        self.customer = Customer(self.customer_id, self.customer_name, self.contact )
        self.customer.save_to_file()

    def tearDown(self):
        if os.path.exists(f"customer_{self.customer_id}.json"):
            os.remove(f"customer_{self.customer_id}.json")

    def test_save_to_file(self):
        self.assertTrue(os.path.exists(f"customer_{self.customer_id}.json"))

    def test_file_creation(self):
        Customer.create_customer(self.customer_id, self.customer_name, self.contact )
        self.assertTrue(os.path.exists(f"customer_{self.customer_id}.json"))    


    @patch('sys.stdout')
    def test_display_customer_information(self, mock_stdout):
        """Prueba que verifica si la información del hotel se muestra correctamente."""
        Customer.display_customer_information(self.customer_id)
        expected_output = f"Customer ID: {self.customer_id}, Name: {self.customer_name}, Contact: {self.contact}"
        mock_stdout.write.assert_any_call(expected_output)
        
    def test_curstomer_deletion(self):
        Customer.delete_customer(self.customer_id) 
        self.assertFalse(os.path.exists(f"customer_{self.customer_id}.json"))    


if __name__ == '__main__':
    unittest.main()