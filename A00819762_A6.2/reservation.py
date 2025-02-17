"""
reservation.py

Define la clase Reservation y ReservationManager.
Usa TCreservation.json para almacenar la información de reservas.
"""

import json
import os
from datetime import datetime

from hotel import HotelManager
from customer import CustomerManager


class Reservation:
    """
    Representa una reservación que asocia un Hotel y un Customer.
    """

    def __init__(self, reservation_id, hotel_id, customer_id, date_str=None):
        """
        Inicializa una Reservation.

        :param reservation_id: ID único de la reservación.
        :param hotel_id: ID del Hotel asociado.
        :param customer_id: ID del cliente asociado.
        :param date_str: Fecha de la reserva (por defecto, hoy).
        """
        self.reservation_id = reservation_id
        self.hotel_id = hotel_id
        self.customer_id = customer_id
        self.date_str = date_str or datetime.now().strftime("%Y-%m-%d")

    def display_reservation_info(self):
        """
        Devuelve un string con la info de la reservación.
        """
        info = (
            f"Reservation ID: {self.reservation_id}\n"
            f"Hotel ID: {self.hotel_id}\n"
            f"Customer ID: {self.customer_id}\n"
            f"Fecha: {self.date_str}\n"
        )
        return info


class ReservationManager:
    """
    Maneja (CRUD) las reservas y su persistencia en TCreservation.json.
    """

    FILE_PATH = "TCreservation.json"

    @staticmethod
    def load_reservations():
        """
        Carga las reservas de TCreservation.json.
        Retorna {reservation_id: Reservation}.
        """
        if not os.path.exists(ReservationManager.FILE_PATH):
            return {}

        try:
            with open(ReservationManager.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
            reservations = {}
            for r_id, r_data in data.items():
                reservation = Reservation(
                    reservation_id=r_data["reservation_id"],
                    hotel_id=r_data["hotel_id"],
                    customer_id=r_data["customer_id"],
                    date_str=r_data["date_str"]
                )
                reservations[r_id] = reservation
            return reservations
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            print(f"[Error] Datos de reserva inválidos: {error}")
            return {}

    @staticmethod
    def save_reservations(reservations):
        """
        Guarda en TCreservation.json los datos de {reservation_id: Reservation}.
        """
        data = {}
        for r_id, reservation in reservations.items():
            data[r_id] = {
                "reservation_id": reservation.reservation_id,
                "hotel_id": reservation.hotel_id,
                "customer_id": reservation.customer_id,
                "date_str": reservation.date_str
            }
        with open(ReservationManager.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    @staticmethod
    def create_reservation(reservation_id, hotel_id, customer_id, date_str=None):
        """
        Crea una nueva reserva y también reserva una habitación en el hotel.
        Verifica si existe el hotel y el cliente antes de crear.
        """
        hotels = HotelManager.load_hotels()
        if hotel_id not in hotels:
            print(f"No se encontró hotel con ID '{hotel_id}'.")
            return False

        customers = CustomerManager.load_customers()
        if customer_id not in customers:
            print(f"No se encontró cliente con ID '{customer_id}'.")
            return False

        # Reservar habitación en el hotel
        success = hotels[hotel_id].reserve_room()
        if not success:
            print("No hay disponibilidad en el hotel.")
            return False
        # Guardar la info del hotel actualizada
        HotelManager.save_hotels(hotels)

        # Crear la reserva si no existe ya
        reservations = ReservationManager.load_reservations()
        if reservation_id in reservations:
            print(f"Reserva con ID '{reservation_id}' ya existe.")
            return False

        reservations[reservation_id] = Reservation(
            reservation_id, hotel_id, customer_id, date_str
        )
        ReservationManager.save_reservations(reservations)
        return True

    @staticmethod
    def cancel_reservation(reservation_id):
        """
        Cancela la reserva si existe, liberando la habitación en el hotel asociado.
        """
        reservations = ReservationManager.load_reservations()
        if reservation_id not in reservations:
            print(f"No se encontró reserva con ID '{reservation_id}'.")
            return False

        hotel_id = reservations[reservation_id].hotel_id
        del reservations[reservation_id]
        ReservationManager.save_reservations(reservations)

        # Liberar la habitación en el hotel
        hotels = HotelManager.load_hotels()
        if hotel_id in hotels:
            hotels[hotel_id].cancel_reservation()
            HotelManager.save_hotels(hotels)

        return True

    @staticmethod
    def display_reservation_info(reservation_id):
        """
        Muestra la información de una reserva específica.
        """
        reservations = ReservationManager.load_reservations()
        if reservation_id not in reservations:
            print(f"No se encontró reserva con ID '{reservation_id}'.")
            return ""
        return reservations[reservation_id].display_reservation_info()
