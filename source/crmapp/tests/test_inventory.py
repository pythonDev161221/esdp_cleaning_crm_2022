import datetime

from django.test import TestCase


from crmapp.models import Inventory, Order, ObjectType, Client, Fine, Service


class TestCreateInventory(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.inventory = Inventory.objects.create(
            name="test_inventory",
            description="test_inventory_description"
        )
        cls.object_type = ObjectType.objects.create(
            name="object_name_1"
        )

    def test_success_create_inventory(self):
        self.assertTrue(self.inventory is not None)
        self.assertEqual(self.inventory.name, "test_inventory")
        self.assertEqual(self.inventory.description, "test_inventory_description")

    def test_success_create_object_type(self):
        self.assertTrue(self.object_type is not None)
        self.assertEqual(self.object_type.name, "object_name_1")

    def test_success_create_client(self):
        client = Client.objects.create(
            first_name="client_first_name",
            last_name="client_last_name",
            phone="+996700234152",
            organization="client_organization"
        )

        self.assertTrue(client is not None)
        self.assertEqual(Client.objects.get(id=1).first_name, "client_first_name")
        self.assertEqual(client.last_name, "client_last_name")
        self.assertEqual(client.phone, "+996700234152")
        self.assertEqual(client.organization, "client_organization")

    def test_success_create_fine(self):
        fine = Fine.objects.create(
            category="fine_category",
            fine="fine",
            criteria="fine_criteria",
            value=500,
            description="fine_description"
        )

        self.assertTrue(fine is not None)
        self.assertEqual(Fine.objects.get(id=1).category, "fine_category")
        self.assertEqual(fine.fine, "fine")
        self.assertEqual(fine.value, 500)
        self.assertEqual(fine.description, "fine_description")
        self.assertEqual(fine.criteria, "fine_criteria")

    def test_success_create_service(self):
        service = Service.objects.create(
            name="service_name",
            unit="squire_meter",
            price=234,
            is_extra=True,
        )

        self.assertTrue(service is not None)
        self.assertEqual(service.name, "service_name")
        self.assertEqual(service.unit, "squire_meter")
        self.assertEqual(service.price, 234)
        self.assertEqual(service.is_extra, True)

