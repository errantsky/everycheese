import pytest
from pytest_django.asserts import assertContains

from django.urls import reverse

from .factories import CheeseFactory, UserFactory
from ..models import Cheese
from ..views import (
    CheeseListView,
    CheeseDetailView,
)

@pytest.fixture
def user():
    return UserFactory()

pytestmark = pytest.mark.django_db


def test_good_cheese_list_view_expanded(rf):
    url = reverse('cheeses:list')
    request = rf.get(url)
    callable_obj = CheeseListView.as_view()
    response = callable_obj(request)
    assertContains(response, 'Cheese List')


def test_good_cheese_list_view(rf):
    request = rf.get(reverse('cheeses:list'))
    response = CheeseListView.as_view()(request)
    assertContains(response, "Cheese List")


def test_good_cheese_detail_view(rf):
    cheese = CheeseFactory()
    url = reverse("cheeses:detail", kwargs={'slug': cheese.slug})
    request = rf.get(url)

    callable_obj = CheeseDetailView.as_view()
    response = callable_obj(request, slug=cheese.slug)
    assertContains(response, cheese.name)


def test_good_cheese_create_view(client, user):
    client.force_login(user)
    url = reverse('cheeses:add')
    response = client.get(url)
    assert response.status_code == 200


def test_cheese_list_contains_2_cheeses(rf):
    cheese1 = CheeseFactory()
    cheese2 = CheeseFactory()

    request = rf.get(reverse('cheeses:list'))
    response = CheeseListView.as_view()(request)

    assertContains(response, cheese1.name)
    assertContains(response, cheese2.name)


def test_detail_contains_cheese_data(rf):
    cheese = CheeseFactory()

    request = rf.get(reverse('cheeses:detail', kwargs={'slug': cheese.slug}))
    response = CheeseDetailView.as_view()(request, slug=cheese.slug)

    assertContains(response, cheese.name)
    assertContains(response, cheese.description)
    assertContains(response, cheese.get_firmness_display())
    assertContains(response, cheese.country_of_origin.name)
    assertContains(response, cheese.creator)


def test_cheese_create_form_valid(client, user):
    client.force_login(user)
    form_data = {"name": "Paski Sir",
                 "description": "A salty hard cheese",
                 "firmness": Cheese.Firmness.HARD,
    }
    url = reverse('cheeses:add')
    response = client.post(url, form_data)

    assert response.status_code == 302

    cheese = Cheese.objects.get(name="Paski Sir")

    assert cheese.description == "A salty hard cheese"
    assert cheese.firmness == Cheese.Firmness.HARD
    assert cheese.creator == user
