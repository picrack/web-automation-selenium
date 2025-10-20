"""
Tarea: Extraer registros de WebTables y guardar en MySQL
URL: https://demoqa.com/webtables
Extrae solo registro 1 y 3 (ignora el 2)
"""
import logging
from selenium.webdriver.common.by import By
from utils.selectors import WEBTABLE_SELECTORS
from utils.utils import wait_for_element, take_screenshot
from app.db import insert_employee, get_all_employees

logger = logging.getLogger(__name__)


def extract_row_data(row):
    """
    Extrae los datos de una fila de la tabla
    
    Args:
        row: WebElement de la fila
    
    Returns:
        dict: Datos de la fila o None si está vacía
    """
    try:
        first_name = row.find_element(By.CSS_SELECTOR, WEBTABLE_SELECTORS['first_name']).text.strip()
        
        # Si la fila está vacía, retornar None
        if not first_name:
            return None
        
        last_name = row.find_element(By.CSS_SELECTOR, WEBTABLE_SELECTORS['last_name']).text.strip()
        age = row.find_element(By.CSS_SELECTOR, WEBTABLE_SELECTORS['age']).text.strip()
        email = row.find_element(By.CSS_SELECTOR, WEBTABLE_SELECTORS['email']).text.strip()
        salary = row.find_element(By.CSS_SELECTOR, WEBTABLE_SELECTORS['salary']).text.strip()
        department = row.find_element(By.CSS_SELECTOR, WEBTABLE_SELECTORS['department']).text.strip()
        
        return {
            'first_name': first_name,
            'last_name': last_name,
            'age': int(age) if age else 0,
            'email': email,
            'salary': float(salary) if salary else 0.0,
            'department': department
        }
    except Exception as e:
        logger.warning(f"Error extrayendo datos de fila: {e}")
        return None


def extract_webtables(driver):
    """
    Extrae el registro 1 y 3 de la tabla (ignora el 2)
    
    Args:
        driver: WebDriver instance
    
    Returns:
        list: Lista con los datos extraídos
    """
    try:
        driver.get('https://demoqa.com/webtables')
        logger.info("Navegando a WebTables")
        
        # Esperar que la tabla esté visible
        wait_for_element(driver, WEBTABLE_SELECTORS['table'])
        
        # Obtener todas las filas
        rows = driver.find_elements(By.CSS_SELECTOR, WEBTABLE_SELECTORS['rows'])
        logger.info(f"Se encontraron {len(rows)} filas en la tabla")
        
        extracted_data = []
        
        # Extraer solo registro 1 y 3 (índices 0 y 2)
        target_indices = [0, 2]
        
        for index in target_indices:
            if index < len(rows):
                row_data = extract_row_data(rows[index])
                if row_data:
                    extracted_data.append(row_data)
                    logger.info(f"✓ Registro {index + 1} extraído: {row_data['email']}")
                else:
                    logger.warning(f"Registro {index + 1} está vacío")
        
        logger.info(f"Total de registros extraídos: {len(extracted_data)}")
        return extracted_data
        
    except Exception as e:
        logger.error(f"Error al extraer datos de WebTables: {e}")
        take_screenshot(driver, 'webtables_error.png')
        raise


def save_to_database(data_list):
    """
    Guarda los datos extraídos en MySQL
    
    Args:
        data_list (list): Lista de diccionarios con datos de empleados
    
    Returns:
        int: Cantidad de registros insertados
    """
    inserted_count = 0
    
    for data in data_list:
        try:
            insert_employee(
                first_name=data['first_name'],
                last_name=data['last_name'],
                age=data['age'],
                email=data['email'],
                salary=data['salary'],
                department=data['department']
            )
            inserted_count += 1
            logger.info(f"✓ Empleado guardado en BD: {data['email']}")
            
        except Exception as e:
            logger.error(f"Error al guardar empleado {data['email']}: {e}")
    
    return inserted_count


def execute_webtables_task(driver):
    """
    Ejecuta la tarea completa de WebTables
    
    Args:
        driver: WebDriver instance
    """
    logger.info("=== Iniciando tarea: WEBTABLES ===")
    
    # Extraer datos
    extracted_data = extract_webtables(driver)
    
    if not extracted_data:
        logger.warning("No se extrajeron datos de la tabla")
        return False
    
    # Guardar en base de datos
    inserted_count = save_to_database(extracted_data)
    
    logger.info(f"✓ Tarea WebTables completada: {inserted_count} registros guardados")
    
    # Mostrar registros en BD
    all_employees = get_all_employees()
    logger.info(f"Total de empleados en BD: {len(all_employees)}")
    
    return True