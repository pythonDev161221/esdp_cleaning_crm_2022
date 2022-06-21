import datetime

from django.test import TestCase


from crmapp.models import Inventory


class TestCreateInventory(TestCase):
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

    def test_success_change_inventory(self):
        self.inventory.name = "test_inventory_2"
        self.inventory.save()
        self.assertEqual(self.inventory.name, "test_inventory_2")
