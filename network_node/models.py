from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models


class Address(models.Model):
    """Модель Контакты поставщика"""
    country = models.CharField(max_length=100, db_index=True)
    city = models.CharField(max_length=100, db_index=True)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=20)


class NetworkNode(models.Model):
    """Модель Поставщик"""
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.ForeignKey(
        Address,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="nodes"
    )
    supplier = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children"
    )
    level = models.PositiveIntegerField(default=0, editable=False)
    debt = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """Валидация на корректный уровень поставщика в сети и отсутствие циклических зависимостей поставщиков"""
        supplier = self.supplier
        while supplier:
            if supplier == self:
                raise ValidationError("Циклическая зависимость запрещена")
            supplier = supplier.supplier

        if self.supplier and self.supplier.level >= 2:
            raise ValidationError("Максимум 3 уровня сети")

    def save(self, *args, **kwargs):
        """Атоматический расчет и сохранение уровня поставщика в сети"""
        self.full_clean()
        self.level = self.supplier.level + 1 if self.supplier else 0
        super().save(*args, **kwargs)


class Product(models.Model):
    """Модель Продукт"""
    name = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()
    node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name="products"
    )

    def __str__(self):
        return f"{self.name} ({self.model})"
