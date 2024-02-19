import json
import os
import re
import datetime
from datetime import datetime

class Hotel:
    def __init__(self, name, location, rooms):
        self.name = name
        self.location = location
        self.rooms = {str(room_number): "available" for room_number in range(1, rooms + 1)}  # Ejemplo: {"1": "available", "2": "reserved"}

    def save_to_file(self):
        with open(f"{self.name}.json", "w") as file:
            json.dump(self.__dict__, file)

    @staticmethod
    def load_from_file(filename):
        with open(filename, "r") as file:
            data = json.load(file)
            hotel = Hotel(data["name"], data["location"], len(data["rooms"]))
            hotel.rooms = data["rooms"]
            return hotel
  
    @staticmethod
    def create_hotel():
        name_pattern = re.compile(r'^[A-Za-z\s]+$')  # Acepta letras y espacios
        rooms_pattern = re.compile(r'^\d{1,4}$')  # Rooms pattern
        name =  input("Enter hotel name: ")
        while name and not name_pattern.match(name):
            print("Invalid name. Please enter only letters.")
            name = input("Enter hotel name: ")
        location =  input("Enter hotel location: ")
        while location and not name_pattern.match(location):
            print("Invalid name. Please enter only letters.")
            location = input("Enter hotel location: ")
        rooms = input("Enter number of rooms: ")
        while not rooms_pattern.match(rooms):
            print("Invalid rooms number. Please enter a number with up to 4 digits.")
            rooms = input("Enter number of rooms: ")
        hotel = Hotel(name, location, int(rooms))
        hotel.save_to_file()

    @staticmethod
    def delete_hotel():
        name_pattern = re.compile(r'^[A-Za-z\s]+$')  # Acepta letras y espacios
        name =  input("Enter hotel name to delete: ")
        while name and not name_pattern.match(name):
            print("Invalid name. Please enter only letters.")
            name = input("Enter hotel name to delete: ")
        os.remove(f"{name}.json")

    @staticmethod
    def display_hotel_information():
        name_pattern = re.compile(r'^[A-Za-z\s]+$')  # Acepta letras y espacios
        name =  input("Enter hotel name to display: ")
        while name and not name_pattern.match(name):
            print("Invalid name. Please enter only letters.")
            name = input("Enter hotel name to display: ")
        hotel = Hotel.load_from_file(f"{name}.json")
        print(f"Hotel Name: {hotel.name}, Location: {hotel.location}, Rooms: {hotel.rooms}")

    @staticmethod
    def modify_hotel_information():
        name_pattern = re.compile(r'^[A-Za-z\s]+$')  # Acepta letras y espacios
        name =  input("Enter hotel name to modify: ")
        while name and not name_pattern.match(name):
            print("Invalid name. Please enter only letters.")
            name = input("Enter hotel name to modify: ")
        hotel = Hotel.load_from_file(f"{name}.json")
        new_name = input("Enter new hotel name (leave blank to keep current): ")
        new_location = input("Enter new hotel location (leave blank to keep current): ")
        all_rooms_available = all(status == "available" for status in hotel.rooms.values())

        if new_name:
            hotel.name = new_name
        if new_location:
            hotel.location = new_location
        if all_rooms_available:
            try:
                new_rooms = input("Enter new number of rooms (leave blank to keep current): ")
                if new_rooms:
                    new_rooms = int(new_rooms)
                    # Si el número de habitaciones se reduce, asegúrate de eliminar las habitaciones extras
                    # Si se aumenta, añade las nuevas habitaciones como disponibles
                    current_rooms = len(hotel.rooms)
                    if new_rooms < current_rooms:
                        for room_number in range(new_rooms + 1, current_rooms + 1):
                            del hotel.rooms[str(room_number)]
                    else:
                        for room_number in range(current_rooms + 1, new_rooms + 1):
                            hotel.rooms[str(room_number)] = "available"
            except ValueError:
                print("Invalid input for the number of rooms. It must be a number.")
        else:
            print("Cannot change the number of rooms because one or more rooms are reserved.")
        
        hotel.save_to_file()

    @staticmethod
    def reserve_a_room():
        name_pattern = re.compile(r'^[A-Za-z\s]+$')  # Acepta letras y espacios
        rooms_pattern = re.compile(r'^\d{1,4}$')  # Rooms pattern
        hotel_name =  input("Enter hotel name to delete: ")
        while hotel_name and not name_pattern.match(hotel_name):
            print("Invalid name. Please enter only letters.")
            hotel_name = input("Enter hotel name to delete: ")
        room_number = input("Enter room number to reserve: ")
        while not rooms_pattern.match(room_number):
            print("Invalid rooms number. Please enter a number with up to 4 digits.")
            room_number = input("Enter room number to reserve: ")
        hotel = Hotel.load_from_file(f"{hotel_name}.json")
        if hotel.rooms[room_number] == "available":
            hotel.rooms[room_number] = "reserved"
            hotel.save_to_file()
            print("Room reserved successfully.")
        else:
            print("Room is already reserved.")

    @staticmethod
    def cancel_a_reservation():
        name_pattern = re.compile(r'^[A-Za-z\s]+$')  # Acepta letras y espacios
        rooms_pattern = re.compile(r'^\d{1,4}$')  # Rooms pattern
        hotel_name =  input("Enter hotel name to delete: ")
        while hotel_name and not name_pattern.match(hotel_name):
            print("Invalid name. Please enter only letters.")
            hotel_name = input("Enter hotel name to delete: ")
        room_number = input("Enter room number to reserve: ")
        while not rooms_pattern.match(room_number):
            print("Invalid rooms number. Please enter a number with up to 4 digits.")
            room_number = input("Enter room number to reserve: ")   
        hotel = Hotel.load_from_file(f"{hotel_name}.json")
        if hotel.rooms[room_number] == "reserved":
            hotel.rooms[room_number] = "available"
            hotel.save_to_file()
            print("Reservation cancelled successfully.")
        else:
            print("Room is not reserved.")

    # Métodos para manejar comportamientos persistentes aquí

