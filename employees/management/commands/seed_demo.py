import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from faker import Faker

from employees.models import Department, Employee


class Command(BaseCommand):
    help = 'Создает тестовые подразделения (5 уровней) и сотрудников для демонстрации дерева.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--departments',
            type=int,
            default=25,
            help='Число подразделений (по умолчанию 25).',
        )
        parser.add_argument(
            '--employees',
            type=int,
            default=50000,
            help='Число сотрудников (по умолчанию 50 000).',
        )

    def handle(self, *args, **options):
        departments_target = options['departments']
        employees_target = options['employees']

        self.stdout.write('Очищаю старые данные...')
        Employee.objects.all().delete()
        Department.objects.all().delete()

        fake = Faker('ru_RU')
        departments = self._create_departments(departments_target)
        self.stdout.write(self.style.SUCCESS(f'Создано подразделений: {len(departments)}'))

        self._create_employees(fake, departments, employees_target)
        self.stdout.write(self.style.SUCCESS(f'Создано сотрудников: {employees_target}'))

    def _create_departments(self, target_count: int):
        branches = 5
        depth = 5
        created = []

        for branch in range(branches):
            parent = None
            for level in range(depth):
                if len(created) >= target_count:
                    break
                name = f'Подразделение {branch + 1}.{level + 1}'
                parent = Department.objects.create(name=name, parent=parent)
                created.append(parent)

        Department.objects.rebuild()
        return created

    def _create_employees(self, fake: Faker, departments, target_count: int):
        positions = [
            'Менеджер',
            'Разработчик',
            'Аналитик',
            'Тестировщик',
            'HR-специалист',
            'Руководитель группы',
            'Дизайнер',
        ]
        batch_size = 2000
        buffer = []

        for index in range(target_count):
            department = departments[index % len(departments)]
            buffer.append(
                Employee(
                    full_name=fake.name(),
                    position=random.choice(positions),
                    hired_at=fake.date_between(start_date='-10y', end_date='today'),
                    salary=Decimal(random.randrange(50_000, 300_000)),
                    department=department,
                )
            )
            if len(buffer) >= batch_size:
                Employee.objects.bulk_create(buffer, batch_size=batch_size)
                buffer.clear()
                self.stdout.write(f'Создано сотрудников: {index + 1}/{target_count}', ending='\r')

        if buffer:
            Employee.objects.bulk_create(buffer, batch_size=batch_size)
            self.stdout.write(f'Создано сотрудников: {target_count}/{target_count}', ending='\r')
        self.stdout.write('')
