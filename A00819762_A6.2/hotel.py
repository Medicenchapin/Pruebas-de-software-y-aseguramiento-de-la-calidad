"""
hotel.py

Define la clase Hotel y la clase HotelManager.
Usa TChotel.json para almacenar la información de hoteles.
"""

import json
import os


class Hotel:
    """
    Representa un Hotel con atributos básicos.
    """

    def __init__(self, hotel_id, name, location, total_rooms):
        """
        Inicializa un objeto Hotel.

        :param hotel_id: ID único del hotel.
        :param name: Nombre del hotel.
        :param location: Ubicación del hotel.
        :param total_rooms: Cantidad total de habitaciones.
        """
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.reserved_rooms = 0  # Cuántas habitaciones están reservadas

    def display_hotel_info(self):
        """
        Devuelve un string con la información del hotel.
        """
        info = (
            f"Hotel ID: {self.hotel_id}\n"
            f"Nombre: {self.name}\n"
            f"Ubicación: {self.location}\n"
            f"Habitaciones totales: {self.total_rooms}\n"
            f"Habitaciones reservadas: {self.reserved_rooms}\n"
            f"Habitaciones disponibles: {self.available_rooms()}\n"
        )
        return info

    def modify_hotel_info(self, name=None, location=None, total_rooms=None):
        """
        Modifica la información del hotel si se pasan nuevos valores.
        """
        if name is not None:
            self.name = name
        if location is not None:
            self.location = location
        if total_rooms is not None:
            self.total_rooms = total_rooms

    def available_rooms(self):
        """
        Retorna cuántas habitaciones siguen disponibles.
        """
        return self.total_rooms - self.reserved_rooms

    def reserve_room(self):
        """
        Reserva una habitación si hay disponibilidad.
        Retorna True si se pudo reservar, False si no había cupo.
        """
        if self.available_rooms() > 0:
            self.reserved_rooms += 1
            return True
        return False

    def cancel_reservation(self):
        """
        Cancela una reserva de habitación (si existe al menos una reservada).
        Retorna True si se pudo cancelar, False si no había reservas.
        """
        if self.reserved_rooms > 0:
            self.reserved_rooms -= 1
            return True
        return False


class HotelManager:
    """
    Clase que maneja (CRUD) los hoteles y su persistencia en TChotel.json.
    """

    FILE_PATH = "TChotel.json"

    @staticmethod
    def load_hotels():
        """
        Carga los hoteles desde TChotel.json.
        Retorna un diccionario {hotel_id: Hotel}.
        """
        if not os.path.exists(HotelManager.FILE_PATH):
            return {}

        try:
            with open(HotelManager.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
            hotels = {}
            for h_id, h_data in data.items():
                hotel = Hotel(
                    hotel_id=h_data["hotel_id"],
                    name=h_data["name"],
                    location=h_data["location"],
                    total_rooms=h_data["total_rooms"]
                )
                hotel.reserved_rooms = h_data["reserved_rooms"]
                hotels[h_id] = hotel
            return hotels
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            print(f"[Error] Datos de hotel inválidos: {error}")
            return {}

    @staticmethod
    def save_hotels(hotels):
        """
        Guarda en TChotel.json los datos de un dict {hotel_id: Hotel}.
        """
        data = {}
        for h_id, hotel in hotels.items():
            data[h_id] = {
                "hotel_id": hotel.hotel_id,
                "name": hotel.name,
                "location": hotel.location,
                "total_rooms": hotel.total_rooms,
                "reserved_rooms": hotel.reserved_rooms
            }
        with open(HotelManager.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    @staticmethod
    def create_hotel(hotel_id, name, location, total_rooms):
        hotels = HotelManager.load_hotels()
        if hotel_id in hotels:
            print(f"Hotel con ID '{hotel_id}' ya existe.")
            return False
        hotels[hotel_id] = Hotel(hotel_id, name, location, total_rooms)
        HotelManager.save_hotels(hotels)
        return True

    @staticmethod
    def delete_hotel(hotel_id):
        hotels = HotelManager.load_hotels()
        if hotel_id not in hotels:
            print(f"No se encontró hotel con ID '{hotel_id}'.")
            return False
        del hotels[hotel_id]
        HotelManager.save_hotels(hotels)
        return True

    @staticmethod
    def display_hotel_info(hotel_id):
        hotels = HotelManager.load_hotels()
        if hotel_id not in hotels:
            print(f"No se encontró hotel con ID '{hotel_id}'.")
            return ""
        return hotels[hotel_id].display_hotel_info()

    @staticmethod
    def modify_hotel_info(hotel_id, **kwargs):
        hotels = HotelManager.load_hotels()
        if hotel_id not in hotels:
            print(f"No se encontró hotel con ID '{hotel_id}'.")
            return False
        hotels[hotel_id].modify_hotel_info(**kwargs)
        HotelManager.save_hotels(hotels)
        return True

    @staticmethod
    def reserve_room(hotel_id):
        hotels = HotelManager.load_hotels()
        if hotel_id not in hotels:
            print(f"No se encontró hotel con ID '{hotel_id}'.")
            return False
        success = hotels[hotel_id].reserve_room()
        HotelManager.save_hotels(hotels)
        return success

    @staticmethod
    def cancel_reservation(hotel_id):
        hotels = HotelManager.load_hotels()
        if hotel_id not in hotels:
            print(f"No se encontró hotel con ID '{hotel_id}'.")
            return False
        success = hotels[hotel_id].cancel_reservation()
        HotelManager.save_hotels(hotels)
        return success
