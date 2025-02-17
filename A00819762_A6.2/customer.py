"""
customer.py

Define la clase Customer y CustomerManager.
Usa TCcustomer.json para almacenar la información de clientes.
"""

import json
import os


class Customer:
    """
    Representa un cliente con ID, nombre y correo.
    """

    def __init__(self, customer_id, name, email):
        """
        Inicializa un objeto Customer.

        :param customer_id: ID único del cliente.
        :param name: Nombre del cliente.
        :param email: Correo electrónico.
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def display_customer_info(self):
        """
        Devuelve un string con la información del cliente.
        """
        info = (
            f"Customer ID: {self.customer_id}\n"
            f"Nombre: {self.name}\n"
            f"Correo: {self.email}\n"
        )
        return info

    def modify_customer_info(self, name=None, email=None):
        """
        Modifica la información del cliente si se pasan nuevos valores.
        """
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email


class CustomerManager:
    """
    Maneja (CRUD) los clientes y su persistencia en TCcustomer.json.
    """

    FILE_PATH = "TCcustomer.json"

    @staticmethod
    def load_customers():
        """
        Carga clientes de TCcustomer.json.
        Retorna un dict {customer_id: Customer}.
        """
        if not os.path.exists(CustomerManager.FILE_PATH):
            return {}

        try:
            with open(CustomerManager.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
            customers = {}
            for c_id, c_data in data.items():
                customer = Customer(
                    customer_id=c_data["customer_id"],
                    name=c_data["name"],
                    email=c_data["email"]
                )
                customers[c_id] = customer
            return customers
        except (json.JSONDecodeError, KeyError, TypeError) as error:
            print(f"[Error] Datos de cliente inválidos: {error}")
            return {}

    @staticmethod
    def save_customers(customers):
        """
        Guarda en TCcustomer.json los datos de {customer_id: Customer}.
        """
        data = {}
        for c_id, cust in customers.items():
            data[c_id] = {
                "customer_id": cust.customer_id,
                "name": cust.name,
                "email": cust.email
            }
        with open(CustomerManager.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    @staticmethod
    def create_customer(customer_id, name, email):
        customers = CustomerManager.load_customers()
        if customer_id in customers:
            print(f"Cliente con ID '{customer_id}' ya existe.")
            return False
        customers[customer_id] = Customer(customer_id, name, email)
        CustomerManager.save_customers(customers)
        return True

    @staticmethod
    def delete_customer(customer_id):
        customers = CustomerManager.load_customers()
        if customer_id not in customers:
            print(f"No se encontró cliente con ID '{customer_id}'.")
            return False
        del customers[customer_id]
        CustomerManager.save_customers(customers)
        return True

    @staticmethod
    def display_customer_info(customer_id):
        customers = CustomerManager.load_customers()
        if customer_id not in customers:
            print(f"No se encontró cliente con ID '{customer_id}'.")
            return ""
        return customers[customer_id].display_customer_info()

    @staticmethod
    def modify_customer_info(customer_id, **kwargs):
        customers = CustomerManager.load_customers()
        if customer_id not in customers:
            print(f"No se encontró cliente con ID '{customer_id}'.")
            return False
        customers[customer_id].modify_customer_info(**kwargs)
        CustomerManager.save_customers(customers)
        return True
