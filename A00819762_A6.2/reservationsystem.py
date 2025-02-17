"""
reservationsystem.py

Punto de entrada con menús interactivos para gestionar hoteles, clientes y reservas.
Se almacenan datos en TChotel.json, TCcustomer.json, TCreservation.json.
Los resultados se guardan (sobrescribiendo) en resultados.txt.

Requiere:
  - hotel.py
  - customer.py
  - reservation.py
"""

from hotel import HotelManager
from customer import CustomerManager
from reservation import ReservationManager

RESULT_FILE = "resultados.txt"


def write_result(text):
    """
    Escribe texto en 'resultados.txt' (sobrescribiendo),
    además de imprimirlo en consola.
    """
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write(text + "\n")
    print(text)


def menu_hoteles():
    """
    Muestra el submenú de gestión de hoteles.
    """
    while True:
        print("\n--- MENÚ HOTELES ---")
        print("1. Crear hotel")
        print("2. Buscar/Mostrar hotel")
        print("3. Modificar hotel")
        print("4. Eliminar hotel")
        print("5. Reservar habitación")
        print("6. Cancelar reserva de habitación")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            hotel_id = input("Ingrese ID del hotel (ej. H001): ")
            name = input("Ingrese nombre del hotel: ")
            location = input("Ingrese ubicación del hotel: ")
            total_rooms = input("Ingrese número total de habitaciones: ")

            if total_rooms.isdigit():
                creado = HotelManager.create_hotel(hotel_id, name, location, int(total_rooms))
                if creado:
                    write_result(f"Hotel {hotel_id} creado correctamente.")
                else:
                    write_result(f"No se pudo crear el hotel {hotel_id} (¿ya existía?).")
            else:
                write_result("Error: 'total_rooms' no es un número válido.")

        elif opcion == "2":
            hotel_id = input("Ingrese ID del hotel a buscar: ")
            info = HotelManager.display_hotel_info(hotel_id)
            if info:
                write_result("Información del hotel:\n" + info)
            else:
                write_result("No se encontró ese hotel.")

        elif opcion == "3":
            hotel_id = input("Ingrese ID del hotel a modificar: ")
            new_name = input("Nuevo nombre (deje vacío si no cambia): ")
            new_loc = input("Nueva ubicación (deje vacío si no cambia): ")
            new_rooms = input("Nuevo total de habitaciones (deje vacío si no cambia): ")

            kwargs = {}
            if new_name.strip():
                kwargs["name"] = new_name
            if new_loc.strip():
                kwargs["location"] = new_loc
            if new_rooms.isdigit():
                kwargs["total_rooms"] = int(new_rooms)

            modif = HotelManager.modify_hotel_info(hotel_id, **kwargs)
            if modif:
                write_result(f"Hotel {hotel_id} modificado correctamente.")
            else:
                write_result(f"No se pudo modificar (Hotel {hotel_id} no existe).")

        elif opcion == "4":
            hotel_id = input("Ingrese ID del hotel a eliminar: ")
            borrado = HotelManager.delete_hotel(hotel_id)
            if borrado:
                write_result(f"Hotel {hotel_id} eliminado correctamente.")
            else:
                write_result(f"No se pudo eliminar el hotel {hotel_id} (no existe).")

        elif opcion == "5":
            hotel_id = input("Ingrese ID del hotel en el que desea reservar: ")
            reservado = HotelManager.reserve_room(hotel_id)
            if reservado:
                write_result(f"Habitación reservada en el Hotel {hotel_id}.")
            else:
                write_result(f"No se pudo reservar. Verifique disponibilidad o ID.")

        elif opcion == "6":
            hotel_id = input("Ingrese ID del hotel para cancelar una reserva: ")
            cancelado = HotelManager.cancel_reservation(hotel_id)
            if cancelado:
                write_result(f"Reserva cancelada en el Hotel {hotel_id}.")
            else:
                write_result(f"No se pudo cancelar (tal vez no existe reserva o ID).")

        elif opcion == "0":
            break
        else:
            print("Opción inválida. Intente de nuevo.")


