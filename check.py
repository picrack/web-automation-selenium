"""
Script de verificación de entorno
Valida conexión a BD, driver de Chrome, y dependencias
"""
import sys
import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from app.db import test_connection
from dotenv import load_dotenv
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_environment():
    """
    Verifica las variables de entorno
    """
    logger.info("=== Verificando variables de entorno ===")
    load_dotenv()
    
    required_vars = ['DB_HOST', 'DB_USER', 'DB_PASSWORD', 'DB_NAME']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            logger.info(f"✓ {var}: configurado")
        else:
            logger.error(f"✗ {var}: NO configurado")
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Faltan variables de entorno: {missing_vars}")
        logger.info("Copia .env.example a .env y configura las variables")
        return False
    
    return True


def check_database_connection():
    """
    Verifica la conexión a MySQL
    """
    logger.info("\n=== Verificando conexión a MySQL ===")
    try:
        if test_connection():
            logger.info("✓ Conexión a MySQL exitosa")
            return True
        else:
            logger.error("✗ No se pudo conectar a MySQL")
            return False
    except Exception as e:
        logger.error(f"✗ Error al conectar a MySQL: {e}")
        logger.info("Verifica que MySQL esté corriendo y las credenciales sean correctas")
        return False


def check_firefox_driver():
    """
    Verifica que el driver de Firefox funcione
    """
    logger.info("\n=== Verificando Firefox WebDriver ===")
    driver = None
    try:
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        
        service = Service(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        
        driver.get('https://www.google.com')
        logger.info("✓ Firefox WebDriver funciona correctamente")
        return True
        
    except Exception as e:
        logger.error(f"✗ Error con Chrome WebDriver: {e}")
        return False
    finally:
        if driver:
            driver.quit()


def check_python_version():
    """
    Verifica la versión de Python
    """
    logger.info("=== Verificando versión de Python ===")
    version = sys.version_info
    logger.info(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 9:
        logger.info("✓ Versión de Python compatible (3.9+)")
        return True
    else:
        logger.warning("⚠ Se recomienda Python 3.9 o superior")
        return False


def check_dependencies():
    """
    Verifica que las dependencias estén instaladas
    """
    logger.info("\n=== Verificando dependencias ===")
    dependencies = {
        'selenium': 'selenium',
        'webdriver_manager': 'webdriver-manager',
        'pymysql': 'PyMySQL',
        'dotenv': 'python-dotenv'
    }
    
    all_installed = True
    for module, package_name in dependencies.items():
        try:
            __import__(module)
            logger.info(f"✓ {package_name}: instalado")
        except ImportError:
            logger.error(f"✗ {package_name}: NO instalado")
            all_installed = False
    
    if not all_installed:
        logger.info("\nInstala las dependencias con:")
        logger.info("pip install -r requirements.txt")
        return False
    
    return True


def main():
    """
    Ejecuta todas las verificaciones
    """
    logger.info("="*60)
    logger.info("ENVIRONMENT VERIFICATION - RPA SYSTEM")
    logger.info("="*60)
    
    checks = {
    'Python': check_python_version(),
    'Dependencias': check_dependencies(),
    'Variables de entorno': check_environment(),
    'Base de datos': check_database_connection(),
    'Firefox Driver': check_firefox_driver()
}
    
    logger.info("\n" + "="*60)
    logger.info("RESUMEN DE VERIFICACIONES")
    logger.info("="*60)
    
    for check_name, result in checks.items():
        status = "✓ OK" if result else "✗ FALLÓ"
        logger.info(f"{check_name}: {status}")
    
    all_passed = all(checks.values())
    
    if all_passed:
        logger.info("\n✓ ¡Todas las verificaciones pasaron exitosamente!")
        logger.info("El entorno está listo para ejecutar las tareas.")
        logger.info("\nEjecuta: python main.py --task all")
        return 0
    else:
        logger.error("\n✗ Algunas verificaciones fallaron.")
        logger.error("Revisa los errores anteriores y corrígelos antes de continuar.")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)