from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.portal.models import Animal, AnimalGroup, Farm


class FarmCreateViewTests(TestCase):
    def test_create_view_redirects_to_farm_detail_with_public_id(self):
        user = get_user_model().objects.create_user(
            username="tester", password="secret"
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse("portal:farms_create_view"),
            {"name": "Test Farm", "location": "Here"},
        )

        farm = Farm.objects.get(name="Test Farm")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("portal:farms_detail_view", kwargs={"public_id": farm.public_id}),
        )


class SearchViewTests(TestCase):
    def test_search_returns_model_detail_links(self):
        user = get_user_model().objects.create_user(
            username="searcher", password="secret"
        )
        self.client.force_login(user)

        farm = Farm.objects.create(name="Test Farm", location="Here")
        farm.users.add(user)
        herd = AnimalGroup.objects.create(name="Test Herd", farm=farm)
        animal = Animal.objects.create(
            group=herd,
            category="MC",
            breed="Test Breed",
            name="Buster",
        )

        response = self.client.get(reverse("portal:search_view"), {"search": "test"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            reverse("portal:farms_detail_view", kwargs={"public_id": farm.public_id}),
        )
        self.assertContains(
            response,
            reverse("portal:herds_detail_view", kwargs={"public_id": herd.public_id}),
        )
        self.assertContains(
            response,
            reverse(
                "portal:animals_detail_view", kwargs={"public_id": animal.public_id}
            ),
        )
