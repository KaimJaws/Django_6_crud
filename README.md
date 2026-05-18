# Django 6 CRUD Example + Bootstrap 5

The following is an example of CRUD (Create, Read, Update, Delete) in Django 6.

There are 2 CRUD applications, one uses function-based views (FBV) and the other
uses class-based views (CBV).

## Requirements:
```
Django==6.0.2
Python>=3.12
```

## Run the following commands in sequence to deploy the project to a development environment:

```bash
Creating a Python 3 virtual environment:

1. Update the package list:

$ sudo apt update

2. Install python3-venv

$ sudo apt install python3-venv

3. Create the virtual environment:

$ python3 -m venv my_environment

4. Activate the environment:

$ source my_environment/bin/activate
```

Now install de Requirements

```bash
$ pip install -r requirements.txt

$ cp Django_6_crud/settings.py_example Django_6_crud/settings.py

$ python manage.py makemigrations person product

$ python manage.py migrate

$ python manage.py runserver
```

## Test the project:

Open your browser to http://127.0.0.1:8000 and you'll see the Django 6 CRUD
application for managing people records.

## Image

![1.png](1.png "1.png")

![2.png](2.png "2.png")

![3.png](3.png "3.png")

![4.png](4.png "4.png")

## Comandos Interactivos de Administración

### Concepto General y Objetivos

Un Comando de Administración Personalizado en Django es un script de Python que se crea dentro de las aplicaciones para extender las capacidades de la interfaz de línea de comandos de Django (`manage.py`). Al heredar de la clase base `BaseCommand`, se integra directamente con el ecosistema del framework, dándote acceso nativo al ORM, configuraciones y utilidades de la consola.

Cuando a este script le añades el apellido de "Interactivo", significa que el comando no se limita a ejecutar una tarea en segundo plano de forma lineal, sino que establece un diálogo bidireccional con el desarrollador o administrador del sistema a través de la terminal en tiempo de ejecución.

Un comando de administración interactivo se caracteriza técnicamente por implementar los siguientes comportamientos:

    - Pausas de Ejecución (Captura de Inputs): Detiene el flujo del script utilizando funciones como `input()` para solicitar parámetros dinámicos directamente en la consola.

    - Validación en Tiempo Real: Analiza las respuestas introducidas por el usuario en la terminal y, si rompen alguna regla de negocio, interrumpe el proceso de forma segura devolviendo excepciones controladas (`CommandError`) sin llegar a tocar la base de datos.

    - Mecanismos de Confirmación (Gatekeeping): Antes de ejecutar operaciones críticas, destructivas o masivas (como un `.update()` o un `.delete()`), muestra advertencias detalladas del impacto y exige una confirmación explícita (ej. `[s/n]`) para proceder o abortar la operación.

    - Salidas Formateadas con Estilo: Utiliza canales estandarizados como `self.stdout` y `self.stderr` junto con buffers de estilizado (`self.style.SUCCESS`, `self.style.ERROR`) para pintar alertas de colores en la terminal según el resultado de la interacción.

Esta Prueba de Concepto demuestra la implementación en Django 6 de un comando de consola interactivo y seguro. Su comportamiento es el equivalente funcional a los Seeders interactivos de frameworks como Laravel.

El objetivo principal es permitir la modificación masiva y controlada del campo `age` en el modelo `Person`, aislando la lógica dentro del ecosistema de comandos nativos de administración de Django (`BaseCommand`), garantizando la integridad de los datos mediante validaciones estrictas en la capa de consola antes de impactar la base de datos.

### Estructura de Archivos Creada
Para los comandos personalizados de administración, Django requiere una estructura de paquetes específica dentro de la aplicación correspondiente, en este caso la aplicación de personas (`apps/person`):

```
apps/
└── person/
    ├── management/
    │   ├── __init__.py
    │   └── commands/
    │       ├── __init__.py
    │       └── update_person_age.py   <-- Implementación de la PoC
```

### Código de la PoC
El código se encuentra en `update_person_age.py` y hereda de `django.core.management.base.BaseCommand`. Implementa:
1. **Entrada Interactiva:** Solicita la nueva edad por terminal mediante `input()`.
2. **Validación de Datos:** Valida que sea un número entero positivo válido entre `0` y `100`.
3. **Petición de Confirmación:** Advierte el número de registros que serán afectados y requiere confirmación (`s`/`n`).
4. **Actualización Masiva Eficiente:** Realiza una sola transacción en base de datos utilizando el método `update()` del ORM de Django (`Person.objects.all().update(age=age)`).
5. **Resumen de Resultados:** Muestra la cantidad de registros actualizados y un desglose agrupado del estado actual de edades en la base de datos.

### Instrucciones de Uso y Escenarios de Prueba

Para ejecutar el comando interactivo, asegúrese de tener activado el entorno virtual y ejecute:

```bash
python manage.py update_person_age
```

#### Escenario 1: Flujo Exitoso
```bash
$ python manage.py update_person_age
Ingrese el valor numérico para actualizar el campo edad de todas las personas:
30

Se actualizarán 7 registros del modelo Person a edad = 30.
¿Desea continuar con esta acción? (s/n): s

Se actualizaron exitosamente 7 registros a edad = 30.

 Resumen de edades actuales:
   - Edad 30: 7 registros
```

#### Escenario 2: Validación de Error (Entrada Inválida)
```bash
$ python manage.py update_person_age
Ingrese el valor numérico para actualizar el campo edad de todas las personas:
abc
Error: Debe ingresar un valor numérico entero válido.
```

#### Escenario 3: Cancelación del Usuario
```bash
$ python manage.py update_person_age
Ingrese el valor numérico para actualizar el campo edad de todas las personas:
28

Se actualizarán 7 registros del modelo Person a edad = 28.
¿Desea continuar con esta acción? (s/n): n
Operación abortada por el usuario.
```
