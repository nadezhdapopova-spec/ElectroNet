from django.contrib.auth.models import User

from rest_framework.test import APIClient, APITestCase

from network_node.models import Address, NetworkNode


class NetworkNodeViewSetTests(APITestCase):

    def setUp(self):
        """Формирует тестовые данные"""
        super().setUp()

        self.active_user = User.objects.create_user(
            username="employee", password="pass123", is_active=True, is_staff=True
        )
        self.inactive_user = User.objects.create_user(
            username="inactive", password="pass123", is_active=False, is_staff=True
        )

        self.active_client = APIClient()
        self.active_client.force_authenticate(user=self.active_user)

        self.inactive_client = APIClient()
        self.inactive_client.force_authenticate(user=self.inactive_user)

        self.factory_address = Address.objects.create(
            country="Russia", city="Moscow", street="Lenina", house_number="1"
        )
        self.retail_address = Address.objects.create(
            country="Russia", city="SPB", street="Pushkina", house_number="10"
        )
        self.retail_with_debt_address = Address.objects.create(
            country="Germany", city="Berlin", street="B", house_number="2"
        )

        self.factory = NetworkNode.objects.create(
            name="Factory", email="factory@test.com", address=self.factory_address
        )

        self.retail = NetworkNode.objects.create(
            name="Retail",
            email="retail@test.com",
            address=self.retail_address,
            supplier=self.factory,
        )

        self.retail_with_debt = NetworkNode.objects.create(
            name="Retail 1",
            email="test@test.com",
            address=self.retail_with_debt_address,
            supplier=self.factory,
            debt=1000,
        )

    def test_api_access_only_for_active_user(self):
        """Доступ к API только активным сотрудникам"""
        response = self.active_client.get("/api/nodes/")
        assert response.status_code == 200

    def test_api_denied_for_inactive_user(self):
        """Неактивный пользователь не имеет доступ"""
        response = self.inactive_client.get("/api/nodes/")
        assert response.status_code == 403

    def test_debt_cannot_be_updated(self):
        """Поле debt нельзя изменить через API"""
        self.active_client.patch(f"/api/nodes/{self.retail_with_debt.id}/", {"debt": 9999}, format="json")
        self.retail_with_debt.refresh_from_db()
        assert self.retail_with_debt.debt == 1000

    def test_filter_by_country(self):
        """Фильтрация по стране"""
        response = self.active_client.get("/api/nodes/?address__country=Germany")
        assert len(response.data["results"]) == 1

    def test_hierarchy_level(self):
        """Проверка иерархии объектов как звеньев сети"""
        response = self.active_client.get(f"/api/nodes/{self.retail.id}/", format="json")
        assert response.status_code == 200
        data = response.data
        assert data["level"] == 1
        assert data["supplier"]["id"] == self.factory.id
