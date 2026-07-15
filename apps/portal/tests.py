from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.portal.models import (
    Animal,
    AnimalGroup,
    Farm,
    LivestockRecord,
    RecordTemplate,
)


class FarmCreateViewTests(TestCase):
    def test_create_view_redirects_to_farm_detail_with_slug(self):
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
            reverse("portal:farms_detail_view", kwargs={"slug": farm.slug}),
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
            reverse("portal:farms_detail_view", kwargs={"slug": farm.slug}),
        )
        self.assertContains(
            response,
            reverse("portal:herds_detail_view", kwargs={"slug": herd.slug}),
        )
        self.assertContains(
            response,
            reverse(
                "portal:animals_detail_view",
                kwargs={"slug": animal.slug},
            ),
        )


class DashboardViewTests(TestCase):
    def test_dashboard_shows_real_counts_and_recent_activity(self):
        user = get_user_model().objects.create_user(
            username="dashboard_user", password="secret"
        )
        self.client.force_login(user)

        farm = Farm.objects.create(name="Demo Farm", location="Here")
        farm.users.add(user)

        herd = AnimalGroup.objects.create(name="Demo Herd", farm=farm)
        animal = Animal.objects.create(group=herd, category="MC", breed="Barred Rock")
        template = RecordTemplate.objects.create(
            farm=farm,
            name="Health Check",
            slug="health-check",
            schema=[
                {
                    "name": "note",
                    "label": "Note",
                    "field_type": "text",
                    "required": True,
                }
            ],
        )
        LivestockRecord.objects.create(
            report_link=animal,
            template=template,
            data={"note": "Checked in"},
        )

        response = self.client.get(reverse("portal:index_view"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1")
        self.assertContains(response, "Demo Farm")
        self.assertContains(response, "Health Check")


class TagReadViewTests(TestCase):
    def test_post_redirects_to_record_creation_view_with_selected_form(self):
        user = get_user_model().objects.create_user(
            username="tag_reader", password="secret"
        )
        self.client.force_login(user)

        farm = Farm.objects.create(name="Tag Farm", location="Here")
        farm.users.add(user)
        RecordTemplate.objects.create(
            farm=farm,
            name="Health Check",
            slug="health-check",
            schema=[
                {
                    "name": "note",
                    "label": "Note",
                    "field_type": "text",
                    "required": True,
                }
            ],
        )

        response = self.client.post(
            reverse("portal:tags_read_view"),
            {
                "slug": "animal-public-id",
                "template_slug": "health-check",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse(
                "portal:records_create_view",
                kwargs={"slug": "animal-public-id", "form_slug": "health-check"},
            ),
        )


class TagWriteModalViewTests(TestCase):
    def test_alpine_request_returns_modal_fragment(self):
        user = get_user_model().objects.create_user(
            username="tagger", password="secret"
        )
        self.client.force_login(user)

        response = self.client.get(
            reverse("portal:tags_write_view"),
            HTTP_X_ALPINE_REQUEST="true",
            HTTP_X_ALPINE_TARGET="modal",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Write NFC Tag")
        self.assertContains(response, "Write Tag")
