import sqlite3

# Clase que maneja la conexión y las operaciones básicas en la base de datos
class BaseDeDatos:

    # Constructor
    def __init__(self, db_name="inventario.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.crear_tabla()

    # Método para crear la tabla de productos
    def crear_tabla(self):
        query = """
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT,
            stock INTEGER NOT NULL,
            tipo TEXT,
            garantia INTEGER
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    # Método para ejecutar una Operacion SQL
    def ejecutar_consulta(self, query, parametros=None):
        if parametros:
            self.cursor.execute(query, parametros)
        else:
            self.cursor.execute(query)
        self.conn.commit()

    # Método para consultar la base de datos
    def consultar(self, query, parametros=None):
        if parametros:
            self.cursor.execute(query, parametros)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall() # Obtenemos la lista de resultados

    # Método para cerrar la conexión a la base de datos
    def cerrar_conexion(self):
        self.conn.close()





# Clase base que representa un producto genérico
class Producto:
    def __init__(self, nombre, categoria, stock):
        self.nombre = nombre
        self.categoria = categoria
        self.stock = stock

    def __str__(self):
        return f"Nombre: {self.nombre}, Categoría: {self.categoria}, Stock: {self.stock}"





# Subclase de Producto para productos electrónicos
class ProductoElectronico(Producto):
    def __init__(self, nombre, categoria, stock, garantia):
        super().__init__(nombre, categoria, stock)  # Llama al constructor de Producto
        self.garantia = garantia  # Meses de garantía

    def __str__(self):
        return super().__str__() + f", Garantía: {self.garantia} meses"




# Clase que administra el inventario utilizando la base de datos
class Inventario:
    def __init__(self, base_de_datos):
        self.db = base_de_datos

    def agregar_producto(self, producto):
        tipo = type(producto).__name__  # Obtenemos el tipo de producto
        garantia = getattr(producto, "garantia", None)  # Garantía solo para electrónicos
        query = """
        INSERT INTO productos (nombre, categoria, stock, tipo, garantia)
        VALUES (?, ?, ?, ?, ?)
        """
        self.db.ejecutar_consulta(query, (producto.nombre, producto.categoria, producto.stock, tipo, garantia))
        print(f"Producto '{producto.nombre}' agregado con éxito.")

    def eliminar_producto(self, producto_id):

        # query_exists = "SELECT * FROM productos WHERE id = ?"
        # result = self.db.ejecutar_consulta(query_exists, (producto_id,))
        # if result:
        query = "DELETE FROM productos WHERE id = ?"
        self.db.ejecutar_consulta(query, (producto_id,))
        print(f"Producto con ID {producto_id} eliminado con éxito.")
        # else:
            # print(f"No se encontró el producto con ID {producto_id}.")


    def actualizar_stock(self, producto_id, nuevo_stock):
        query = "UPDATE productos SET stock = ? WHERE id = ?"
        self.db.ejecutar_consulta(query, (nuevo_stock, producto_id))
        print(f"Stock del producto con ID {producto_id} actualizado a {nuevo_stock}.")

    def mostrar_productos(self):
        query = "SELECT * FROM productos"
        productos = self.db.consultar(query)
        if productos:
            print("\nLista de productos:")
            for prod in productos:
                tipo = prod[4]
                if tipo == "ProductoElectronico":
                    producto = ProductoElectronico(prod[1], prod[2], prod[3], prod[5])
                else:
                    producto = Producto(prod[1], prod[2], prod[3])
                print(f"ID: {prod[0]}, {producto}")
        else:
            print("\nNo hay productos en el inventario.")




# Función que muestra el menú principal
def menu():
    opciones = (
        "1. Agregar producto genérico",
        "2. Agregar producto electrónico",
        "3. Eliminar producto",
        "4. Actualizar stock",
        "5. Mostrar productos",
        "6. Salir"
    )
    print("\n" + "\n".join(opciones))


# Función principal
def main():

    base_datos = BaseDeDatos()
    inventario = Inventario(base_datos)

    while True:

        menu()

        opcion = input("\nSeleccione una opción: ") # Obtenemos la opción del usuario

        if opcion == "1": # Agregar producto genérico
            nombre = input("Nombre del producto: ")
            categoria = input("Categoría del producto: ")
            try:
                stock = int(input("Cantidad en stock: "))
                producto = Producto(nombre, categoria, stock)
                inventario.agregar_producto(producto)
            except ValueError:
                print("Por favor, ingrese un número válido para el stock.")

        elif opcion == "2": # Agregar producto electrónico
            nombre = input("Nombre del producto electrónico: ")
            categoria = input("Categoría del producto: ")
            try:
                stock = int(input("Cantidad en stock: "))
                garantia = int(input("Garantía (meses): "))
                producto = ProductoElectronico(nombre, categoria, stock, garantia)
                inventario.agregar_producto(producto)
            except ValueError:
                print("Por favor, ingrese valores válidos.")

        elif opcion == "3": # Eliminar Producto
            try:
                producto_id = int(input("ID del producto a eliminar: "))
                inventario.eliminar_producto(producto_id)
            except ValueError:
                print("Por favor, ingrese un ID válido.")

        elif opcion == "4": # Actualizar stock
            try:
                producto_id = int(input("ID del producto a actualizar: "))
                nuevo_stock = int(input("Nuevo stock: "))
                inventario.actualizar_stock(producto_id, nuevo_stock)
            except ValueError:
                print("Por favor, ingrese valores válidos.")

        elif opcion == "5": # Mostrar productos
            inventario.mostrar_productos()

        elif opcion == "6": # Salir de la Aplicación
            base_datos.cerrar_conexion()
            print("Saliendo del sistema. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida, intente de nuevo.")


# Punto de entrada
if __name__ == "__main__":
    main()
