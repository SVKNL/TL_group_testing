from django.core.exceptions import ValidationError
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Department(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'подразделение'
        verbose_name_plural = 'подразделения'

    def clean(self):
        if self.parent and self.parent.level >= 4:
            raise ValidationError('Максимальная глубина подразделений — 5 уровней.')

    def __str__(self) -> str:
        return self.name


class Employee(models.Model):
    full_name = models.CharField('ФИО', max_length=255)
    position = models.CharField('должность', max_length=255)
    hired_at = models.DateField('дата приема')
    salary = models.DecimalField('зарплата', max_digits=12, decimal_places=2)
    department = models.ForeignKey(
        Department,
        related_name='employees',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['full_name']
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'
        indexes = [
            models.Index(fields=['department']),
            models.Index(fields=['full_name']),
            models.Index(fields=['hired_at']),
        ]

    def __str__(self) -> str:
        return self.full_name
