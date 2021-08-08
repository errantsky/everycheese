import pytest

pytestmark = pytest.mark.django_db

from ..models import Cheese
from .factories import CheeseFactory


def test__str__():
    cheese = CheeseFactory()
    assert cheese.__str__() == cheese.name
    assert str(cheese) == cheese.name


def test_get_absolute_url():
    cheese = CheeseFactory()
    assert cheese.get_absolute_url() == f'/cheeses/{cheese.slug}/'
