"""
Tarea: Completar y validar formulario de práctica
URL: https://demoqa.com/automation-practice-form
"""
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from utils.selectors import FORM_SELECTORS
from utils.utils import (
    wait_for_element, 
    wait_for_clickable, 
    scroll_to_element,
    create_test_image,
    take_screenshot
)

logger = logging.getLogger(__name__)


def fill_form(driver):
    """
    Completa todos los campos del formulario
    
    Args:
        driver: WebDriver instance
    
    Returns:
        dict: Datos enviados para validación
    """
    try:
        driver.get('https://demoqa.com/automation-practice-form')
        logger.info("Navegando a formulario de práctica")
        
        # Datos de prueba
        form_data = {
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'email': 'juan.perez@example.com',
            'gender': 'Male',
            'mobile': '1234567890',
            'date_of_birth': '15 Oct 1990',
            'subjects': ['Maths', 'Physics'],
            'hobbies': ['Sports', 'Reading'],
            'current_address': 'Calle Principal 123, Ciudad',
            'state': 'NCR',
            'city': 'Delhi'
        }
        
        # First Name
        first_name_input = wait_for_element(driver, FORM_SELECTORS['first_name'])
        first_name_input.send_keys(form_data['first_name'])
        
        # Last Name
        last_name_input = wait_for_element(driver, FORM_SELECTORS['last_name'])
        last_name_input.send_keys(form_data['last_name'])
        
        # Email
        email_input = wait_for_element(driver, FORM_SELECTORS['email'])
        email_input.send_keys(form_data['email'])
        
        # Gender - Male
        gender_radio = wait_for_clickable(driver, FORM_SELECTORS['gender_male'])
        scroll_to_element(driver, gender_radio)
        time.sleep(0.5)
        scroll_to_element(driver, gender_radio)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", gender_radio)
        
        # Mobile
        mobile_input = wait_for_element(driver, FORM_SELECTORS['mobile'])
        mobile_input.send_keys(form_data['mobile'])
        
        # Date of Birth
        dob_input = wait_for_clickable(driver, FORM_SELECTORS['date_of_birth'])
        scroll_to_element(driver, dob_input)
        dob_input.click()
        dob_input.send_keys(Keys.CONTROL + "a")
        dob_input.send_keys(form_data['date_of_birth'])
        dob_input.send_keys(Keys.ENTER)
        
        # Subjects
        subjects_input = wait_for_element(driver, FORM_SELECTORS['subjects'])
        scroll_to_element(driver, subjects_input)
        for subject in form_data['subjects']:
            subjects_input.send_keys(subject)
            time.sleep(0.5)
            subjects_input.send_keys(Keys.ENTER)
        
        # Hobbies
        hobbies_checkbox = wait_for_clickable(driver, FORM_SELECTORS['hobbies_sports'])
        scroll_to_element(driver, hobbies_checkbox)
        hobbies_checkbox.click()
        
        reading_checkbox = wait_for_clickable(driver, FORM_SELECTORS['hobbies_reading'])
        reading_checkbox.click()
        
        # Picture Upload
        picture_input = driver.find_element(By.CSS_SELECTOR, FORM_SELECTORS['picture'])
        image_path = create_test_image()
        picture_input.send_keys(image_path)
        logger.info(f"Imagen cargada: {image_path}")
        
        # Current Address
        address_input = wait_for_element(driver, FORM_SELECTORS['current_address'])
        scroll_to_element(driver, address_input)
        address_input.send_keys(form_data['current_address'])
        
        # State - NCR
        state_dropdown = wait_for_clickable(driver, FORM_SELECTORS['state'])
        scroll_to_element(driver, state_dropdown)
        state_dropdown.click()
        time.sleep(0.5)
        state_option = wait_for_clickable(driver, FORM_SELECTORS['state_option'])
        state_option.click()
        
        # City - Delhi
        city_dropdown = wait_for_clickable(driver, FORM_SELECTORS['city'])
        city_dropdown.click()
        time.sleep(0.5)
        city_option = wait_for_clickable(driver, FORM_SELECTORS['city_option'])
        city_option.click()
        
        # Submit
        submit_button = wait_for_clickable(driver, FORM_SELECTORS['submit'])
        scroll_to_element(driver, submit_button)
        submit_button.click()
        
        logger.info("Formulario enviado exitosamente")
        return form_data
        
    except Exception as e:
        logger.error(f"Error al completar formulario: {e}")
        take_screenshot(driver, 'form_error.png')
        raise


def validate_modal(driver, form_data):
    """
    Valida el modal de confirmación
    Compara los datos enviados con los mostrados
    
    Args:
        driver: WebDriver instance
        form_data (dict): Datos enviados en el formulario
    
    Returns:
        bool: True si la validación es exitosa
    """
    try:
        # Esperar modal
        modal_title = wait_for_element(driver, FORM_SELECTORS['modal_title'], timeout=10)
        assert 'Thanks for submitting the form' in modal_title.text
        logger.info("Modal de confirmación detectado")
        
        # Obtener contenido del modal
        modal_body = wait_for_element(driver, FORM_SELECTORS['modal_content'])
        modal_text = modal_body.text
        
        # Validaciones
        validations = {
            'Student Name': f"{form_data['first_name']} {form_data['last_name']}",
            'Student Email': form_data['email'],
            'Gender': form_data['gender'],
            'Mobile': form_data['mobile'],
            'Subjects': ', '.join(form_data['subjects']),
            'Hobbies': ', '.join(form_data['hobbies']),
            'Address': form_data['current_address'],
            'State and City': f"{form_data['state']} {form_data['city']}"
        }
        
        all_valid = True
        for label, expected_value in validations.items():
            if expected_value in modal_text:
                logger.info(f"✓ Validación exitosa - {label}: {expected_value}")
            else:
                logger.warning(f"✗ Validación fallida - {label}: esperado '{expected_value}'")
                all_valid = False
        
        # Cerrar modal
        close_button = wait_for_clickable(driver, FORM_SELECTORS['close_modal'])
        close_button.click()
        
        return all_valid
        
    except Exception as e:
        logger.error(f"Error al validar modal: {e}")
        take_screenshot(driver, 'modal_validation_error.png')
        raise


def execute_form_task(driver):
    """
    Ejecuta la tarea completa del formulario
    
    Args:
        driver: WebDriver instance
    """
    logger.info("=== Iniciando tarea: FORMULARIO ===")
    form_data = fill_form(driver)
    time.sleep(2)  # Esperar que el modal aparezca
    validation_result = validate_modal(driver, form_data)
    
    if validation_result:
        logger.info("✓ Tarea de formulario completada exitosamente")
    else:
        logger.warning("⚠ Tarea de formulario completada con advertencias")
    
    return validation_result