def menu_clientes():
    """
    Muestra el submenú de gestión de clientes.
    """
    while True:
        print("\n--- MENÚ CLIENTES ---")
        print("1. Crear cliente")
        print("2. Buscar/Mostrar cliente")
        print("3. Modificar cliente")
        print("4. Eliminar cliente")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            customer_id = input("Ingrese ID del cliente (ej. C001): ")
            name = input("Ingrese nombre del cliente: ")
            email = input("Ingrese correo electrónico: ")
            creado = CustomerManager.create_customer(customer_id, name, email)
            if creado:
                write_result(f"Cliente {customer_id} creado correctamente.")
            else:
                write_result(f"No se pudo crear el cliente {customer_id} (¿ya existía?).")

        elif opcion == "2":
            customer_id = input("Ingrese ID del cliente a buscar: ")
            info = CustomerManager.display_customer_info(customer_id)
            if info:
                write_result("Información del cliente:\n" + info)
            else:
                write_result(f"No se encontró cliente {customer_id}.")

        elif opcion == "3":
            customer_id = input("Ingrese ID del cliente a modificar: ")
            new_name = input("Nuevo nombre (deje vacío si no cambia): ")
            new_email = input("Nuevo correo (deje vacío si no cambia): ")

            kwargs = {}
            if new_name.strip():
                kwargs["name"] = new_name
            if new_email.strip():
                kwargs["email"] = new_email

            modif = CustomerManager.modify_customer_info(customer_id, **kwargs)
            if modif:
                write_result(f"Cliente {customer_id} modificado correctamente.")
            else:
                write_result(f"No se pudo modificar (Cliente {customer_id} no existe).")

        elif opcion == "4":
            customer_id = input("Ingrese ID del cliente a eliminar: ")
            borrado = CustomerManager.delete_customer(customer_id)
            if borrado:
                write_result(f"Cliente {customer_id} eliminado correctamente.")
            else:
                write_result(f"No se pudo eliminar el cliente {customer_id} (no existe).")

        elif opcion == "0":
            break
        else:
            print("Opción inválida. Intente de nuevo.")


def menu_reservas():
    """
    Muestra el submenú de gestión de reservas.
    """
    while True:
        print("\n--- MENÚ RESERVAS ---")
        print("1. Crear reserva")
        print("2. Mostrar reserva")
        print("3. Cancelar reserva")
        print("0. Volver al menú principal")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            reservation_id = input("Ingrese ID de la reserva (ej. R001): ")
            hotel_id = input("Ingrese ID del hotel: ")
            customer_id = input("Ingrese ID del cliente: ")
            date_str = input("Ingrese fecha (YYYY-MM-DD) [Enter para usar fecha actual]: ")
            date_str = date_str.strip() if date_str.strip() else None

            creado = ReservationManager.create_reservation(reservation_id, hotel_id, customer_id, date_str)
            if creado:
                write_result(f"Reserva {reservation_id} creada correctamente.")
            else:
                write_result(f"No se pudo crear la reserva {reservation_id}.")

        elif opcion == "2":
            reservation_id = input("Ingrese ID de la reserva a mostrar: ")
            info = ReservationManager.display_reservation_info(reservation_id)
            if info:
                write_result("Información de la reserva:\n" + info)
            else:
                write_result(f"No se encontró la reserva {reservation_id}.")

        elif opcion == "3":
            reservation_id = input("Ingrese ID de la reserva a cancelar: ")
            cancelado = ReservationManager.cancel_reservation(reservation_id)
            if cancelado:
                write_result(f"Reserva {reservation_id} cancelada correctamente.")
            else:
                write_result(f"No se pudo cancelar la reserva {reservation_id}.")

        elif opcion == "0":
            break
        else:
            print("Opción inválida. Intente de nuevo.")


def main():
    """
    Menú principal: permite elegir entre gestionar hoteles, clientes o reservas.
    """
    while True:
        print("\n=== SISTEMA DE RESERVAS ===")
        print("1. Gestionar Hoteles")
        print("2. Gestionar Clientes")
        print("3. Gestionar Reservas")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            menu_hoteles()
        elif opcion == "2":
            menu_clientes()
        elif opcion == "3":
            menu_reservas()
        elif opcion == "0":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    main()
