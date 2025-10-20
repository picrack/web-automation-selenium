"""
Tarea: Drag & Drop
URL: https://demoqa.com/droppable
Arrastrar elemento y validar estado "Dropped!"
"""
import logging
from selenium.webdriver import ActionChains
from utils.selectors import DROPPABLE_SELECTORS
from utils.utils import wait_for_element, take_screenshot
import time

logger = logging.getLogger(__name__)


def perform_drag_and_drop(driver):
    """
    Realiza la acción de drag & drop
    
    Args:
        driver: WebDriver instance
    
    Returns:
        bool: True si la validación es exitosa
    """
    try:
        driver.get('https://demoqa.com/droppable')
        logger.info("Navegando a Droppable")
        
        # Esperar que los elementos estén disponibles
        draggable = wait_for_element(driver, DROPPABLE_SELECTORS['draggable'])
        droppable = wait_for_element(driver, DROPPABLE_SELECTORS['droppable'])
        
        # Obtener texto inicial
        initial_text = droppable.text
        logger.info(f"Texto inicial del área de drop: '{initial_text}'")
        
        # Realizar drag & drop (método alternativo para Firefox)
        actions = ActionChains(driver)
        actions.click_and_hold(draggable).pause(0.5).move_to_element(droppable).pause(0.5).release().perform()
        
        logger.info("Drag & Drop ejecutado")
        time.sleep(1)
        
        # Validar el cambio de estado
        droppable_text_element = wait_for_element(driver, DROPPABLE_SELECTORS['droppable_text'])
        final_text = droppable_text_element.text
        
        expected_text = "Dropped!"
        
        if expected_text in final_text:
            logger.info(f"✓ Validación exitosa - Texto cambió a: '{final_text}'")
            return True
        else:
            logger.warning(f"✗ Validación fallida - Texto esperado: '{expected_text}', obtenido: '{final_text}'")
            return False
            
    except Exception as e:
        logger.error(f"Error en drag & drop: {e}")
        take_screenshot(driver, 'droppable_error.png')
        raise


def execute_droppable_task(driver):
    """
    Ejecuta la tarea completa de droppable
    
    Args:
        driver: WebDriver instance
    """
    logger.info("=== Iniciando tarea: DROPPABLE ===")
    
    result = perform_drag_and_drop(driver)
    
    if result:
        logger.info("✓ Tarea de Drag & Drop completada exitosamente")
    else:
        logger.warning("⚠ Tarea de Drag & Drop completada con advertencias")
    
    return result