class Reservation:
    def __init__(self, customer_id, hotel_name, room_number, start_date, end_date):
        self.customer_id = customer_id
        self.hotel_name = hotel_name
        self.room_number = room_number
        self.start_date = start_date
        self.end_date = end_date
    
    def save_to_file(self):
        filename = f"reservation_{self.customer_id}_{self.hotel_name}_{self.room_number}.json"
        with open(filename, "w") as file:
            json.dump(self.__dict__, file)

    @staticmethod
    def create_reservation():
        customer_id_pattern = re.compile(r'^\d+$')  # Expresión regular para verificar que solo contiene números
        hotelname_pattern = re.compile(r'^[A-Za-z\s]+$')  # Acepta letras y espacios
        rooms_pattern = re.compile(r'^\d{1,4}$')  # Rooms pattern
        customer_id = customer_id = input("Enter customer ID: ")
        while not customer_id_pattern.match(customer_id):
            print("Invalid customer ID. Please enter only numbers.")
            customer_id = input("Enter customer ID: ")
        hotel_name = input("Enter hotel name: ")
        while hotel_name and not hotelname_pattern.match(hotel_name):
            print("Invalid name. Please enter only letters.")
            hotel_name = input("Enter hotel name: ")
        room_number = input("Enter number of rooms: ")
        while not rooms_pattern.match(room_number):
            print("Invalid rooms number. Please enter a number with up to 4 digits.")
            room_number = input("Enter number of rooms: ")

        # Validar formato de la fecha
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        start_date = input("Enter start date (YYYY-MM-DD): ")
        while not date_pattern.match(start_date):
            print("Invalid date format. Please use YYYY-MM-DD.")
            start_date = input("Enter start date (YYYY-MM-DD): ")
        
        # Convertir a objeto datetime y validar que sea mayor a la fecha actual
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
        if start_date_dt <= datetime.now():
            print("Start date must be greater than today's date.")
            return

        end_date = input("Enter end date (YYYY-MM-DD): ")
        while not date_pattern.match(end_date):
            print("Invalid date format. Please use YYYY-MM-DD.")
            end_date = input("Enter end date (YYYY-MM-DD): ")
        
        # Convertir a objeto datetime y validar que sea mayor a start_date
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
        if end_date_dt <= start_date_dt:
            print("End date must be greater than start date.")
            return

        # Verificar existencia del cliente y del hotel
        customer_file = f"customer_{customer_id}.json"
        hotel_file = f"{hotel_name}.json"
        if not os.path.exists(customer_file):
            print("Customer does not exist.")
            return
        if not os.path.exists(hotel_file):
            print("Hotel does not exist.")
            return

        # Cargar datos del hotel para verificar disponibilidad de la habitación
        hotel = Hotel.load_from_file(hotel_file)
        if hotel.rooms.get(room_number) != "available":
            print("Room is not available.")
            return

        reservation = Reservation(customer_id, hotel_name, room_number, start_date, end_date)
        reservation.save_to_file()

        # Marcar la habitación como reservada
        hotel.rooms[room_number] = "reserved"
        hotel.save_to_file()
        print("Reservation created successfully.")

    @staticmethod
    def cancel_reservation():
        customer_id_pattern = re.compile(r'^\d+$')  # Expresión regular para verificar que solo contiene números
        hotelname_pattern = re.compile(r'^[A-Za-z\s]+$')  # Acepta letras y espacios
        rooms_pattern = re.compile(r'^\d{1,4}$')  # Rooms pattern
        customer_id = customer_id = input("Enter customer ID: ")
        while not customer_id_pattern.match(customer_id):
            print("Invalid customer ID. Please enter only numbers.")
            customer_id = input("Enter customer ID: ")
        hotel_name = input("Enter hotel name: ")
        while hotel_name and not hotelname_pattern.match(hotel_name):
            print("Invalid name. Please enter only letters.")
            hotel_name = input("Enter hotel name: ")
        room_number = input("Enter number of rooms: ")
        while not rooms_pattern.match(room_number):
            print("Invalid rooms number. Please enter a number with up to 4 digits.")
            room_number = input("Enter number of rooms: ")
        
        reservation_file = f"reservation_{customer_id}_{hotel_name}_{room_number}.json"
        if not os.path.exists(reservation_file):
            print("Reservation does not exist.")
            return
        
        os.remove(reservation_file)
        
        # Cargar datos del hotel para marcar la habitación como disponible
        hotel = Hotel.load_from_file(f"{hotel_name}.json")
        hotel.rooms[room_number] = "available"
        hotel.save_to_file()
        print("Reservation cancelled successfully.")

