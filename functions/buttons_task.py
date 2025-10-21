"""
Tarea: Interacciones con botones
URL: https://demoqa.com/buttons
Ejecutar Double Click, Right Click y Dynamic Click
"""
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from utils.selectors import BUTTON_SELECTORS
from utils.utils import wait_for_element, wait_for_clickable, take_screenshot
import time

logger = logging.getLogger(__name__)


def perform_double_click(driver):
    """
    Ejecuta doble click en el botón correspondiente
    
    Args:
        driver: WebDriver instance
    
    Returns:
        bool: True si la validación es exitosa
    """
    try:
        button = wait_for_clickable(driver, BUTTON_SELECTORS['double_click'])
        
        # Realizar doble click
        actions = ActionChains(driver)
        actions.double_click(button).perform()
        
        logger.info("Doble click ejecutado")
        time.sleep(0.5)
        
        # Validar mensaje
        message = wait_for_element(driver, BUTTON_SELECTORS['double_click_message'])
        expected_text = "You have done a double click"
        
        if expected_text in message.text:
            logger.info(f"✓ Mensaje de doble click validado: '{message.text}'")
            return True
        else:
            logger.warning(f"✗ Mensaje incorrecto: '{message.text}'")
            return False
            
    except Exception as e:
        logger.error(f"Error en doble click: {e}")
        take_screenshot(driver, 'double_click_error.png')
        raise


def perform_right_click(driver):
    """
    Ejecuta click derecho en el botón correspondiente
    
    Args:
        driver: WebDriver instance
    
    Returns:
        bool: True si la validación es exitosa
    """
    try:
        button = wait_for_clickable(driver, BUTTON_SELECTORS['right_click'])
        
        # Realizar click derecho
        actions = ActionChains(driver)
        actions.context_click(button).perform()
        time.sleep(1.5)  # Agregar espera
        
        logger.info("Click derecho ejecutado")
        time.sleep(0.5)
        
        # Validar mensaje
        message = wait_for_element(driver, BUTTON_SELECTORS['right_click_message'])
        expected_text = "You have done a right click"
        
        if expected_text in message.text:
            logger.info(f"✓ Mensaje de click derecho validado: '{message.text}'")
            return True
        else:
            logger.warning(f"✗ Mensaje incorrecto: '{message.text}'")
            return False
            
    except Exception as e:
        logger.error(f"Error en click derecho: {e}")
        take_screenshot(driver, 'right_click_error.png')
        raise


def perform_dynamic_click(driver):
    """
    Ejecuta click en el botón dinámico
    
    Args:
        driver: WebDriver instance
    
    Returns:
        bool: True si la validación es exitosa
    """
    try:
        # El botón dinámico usa XPath
        button = wait_for_clickable(
            driver, 
            BUTTON_SELECTORS['dynamic_click'], 
            by=By.XPATH
        )
        
        # Realizar click
        button.click()
        
        logger.info("Click dinámico ejecutado")
        time.sleep(0.5)
        
        # Validar mensaje
        message = wait_for_element(driver, BUTTON_SELECTORS['dynamic_click_message'])
        expected_text = "You have done a dynamic click"
        
        if expected_text in message.text:
            logger.info(f"✓ Mensaje de click dinámico validado: '{message.text}'")
            return True
        else:
            logger.warning(f"✗ Mensaje incorrecto: '{message.text}'")
            return False
            
    except Exception as e:
        logger.error(f"Error en click dinámico: {e}")
        take_screenshot(driver, 'dynamic_click_error.png')
        raise


def execute_buttons_task(driver):
    """
    Ejecuta la tarea completa de botones
    
    Args:
        driver: WebDriver instance
    """
    logger.info("=== Iniciando tarea: BUTTONS ===")
    
    driver.get('https://demoqa.com/buttons')
    logger.info("Navegando a Buttons")
    
    # Ejecutar las tres interacciones
    results = {
        'double_click': perform_double_click(driver),
        'right_click': perform_right_click(driver),
        'dynamic_click': perform_dynamic_click(driver)
    }
    
    # Verificar resultados
    all_passed = all(results.values())
    
    if all_passed:
        logger.info("✓ Tarea de botones completada exitosamente")
    else:
        failed = [k for k, v in results.items() if not v]
        logger.warning(f"⚠ Algunas validaciones fallaron: {failed}")
    
    return all_passed