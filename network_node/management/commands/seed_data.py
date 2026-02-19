from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from network_node.models import NetworkNode, Product, Address


class Command(BaseCommand):
    help = "seed-команда для создания тестовых данных"

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(
            username="employee1",
            password="password123",
            is_active=True
        )
        factory_address, _ = Address.objects.get_or_create(
            country="Russia",
            city="Moscow",
            street="Kirova",
            house_number="5",
        )
        retail_address, _ = Address.objects.get_or_create(
            country="Russia",
            city="SPB",
            street="Pushkina",
            house_number="10",
        )
        factory, _ = NetworkNode.objects.get_or_create(
            name="Factory",
            email="factory@test.com",
            address=factory_address
        )
        retail, _ = NetworkNode.objects.get_or_create(
            name="Retail",
            email="retail@test.com",
            address=retail_address,
            supplier=factory,
            debt=10000
        )
        Product.objects.get_or_create(
            name="TV",
            model="X100",
            release_date="2026-01-01",
            node=retail
        )
        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно созданы / уже существуют"))