class Customer:
    def __init__(self, customer_id, name, contact):
        self.customer_id = customer_id
        self.name = name
        self.contact = contact

    def save_to_file(self):
        with open(f"customer_{self.customer_id}.json", "w") as file:
            json.dump(self.__dict__, file)

    @staticmethod
    def load_from_file(customer_id):
        filename = f"customer_{customer_id}.json"
        if not os.path.exists(filename):
            print(f"No customer found with ID {customer_id}")
            return None
        with open(filename, "r") as file:
            data = json.load(file)
            return Customer(data["customer_id"], data["name"], data["contact"])

    @staticmethod
    def create_customer():
        customer_id_pattern = re.compile(r'^\d+$')  # Expresión regular para verificar que solo contiene números
        name_pattern = re.compile(r'^[A-Za-z\s]+$')  # Acepta letras y espacios
        contact_pattern = re.compile(r'^\d{1,10}$')  # Verifica que contenga entre 1 y 10 dígitos
        customer_id = input("Enter customer ID: ")
        while not customer_id_pattern.match(customer_id):
            print("Invalid customer ID. Please enter only numbers.")
            customer_id = input("Enter customer ID: ")
            
        name = input("Enter customer name: ")
        while name and not name_pattern.match(name):
            print("Invalid name. Please enter only letters.")
            name = input("Enter customer name: ")

        contact = input("Enter customer contact: ")
        while not contact_pattern.match(contact):
            print("Invalid contact. Please enter a number with up to 10 digits.")
            contact = input("Enter customer contact: ")

        customer = Customer(customer_id, name, contact)
        customer.save_to_file()
        print("Customer created successfully.")

    @staticmethod
    def delete_customer():
        customer_id_pattern = re.compile(r'^\d+$') 
        customer_id = input("Enter customer ID: ")
        while not customer_id_pattern.match(customer_id):
            print("Invalid customer ID. Please enter only numbers.")
            customer_id = input("Enter customer ID: ")
        filename = f"customer_{customer_id}.json"
        if os.path.exists(filename):
            os.remove(filename)
            print("Customer deleted successfully.")
        else:
            print("Customer not found.")

    @staticmethod
    def display_customer_information():
        customer_id_pattern = re.compile(r'^\d+$') 
        customer_id = input("Enter customer ID: ")
        while not customer_id_pattern.match(customer_id):
            print("Invalid customer ID. Please enter only numbers.")
            customer_id = input("Enter customer ID: ")
        customer = Customer.load_from_file(customer_id)
        if customer:
            print(f"Customer ID: {customer.customer_id}, Name: {customer.name}, Contact: {customer.contact}")

    def modify_customer_information():
        customer_id_pattern = re.compile(r'^\d+$')
        contact_pattern = re.compile(r'^\d{1,10}$')  # Modificado para aceptar hasta 10 dígitos
        name_pattern = re.compile(r'^[A-Za-z\s]+$')  # Acepta letras y espacios

        customer_id = input("Enter customer ID: ")
        while not customer_id_pattern.match(customer_id):
            print("Invalid customer ID. Please enter only numbers.")
            customer_id = input("Enter customer ID: ")

        customer = Customer.load_from_file(customer_id)
        if not customer:
            return

        new_name = input("Enter new name (leave blank to keep current): ")
        while new_name and not name_pattern.match(new_name):
            print("Invalid name. Please enter only letters.")
            new_name = input("Enter new name (leave blank to keep current): ")

        new_contact = input("Enter new contact (leave blank to keep current): ")
        while new_contact and not contact_pattern.match(new_contact):
            print("Invalid contact. Please enter a number with up to 10 digits.")
            new_contact = input("Enter new contact (leave blank to keep current): ")

        if new_name:
            customer.name = new_name
        if new_contact:
            customer.contact = new_contact

        customer.save_to_file()
        print("Customer information updated successfully.")

