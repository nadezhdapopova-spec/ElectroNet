import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from network_node.models import NetworkNode





@pytest.mark.django_db
def test_api_access_only_for_active_user():
    """Доступ к API только активным сотрудникам"""
    client = APIClient()
    user = User.objects.create_user(
        username="employee",
        password="pass123",
        is_active=True
    )
    client.login(username="employee", password="pass123")
    response = client.get("/api/nodes/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_api_denied_for_inactive_user():
    """Неактивный пользователь не имеет доступ"""
    client = APIClient()
    user = User.objects.create_user(
        username="inactive",
        password="pass123",
        is_active=False
    )
    client.login(username="inactive", password="pass123")
    response = client.get("/api/nodes/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_debt_cannot_be_updated():
    """Поле debt нельзя изменить через API"""
    client = APIClient()
    user = User.objects.create_user(
        username="employee",
        password="pass123",
        is_active=True
    )
    node = NetworkNode.objects.create(
        name="Retail 1",
        email="test@test.com",
        country="Russia",
        city="Moscow",
        street="Lenina",
        house_number="10",
        debt=1000
    )

    client.login(username="employee", password="pass123")
    response = client.patch(
        f"/api/nodes/{node.id}/",
        {"debt": 9999},
        format="json"
    )
    node.refresh_from_db()
    assert node.debt == 1000


@pytest.mark.django_db
def test_filter_by_country():
    """Фильтрация по стране"""
    client = APIClient()
    user = User.objects.create_user(
        username="employee",
        password="pass123",
        is_active=True
    )
    NetworkNode.objects.create(
        name="Node1",
        email="1@test.com",
        country="Russia",
        city="Moscow",
        street="A",
        house_number="1",
    )
    NetworkNode.objects.create(
        name="Node2",
        email="2@test.com",
        country="Germany",
        city="Berlin",
        street="B",
        house_number="2",
    )
    client.login(username="employee", password="pass123")
    response = client.get("/api/nodes/?country=Russia")
    assert len(response.data) == 1


@pytest.mark.django_db
def test_hierarchy_level():
    """Проверка иерархии объектов как звеньев сети"""
    factory = NetworkNode.objects.create(
        name="Factory",
        email="f@test.com",
        country="Russia",
        city="Moscow",
        street="A",
        house_number="1",
    )
    retail = NetworkNode.objects.create(
        name="Retail",
        email="r@test.com",
        country="Russia",
        city="SPB",
        street="B",
        house_number="2",
        supplier=factory
    )
    assert retail.level() == 1