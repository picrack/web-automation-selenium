"""
Script de prueba para función retry_on_failure
"""
import logging
from utils.utils import retry_on_failure

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Test 1: Función que falla 2 veces y luego funciona
print("\n=== TEST 1: Función que falla 2 veces ===")
attempt_count = 0

def flaky_function():
    global attempt_count
    attempt_count += 1
    if attempt_count < 3:
        raise Exception(f"Fallo simulado (intento {attempt_count})")
    return "¡Éxito!"

try:
    result = retry_on_failure(flaky_function, max_retries=5, delay=1)
    print(f"✓ Resultado: {result}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Función que siempre falla
print("\n=== TEST 2: Función que siempre falla ===")

def always_fails():
    raise Exception("Esta función siempre falla")

try:
    result = retry_on_failure(always_fails, max_retries=3, delay=1)
    print(f"✓ Resultado: {result}")
except Exception as e:
    print(f"✗ Error final después de todos los intentos: {e}")

# Test 3: Función que funciona siempre
print("\n=== TEST 3: Función que funciona primera vez ===")

def always_works():
    return "Funcionó de inmediato"

try:
    result = retry_on_failure(always_works, max_retries=3, delay=1)
    print(f"✓ Resultado: {result}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n=== Todos los tests completados ===")