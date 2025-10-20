-- Datos de prueba opcionales para la tabla employees
-- Este archivo es opcional y se usa solo para testing

-- Limpiar datos existentes (opcional)
-- TRUNCATE TABLE employees;

-- Insertar datos de ejemplo
INSERT INTO employees (first_name, last_name, age, email, salary, department) 
VALUES 
    ('Cierra', 'Vega', 39, 'cierra@example.com', 10000, 'Insurance'),
    ('Alden', 'Cantrell', 45, 'alden@example.com', 12000, 'Compliance'),
    ('Kierra', 'Gentry', 29, 'kierra@example.com', 2000, 'Legal')
ON DUPLICATE KEY UPDATE 
    first_name = VALUES(first_name),
    last_name = VALUES(last_name),
    age = VALUES(age),
    salary = VALUES(salary),
    department = VALUES(department);

-- Verificar inserción
SELECT * FROM employees;