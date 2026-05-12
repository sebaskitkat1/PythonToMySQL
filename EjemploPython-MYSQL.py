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

try:
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=3306,
        use_pure=True
    )
    
    if connection.is_connected():
        db_info = connection.get_server_info()
        print("Conectado al servidor MySQL versión ", db_info)
        
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Conectado a la base de datos: ", record)
        
        while True:
            print("\n--- Menú de opciones ---")
            print("1. Insertar un nuevo paciente")
            print("2. Mostrar todos los pacientes")
            print("3. Salir")
            opcion = input("Seleccione una opción: ").strip()
            
            if opcion == '1':
                nombre = input("Ingrese el nombre del paciente: ").strip()
                if not nombre:
                    print("El nombre no puede estar vacío.")
                    continue
                
                telefono = input("Ingrese el teléfono del paciente: ").strip()
                if not telefono.isdigit() or len(telefono) < 7:
                    print("El teléfono debe contener solo números y al menos 7 dígitos.")
                    continue
                
                try:
                    cursor.execute("INSERT INTO paciente (nombre, telefono) VALUES (%s, %s)", 
                                   (nombre, telefono))
                    connection.commit()
                    print("Paciente insertado correctamente.")
                except Error as e:
                    connection.rollback()
                    print(f"Error al insertar paciente: {e}")
                    
            elif opcion == '2':
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
                    
            elif opcion == '3':
                print("Saliendo del programa.")
                break
            else:
                print("Opción no válida. Por favor, intente de nuevo.")
                print("Por favor intente con las opciones disponibles: 1, 2, 3.")
        cursor.close()
        connection.close()
        print("Conexión cerrada.")

except Error as e:
    print("Error durante la conexión a MySQL:", e)