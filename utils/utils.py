"""
Funciones auxiliares y utilidades comunes
Esperas, validaciones y helpers
"""
import logging
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)


def wait_for_element(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    """
    Espera explícita hasta que un elemento sea visible
    
    Args:
        driver: WebDriver instance
        selector (str): Selector del elemento
        by: Tipo de selector (By.CSS_SELECTOR, By.XPATH, etc.)
        timeout (int): Tiempo máximo de espera
    
    Returns:
        WebElement: Elemento encontrado
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, selector))
        )
        return element
    except TimeoutException:
        logger.error(f"Timeout esperando elemento: {selector}")
        raise


def wait_for_clickable(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    """
    Espera explícita hasta que un elemento sea clickeable
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, selector))
        )
        return element
    except TimeoutException:
        logger.error(f"Timeout esperando elemento clickeable: {selector}")
        raise


def scroll_to_element(driver, element):
    """
    Hace scroll hasta un elemento
    """
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)


def create_test_image(filename='test_image.png'):
    """
    Crea una imagen de prueba simple para el formulario
    
    Returns:
        str: Path absoluto de la imagen
    """
    try:
        from PIL import Image
        
        img = Image.new('RGB', (100, 100), color='blue')
        img_path = os.path.join(os.getcwd(), filename)
        img.save(img_path)
        logger.info(f"Imagen de prueba creada: {img_path}")
        return img_path
    except ImportError:
        # Si PIL no está disponible, crear un archivo simple
        img_path = os.path.join(os.getcwd(), filename)
        # Crear un PNG mínimo válido
        with open(img_path, 'wb') as f:
            # Header PNG mínimo
            f.write(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')
        logger.info(f"Imagen mínima creada: {img_path}")
        return img_path


def setup_logging(level=logging.INFO):
    """
    Configura el sistema de logging
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def take_screenshot(driver, filename='error_screenshot.png'):
    """
    Toma una captura de pantalla
    
    Args:
        driver: WebDriver instance
        filename (str): Nombre del archivo
    """
    try:
        filepath = os.path.join(os.getcwd(), filename)
        driver.save_screenshot(filepath)
        logger.info(f"Screenshot guardado: {filepath}")
    except Exception as e:
        logger.error(f"Error al tomar screenshot: {e}")