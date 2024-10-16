from django.db import models


class Employee(models.Model):
    POSITION_CHOICES = [
        ('Генеральный директор', 'Генеральный директор'),
        ('Руководитель отдела', 'Руководитель отдела'),
        ('Менеджер', 'Менеджер'),
        ('Старший инженер', 'Старший инженер'),
        ('Инженер', 'Инженер'),
    ]
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, choices=POSITION_CHOICES)
    hire_date = models.DateField()
    salary = models.IntegerField()
    manager = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='subordinates'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
