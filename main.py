
"""
Modulo sqlite para base de datos
"""

import sqlite3


def crear_base_de_datos():
    """
    Crea la base de datos y el cursor para manipular la información
    """
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            unidades INTEGER NOT NULL,
            costo_total REAL NOT NULL,
            FOREIGN KEY(cliente_id) REFERENCES Clientes(id),
            FOREIGN KEY(producto_id) REFERENCES Menu(id)
        )
    ''')

    conn.commit()
    conn.close()


def agregar_cliente(nombre):
    """
    Funcion para agregar clientes a la base de datos
    """
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Clientes (nombre) VALUES (?)', (nombre,))
    conn.commit()
    conn.close()


def eliminar_cliente(cliente_id):
    """
    Funcion para eliminar clientes de la base de datos
    """
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Clientes WHERE id = ?', (cliente_id,))
    conn.commit()
    conn.close()


def actualizar_cliente(cliente_id, nuevo_nombre):
    """
    Funcion para actualizar la informacion de la base de datos
    """
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE Clientes SET nombre = ? WHERE id = ?', (nuevo_nombre, cliente_id))
    conn.commit()
    conn.close()


def agregar_producto(nombre, precio):
    """
    Funcion para agregar productos a la base de datos
    """
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Menu (nombre, precio) VALUES (?, ?)', (nombre, precio))
    conn.commit()
    conn.close()


def eliminar_producto(producto_id):
    """
    Funcion para eliminar productos de la base de datos
    """
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Menu WHERE id = ?', (producto_id,))
    conn.commit()
    conn.close()


def actualizar_producto(producto_id, nuevo_nombre, nuevo_precio):
    """
    Funcion para actualizar la informacion del producto de la base de datos
    """
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE Menu SET nombre = ?, precio = ? WHERE id = ?', (nuevo_nombre, nuevo_precio, producto_id))
    conn.commit()
    conn.close()


def listar_productos():
    """
    Funcion que enlista todos los productos guardados
    """
    conn = sqlite3.connect('restaurante.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, precio FROM Menu')
    productos = cursor.fetchall()
    conn.close()
    print("\nProductos en el Menú:")
    for producto in productos:
        print(f"ID: {producto[0]}, Nombre: {producto[1]}, Precio: ${producto[2]:.2f}")
    print()


# Funciones para Manejo de Pedidos
def manejar_pedidos():
    """
    Funcion que solicita datos para crear pedidos con clientes y productos ya guardados
    """
    try:
        conn = sqlite3.connect('restaurante.db')
        cursor = conn.cursor()

        cliente_id = int(input("Ingrese el ID del cliente: "))
        producto_id = int(input("Ingrese el ID del producto: "))
        unidades = int(input("Ingrese la cantidad de unidades: "))

        cursor.execute('SELECT nombre FROM Clientes WHERE id = ?', (cliente_id,))
        cliente = cursor.fetchone()
        if cliente is None:
            print("Error: No existe un cliente con ese ID.")
            return
        cliente_nombre = cliente[0]

        cursor.execute('SELECT nombre, precio FROM Menu WHERE id = ?', (producto_id,))
        producto = cursor.fetchone()
        if producto is None:
            print("Error: No existe un producto con ese ID.")
            return
        producto_nombre, precio = producto

        costo_total = precio * unidades

        cursor.execute('''
            INSERT INTO Pedido (cliente_id, producto_id, unidades, costo_total)
            VALUES (?, ?, ?, ?)
        ''', (cliente_id, producto_id, unidades, costo_total))

        conn.commit()

        with open('ticket.txt', 'w') as file:
            file.write(f"Cliente: {cliente_nombre}\n")
            file.write(f"Producto: {producto_nombre}\n")
            file.write(f"Precio por unidad: ${precio:.2f}\n")
            file.write(f"Unidades solicitadas: {unidades}\n")
            file.write(f"Costo total: ${costo_total:.2f}\n")

        print(f"\nProducto: {producto_nombre}")
        print(f"Precio por unidad: ${precio:.2f}")
        print(f"Unidades solicitadas: {unidades}")
        print(f"Costo total: ${costo_total:.2f}\n")
        print("Ticket generado en ticket.txt\n")
    except ValueError:
        print("Error: Por favor, ingrese un número válido para el precio y las unidades.")
    finally:
        conn.close()


# Función Principal y Manejo del Menú
def mostrar_menu():
    """
    Funcion que imprime las opciones del menu principal
    """
    print("\nBienvenido al sistema:")
    print("a. Pedidos")
    print("b. Clientes")
    print("c. Menú")
    print("d. Salir")
    print("r. Regresar")


def manejar_opcion(opcion):
    """
    Funcion para seleccionar las opciones del menu principal
    """
    if opcion.lower() == 'a' or opcion.lower() == "pedidos":
        manejar_pedidos()
    elif opcion.lower() == 'b' or opcion.lower() == "clientes":
        sub_menu_clientes()
    elif opcion.lower() == 'c' or opcion.lower() == "menú":
        sub_menu_menu()
    elif opcion.lower() == 'd' or opcion.lower() == "salir":
        print("Saliendo del programa...")
        return False
    elif opcion.lower() == 'r' or opcion.lower() == "regresar":
        print("Regresando al menú principal...")
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")
    return True


def sub_menu_clientes():
    """
    Funcion que imprime las acciones a realizar de la opcion clientes
    """
    print("\nGestión de Clientes:")
    print("1. Agregar Cliente")
    print("2. Eliminar Cliente")
    print("3. Actualizar Cliente")
    print("r. Regresar")
    opcion = input("Seleccione una opción: ")
    if opcion == '1':
        nombre = input("Ingrese el nombre del cliente: ")
        agregar_cliente(nombre)
    elif opcion == '2':
        cliente_id = int(input("Ingrese el ID del cliente a eliminar: "))
        eliminar_cliente(cliente_id)
    elif opcion == '3':
        cliente_id = int(input("Ingrese el ID del cliente a actualizar: "))
        nuevo_nombre = input("Ingrese el nuevo nombre del cliente: ")
        actualizar_cliente(cliente_id, nuevo_nombre)
    elif opcion.lower() == 'r':
        print("Regresando...")
    else:
        print("Opción no válida.")


def sub_menu_menu():
    """
    Funcion que imprime las acciones a realizar de la opcion menu
    """
    print("\nGestión del Menú:")
    print("1. Agregar Producto")
    print("2. Eliminar Producto")
    print("3. Actualizar Producto")
    print("4. Listar Productos")
    print("r. Regresar")
    opcion = input("Seleccione una opción: ")
    if opcion == '1':
        nombre = input("Ingrese el nombre del producto: ")
        precio = float(input("Ingrese el precio del producto: "))
        agregar_producto(nombre, precio)
    elif opcion == '2':
        producto_id = int(input("Ingrese el ID del producto a eliminar: "))
        eliminar_producto(producto_id)
    elif opcion == '3':
        producto_id = int(input("Ingrese el ID del producto a actualizar: "))
        nuevo_nombre = input("Ingrese el nuevo nombre del producto: ")
        nuevo_precio = float(input("Ingrese el nuevo precio del producto: "))
        actualizar_producto(producto_id, nuevo_nombre, nuevo_precio)
    elif opcion == '4':
        listar_productos()
    elif opcion.lower() == 'r':
        print("Regresando...")
    else:
        print("Opción no válida.")


def main():
    """
    Funcion para continuar
    """
    crear_base_de_datos()
    continuar = True
    while continuar:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        continuar = manejar_opcion(opcion)


if __name__ == "__main__":
    main()
