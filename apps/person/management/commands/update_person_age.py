from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from apps.person.models import Person

class Command(BaseCommand):
    """
    @class    Command
    
    @brief Ejecuta el comando personalizado para actualizar la edad de todos los
           registros del modelo Person según un valor numérico ingresado por pantalla.
    
    @author    Ing. Argenis Osorio <aosorio@cenditel.gob.ve> (Adaptado a Django 6)
    
    Uso:
    python manage.py update_person_age
    
    @license  <a href='http://derechoinformatico.cenditel.gob.ve/licencia-de-software/'>
                  LICENCIA DE SOFTWARE CENDITEL
              </a>
    """
    
    help = 'Actualiza la edad de todos los registros del modelo Person mediante entrada interactiva'

    def handle(self, *args, **options):
        try:
            # 1. Solicitar el valor numérico por pantalla
            self.stdout.write("Ingrese el valor numérico para actualizar el campo edad de todas las personas:")
            age_input = input().strip()
        except (KeyboardInterrupt, EOFError):
            self.stdout.write(self.style.WARNING('\nOperación cancelada por el usuario.'))
            return

        # 2. Validar que sea un valor numérico entero y no vacío
        if not age_input or not age_input.isdigit():
            self.stderr.write(self.style.ERROR('Error: Debe ingresar un valor numérico entero válido.'))
            return

        # Convertir a entero
        age = int(age_input)

        # Validar rango de edad
        if age < 0 or age > 100:
            self.stderr.write(self.style.ERROR('Error: Ingrese una edad válida (entre 0 y 100 años).'))
            return

        # 3. Confirmar la acción antes de ejecutar
        total_people = Person.objects.count()
        
        if total_people == 0:
            self.stdout.write(self.style.WARNING("No existen registros en la tabla de Personas para actualizar."))
            return

        self.stdout.write(f"\nSe actualizarán {total_people} registros del modelo Person a edad = {age}.")
        self.stdout.write("¿Desea continuar con esta acción? (s/n): ", ending='')
        
        try:
            confirm = input().strip().lower()
        except (KeyboardInterrupt, EOFError):
            self.stdout.write(self.style.WARNING('\nOperación cancelada por el usuario.'))
            return

        if confirm not in ['s', 'si', 'y', 'yes']:
            self.stdout.write(self.style.WARNING('Operación abortada por el usuario.'))
            return

        # 4. Ejecutar la actualización masiva
        with transaction.atomic():
            registros_actualizados = Person.objects.all().update(age=age)

        self.stdout.write(self.style.SUCCESS(f"\nSe actualizaron exitosamente {registros_actualizados} registros a edad = {age}."))

        # 5. Mostrar resumen de los cambios
        self.stdout.write("\n Resumen de edades actuales:")
        
        # Agrupamos por edad y contamos cuántos registros hay de cada una
        distribucion = (
            Person.objects.values('age')
            .annotate(total=Count('id'))
            .order_by('age')
        )
        
        for item in distribucion:
            self.stdout.write(f"   - Edad {item['age']}: {item['total']} registros")
