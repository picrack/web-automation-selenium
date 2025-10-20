"""
Orquestador principal - CLI
Ejecuta las tareas de automatización RPA
"""
import argparse
import logging
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from dotenv import load_dotenv

from functions.form_task import execute_form_task
from functions.webtables_task import execute_webtables_task
from functions.buttons_task import execute_buttons_task
from functions.droppable_task import execute_droppable_task
from utils.utils import setup_logging

# Cargar variables de entorno
load_dotenv()

# Configurar logging
setup_logging()
logger = logging.getLogger(__name__)


def create_driver(headless=False):
    """
    Crea y configura el WebDriver de Firefox
    
    Args:
        headless (bool): Si True, ejecuta en modo headless
    
    Returns:
        WebDriver: Instancia configurada de Firefox WebDriver
    """
    options = webdriver.FirefoxOptions()
    
    if headless:
        options.add_argument('--headless')
    
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    
    # Establecer timeouts
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(30)
    
    return driver


def execute_task(task_name, headless=False):
    """
    Ejecuta una tarea específica
    
    Args:
        task_name (str): Nombre de la tarea a ejecutar
        headless (bool): Modo headless
    """
    driver = None
    try:
        driver = create_driver(headless)
        logger.info(f"WebDriver iniciado correctamente")
        
        if task_name == 'form':
            execute_form_task(driver)
        elif task_name == 'webtables':
            execute_webtables_task(driver)
        elif task_name == 'buttons':
            execute_buttons_task(driver)
        elif task_name == 'droppable':
            execute_droppable_task(driver)
        elif task_name == 'all':
            execute_all_tasks(driver)
        else:
            logger.error(f"Tarea desconocida: {task_name}")
            
    except Exception as e:
        logger.error(f"Error ejecutando tarea '{task_name}': {e}")
        raise
    finally:
        if driver:
            driver.quit()
            logger.info("WebDriver cerrado")


def execute_all_tasks(driver):
    """
    Ejecuta todas las tareas en secuencia
    
    Args:
        driver: WebDriver instance
    """
    logger.info("\n" + "="*60)
    logger.info("EJECUTANDO TODAS LAS TAREAS")
    logger.info("="*60 + "\n")
    
    tasks = [
        ('Formulario', execute_form_task),
        ('WebTables', execute_webtables_task),
        ('Buttons', execute_buttons_task),
        ('Droppable', execute_droppable_task)
    ]
    
    results = {}
    
    for task_name, task_function in tasks:
        try:
            logger.info(f"\n>>> Ejecutando: {task_name}")
            result = task_function(driver)
            results[task_name] = result
            logger.info(f"<<< {task_name}: {'✓ COMPLETADO' if result else '⚠ COMPLETADO CON ADVERTENCIAS'}\n")
        except Exception as e:
            logger.error(f"<<< {task_name}: ✗ ERROR - {e}\n")
            results[task_name] = False
    
    # Resumen final
    logger.info("\n" + "="*60)
    logger.info("RESUMEN DE EJECUCIÓN")
    logger.info("="*60)
    
    for task_name, result in results.items():
        status = "✓ EXITOSO" if result else "✗ FALLÓ"
        logger.info(f"{task_name}: {status}")
    
    success_count = sum(1 for r in results.values() if r)
    total_count = len(results)
    
    logger.info(f"\nTareas exitosas: {success_count}/{total_count}")
    logger.info("="*60)


def main():
    """
    Función principal del CLI
    """
    parser = argparse.ArgumentParser(
        description='Automatización RPA - Personal Project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py --task all              # Ejecuta todas las tareas
  python main.py --task form             # Solo formulario
  python main.py --task webtables        # Solo WebTables
  python main.py --task buttons          # Solo botones
  python main.py --task droppable        # Solo Drag & Drop
  python main.py --task all --headless   # Todas en modo headless
        """
    )
    
    parser.add_argument(
        '--task',
        type=str,
        required=True,
        choices=['form', 'webtables', 'buttons', 'droppable', 'all'],
        help='Tarea a ejecutar'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Ejecutar en modo headless (sin interfaz gráfica)'
    )
    
    args = parser.parse_args()
    
    logger.info("="*60)
    logger.info("WEB AUTOMATION SYSTEM - RPA")
    logger.info("="*60)
    logger.info(f"Tarea seleccionada: {args.task}")
    logger.info(f"Modo headless: {'Sí' if args.headless else 'No'}")
    logger.info("="*60 + "\n")
    
    try:
        execute_task(args.task, args.headless)
        logger.info("\n✓ Ejecución completada exitosamente")
    except Exception as e:
        logger.error(f"\n✗ Ejecución falló: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())