import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase


from crmapp.models import Inventory
from django.urls import reverse

User = get_user_model()


class TestCreateInventory(TestCase):

    def setUp(self):
        admin, created = User.objects.get_or_create(email='admin@mail.ru')
        if created:
            admin.is_staff = True
            admin.set_password('admin')
            admin.save()
        self.client.login(email='admin@mail.ru', password='admin')
        return super().setUp()

    @classmethod
    def setUpTestData(cls):
        cls.inventory = Inventory.objects.create(
            name="test_inventory",
            description="test_inventory_description"
        )

    def test_success_create_inventory(self):
        self.assertTrue(self.inventory is not None)
        self.assertEqual(self.inventory.name, "test_inventory")
        self.assertEqual(self.inventory.description, "test_inventory_description")

        data = {"name": "asfsdf", "description": "dfdsfdsf"}
        response = self.client.post(reverse("crmapp:inventory_create"), data=data)
        self.assertEqual(response.status_code, 302)

    def test_success_change_inventory(self):
        self.inventory.name = "test_inventory_2"
        self.inventory.save()
        self.assertEqual(self.inventory.name, "test_inventory_2")

        data = {"name": "asfsdsfdf", "description": "dfdsdfsfdsf"}
        response = self.client.post(reverse("crmapp:inventory_update", args=[self.inventory.pk]), data=data)
        self.assertEqual(response.status_code, 302)

    def test_success_delete_inventory(self):
        inventory = Inventory.objects.create(
            name="test_inventory_3",
            description="test_inventory_description_3"
        )
        response = self.client.post(reverse("crmapp:inventory_delete", args=[inventory.pk]))
        print(response)
        self.assertEqual(response.status_code, 302)