# Ejemplo de cómo podrías implementar el menú en consola

def main_menu():
    while True:
        print("\n--- Hotel Management System :)---")
        print("1. Manage Hotels")
        print("2. Manage Customers")
        print("3. Manage Reservations")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "4":
            break
        elif choice == "1":
            while True:
                print("\n--- Manage Hotels :)---")
                print("1. Create Hotel")
                print("2. Delete Hotel")
                print("3. Display Hotel information")
                print("4. Modify Hotel information")
                print("5. Reserve a Room")
                print("6. Cancel a reservation")
                print("7. Go back to previous menu")
                choice = input("Enter your choice: ")
                if choice == "7":
                    break
                elif choice == "1":
                    Hotel.create_hotel()
                elif choice == "2":
                    Hotel.delete_hotel()
                elif choice == "3":
                    Hotel.display_hotel_information()
                elif choice == "4":
                    Hotel.modify_hotel_information()
                elif choice == "5":
                    Hotel.reserve_a_room()
                elif choice == "6":
                    Hotel.cancel_a_reservation()
                else:
                    print("Invalid choice. Please enter a number between 1 and 7.")
        elif choice == "2":
            while True:
                print("\n--- Manage Customers :)---")
                print("1. Create Customer")
                print("2. Delete Customer")
                print("3. Display Customer information")
                print("4. Modify Customer information")
                print("5. Go back to previous menu")
                choice = input("Enter your choice: ")
                if choice == "5":
                    break
                elif choice == "1":
                    Customer.create_customer()
                elif choice == "2":
                    Customer.delete_customer()
                elif choice == "3":
                    Customer.display_customer_information()
                elif choice == "4":
                    Customer.modify_customer_information()
                else:
                    print("Invalid choice. Please enter a number between 1 and 5.")
                pass
        elif choice == "3":
            while True:
                print("\n--- Manage Reservation :)---")
                print("1. Create a Reservation")
                print("2. Cancel a Reservation")
                print("3. Go back to previous menu")
                choice = input("Enter your choice: ")
                if choice == "3":
                    break
                elif choice == "1":
                    Reservation.create_reservation()
                    pass
                elif choice == "2":
                    Reservation.cancel_reservation()
                    pass
                else:
                    print("Invalid choice. Please enter a number between 1 and 3.")
                pass
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main_menu()