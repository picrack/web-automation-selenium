"""
Módulo de conexión y operaciones con MySQL
Uso de PyMySQL sin ORM con consultas parametrizadas
"""
import pymysql
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)


def get_connection():
    """
    Crea y retorna una conexión a MySQL
    """
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )
        logger.info("Conexión a MySQL establecida exitosamente")
        return connection
    except pymysql.Error as e:
        logger.error(f"Error al conectar a MySQL: {e}")
        raise


def insert_employee(first_name, last_name, age, email, salary, department):
    """
    Inserta un empleado en la base de datos
    Evita duplicados usando ON DUPLICATE KEY UPDATE
    
    Args:
        first_name (str): Nombre
        last_name (str): Apellido
        age (int): Edad
        email (str): Email (clave única)
        salary (float): Salario
        department (str): Departamento
    
    Returns:
        int: ID del registro insertado o actualizado
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        # Consulta parametrizada con prevención de duplicados
        query = """
            INSERT INTO employees (first_name, last_name, age, email, salary, department)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                first_name = VALUES(first_name),
                last_name = VALUES(last_name),
                age = VALUES(age),
                salary = VALUES(salary),
                department = VALUES(department)
        """
        
        cursor.execute(query, (first_name, last_name, age, email, salary, department))
        connection.commit()
        
        employee_id = cursor.lastrowid
        logger.info(f"Empleado insertado/actualizado - Email: {email}, ID: {employee_id}")
        
        return employee_id
        
    except pymysql.Error as e:
        if connection:
            connection.rollback()
        logger.error(f"Error al insertar empleado: {e}")
        raise
    finally:
        if connection:
            connection.close()


def get_employee_by_email(email):
    """
    Obtiene un empleado por su email
    
    Args:
        email (str): Email del empleado
    
    Returns:
        dict: Datos del empleado o None si no existe
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        query = "SELECT * FROM employees WHERE email = %s"
        cursor.execute(query, (email,))
        
        result = cursor.fetchone()
        return result
        
    except pymysql.Error as e:
        logger.error(f"Error al consultar empleado: {e}")
        raise
    finally:
        if connection:
            connection.close()


def get_all_employees():
    """
    Obtiene todos los empleados
    
    Returns:
        list: Lista de empleados
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        
        query = "SELECT * FROM employees ORDER BY id"
        cursor.execute(query)
        
        results = cursor.fetchall()
        logger.info(f"Se obtuvieron {len(results)} empleados")
        return results
        
    except pymysql.Error as e:
        logger.error(f"Error al consultar empleados: {e}")
        raise
    finally:
        if connection:
            connection.close()


def test_connection():
    """
    Prueba la conexión a la base de datos
    
    Returns:
        bool: True si la conexión es exitosa
    """
    connection = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        logger.error(f"Error en test de conexión: {e}")
        return False
    finally:
        if connection:
            connection.close()