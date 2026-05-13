import mysql.connector
from mysql.connector import Error
from pathlib import Path
import os

env_path = Path(r'C:\Users\fcoan\Documents\TALLER DE BASES DE DATOS\.env')

# Leer el archivo con utf-16 y limpiar caracteres especiales
try:
    with open(env_path, 'r', encoding='utf-16') as f:
        content = f.read()
    
    # Procesar línea por línea
    for line in content.split('\n'):
        line = line.strip()
        # Eliminar caracteres especiales (BOM, etc)
        line = line.replace('\ufeff', '').replace('\r', '')
        
        # Separar key-value en 2 variables para mayor claridad
        if line and not line.startswith('#'):
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                os.environ[key] = value
    
    print("Variables de entorno cargadas correctamente.\n")
except Exception as e:
    print(f"Error al leer el archivo .env: {e}")
    exit()

# Conectar a la base de datos utilizando las variables de entorno cargadas
try:
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=3306,
        use_pure=True
    )

    # Si la conexión es exitosa, mostrar información del servidor y de la base de datos
    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Conectado al servidor MySQL versión ", db_info)
        
        # Obtener la base de datos actual
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Conectado a la base de datos: ", record)
        
        # Menu de opciones
        while True:
            print("\n--- Menú de opciones ---")
            print("1. Insertar un nuevo paciente")
            print("2. Eliminar un paciente")
            print ("3. Mostrar todos los pacientes")
            print ("4. Modificar un paciente")
            print("5. Salir")
            opcion = input("Seleccione una opción: ").strip()
            
            # Agregar un nuevo paciente
            if opcion == '1':
                nombre = input("Ingrese el nombre del paciente: ").strip()
                if not nombre:
                    print("El nombre no puede estar vacío.")
                    continue
                
                telefono = input("Ingrese el teléfono del paciente: ").strip()
                # Validar numero de telefono
                if not telefono.isdigit() or len(telefono) < 7:
                    print("El teléfono debe contener solo numeros y al menos 7 dígitos.")
                    continue
                
                # Tratar de insertar en la base de datos
                try:
                    cursor.execute("INSERT INTO paciente (nombre, telefono) VALUES (%s, %s)", 
                                   (nombre, telefono))
                    connection.commit()
                    print("Paciente insertado correctamente.")
                except Error as e:
                    connection.rollback()
                    print(f"Error al insertar paciente: {e}")
                    
                # Eliminar paciente
            elif opcion == '2':
                try:
                    paciente_id = input("Ingrese el ID del paciente a eliminar: ").strip()
                    # Validar que el ID sea un numero
                    if not paciente_id.isdigit():
                        print("El ID debe ser un número.")
                        continue

                    # Tratar de eliminar al paciente con su ID
                    cursor.execute("DELETE FROM paciente WHERE id = %s", (paciente_id,))
                    connection.commit()
                    print("Paciente eliminado correctamente.")

                except Error as e:
                    print(f"Error al tratar de eliminar el paciente: {e}")        

            # Mostrar todos los pacientes
            elif opcion == '3':
                try:
                    cursor.execute("SELECT * FROM paciente")
                    pacientes = cursor.fetchall()
                    if pacientes:
                        print("\n--- Lista de pacientes ---")
                        for paciente in pacientes:
                            print(paciente)
                    else:
                        print("No hay pacientes registrados.")
                except Error as e:
                    print(f"Error al consultar pacientes: {e}")

            # Modificar un paciente
            elif opcion == '4':
                try:
                    paciente_id = input("Ingrese el ID del paciente a modificar: ").strip()
                    # Validar que el ID sea un numero
                    if not paciente_id.isdigit():
                            print("El ID debe ser un número.")
                            continue

                    # Solicitar los nuevos VALUES para el paciente
                    nuevo_nombre = input("Ingrese el nuevo nombre del paciente: ").strip()
                    if not nuevo_nombre:
                            print("El nombre no puede estar vacío.")
                            continue

                    nuevo_telefono = input("Ingrese el nuevo teléfono del paciente: ").strip()
                    if not nuevo_telefono.isdigit() or len(nuevo_telefono) < 7:
                            print("El teléfono debe contener solo números y al menos 7 dígitos.")
                            continue

                    # Actualizar los valores del paciente
                    cursor.execute("UPDATE paciente SET nombre = %s, telefono = %s WHERE id = %s", 
                                  (nuevo_nombre, nuevo_telefono, paciente_id))
                    connection.commit()
                    print("Paciente modificado correctamente.")
                except Error as e:
                                print(f"Error al modificar el paciente: {e}")
                    
            # Salir del programa
            elif opcion == '5':
                print("Saliendo del programa.")
                break
            #Default para opciones no válidas
            else:
                print("Opción no válida. Por favor, intente de nuevo.")
                
        # Cerrar cursor y conexión
        cursor.close()
        connection.close()
        print("Conexión cerrada.")

except Error as e:
    print("Error durante la conexión a MySQL:", e)