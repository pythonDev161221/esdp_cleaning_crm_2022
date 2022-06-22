import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase

from crmapp.models import Order, ObjectType, Client, Service, ServiceOrder, Inventory, InventoryOrder, StaffOrder
from django.urls import reverse

User = get_user_model()


class TestCreateOrder(TestCase):
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
        obj_type = ObjectType.objects.create(
            name="house"
        )

        staff = User.objects.create(
            email="test_user_for_view@mail.ru",
            password="testPassword",
            first_name="UserView"
        )

        client_info = Client.objects.create(
            first_name="Momoku",
            last_name="Dono",
            phone="0777544332",
            organization="MomokunoDono Family"
        )

        manager = User.objects.create(
            email="manager@mail.ru",
            password="Managers",
            first_name="manager"
        )
        tz = pytz.timezone("Asia/Bishkek")

        cls.order = Order.objects.create(
            status="new",
            object_type=obj_type,
            work_start=datetime.datetime.now().astimezone(tz),
            cleaning_time=datetime.timedelta(hours=6, minutes=30),
            client_info=client_info,
            address="test_address_Polskaya",
            manager=manager,
            review=4,
            payment_type="cash",
            part_units=2000,
            description="test_description",
        )

        cls.second_order = Order.objects.create(
            status="new",
            object_type=obj_type,
            work_start=datetime.datetime.now(),
            cleaning_time=datetime.timedelta(hours=6, minutes=30),
            client_info=client_info,
            address="test_address_Rauedsl",
            manager=manager,
            review=2,
            payment_type="visa",
            part_units=1000,
            description="test_second_description",
        )

        StaffOrder.objects.create(
            staff=staff,
            order=cls.second_order,
            is_brigadier=True
        )

    def test_create_order(self):
        self.assertEqual(self.order.status, "new")
        self.assertEqual(self.order.object_type, ObjectType.objects.first())
        self.assertEqual(self.order.cleaning_time, datetime.timedelta(hours=6, minutes=30))
        self.assertEqual(self.order.client_info, Client.objects.first())
        self.assertEqual(self.order.address, "test_address_Polskaya")
        self.assertEqual(self.order.manager, User.objects.get(email="manager@mail.ru",
                                                              password="Managers",
                                                              first_name="manager"))
        self.assertEqual(self.order.review, 4)
        self.assertEqual(self.order.payment_type, "cash")
        self.assertEqual(self.order.part_units, 2000)
        self.assertEqual(self.order.description, "test_description")

        self.assertTrue(self.order.work_start)

        self.assertFalse(self.order.services.exists())
        self.assertFalse(self.order.cleaners.exists())
        self.assertFalse(self.order.order_inventories.exists())
        self.assertFalse(self.order.is_deleted)

    def test_add_staff_on_order(self):
        self.assertFalse(self.order.cleaners.exists())
        staff1 = User.objects.create(
            email="test1@mail.ru",
            password="testPassword",
            first_name="TestLakiMan"
        )
        staff2 = User.objects.create(
            email="test2@mail.ru",
            password="testPassword",
            first_name="TestBobMan"
        )
        self.order.cleaners.add(staff1)
        self.order.cleaners.add(staff2)

        self.assertTrue(self.order.cleaners.exists())

        self.assertEqual(self.order.cleaners.get(email="test1@mail.ru",
                                                 password="testPassword",
                                                 first_name="TestLakiMan"), staff1)
        self.assertEqual(self.order.cleaners.get(email="test2@mail.ru",
                                                 password="testPassword",
                                                 first_name="TestBobMan"), staff2)

    def test_add_servises_on_order(self):
        self.assertFalse(self.order.services.exists())

        service1 = Service.objects.create(
            name='Test service ;)',
            unit="square_meter",
            price=20,
            is_extra=False
        )
        service2 = Service.objects.create(
            name='Test second service ;(',
            unit="square_meter",
            price=35,
            is_extra=True
        )

        service_order_1 = ServiceOrder.objects.create(
            order=self.order,
            service=service1,
            amount=8,
            rate=1.0,
        )
        service_order_2 = ServiceOrder.objects.create(
            order=self.order,
            service=service2,
            amount=20,
            rate=3.0,
        )
        self.assertEqual(self.order.order_services.get(service=service1), service_order_1)
        self.assertEqual(self.order.order_services.get(service=service2), service_order_2)
        self.assertEqual(self.order.get_total(), 2260)

        self.assertTrue(self.order.services.exists())

    def test_add_inventory_in_order(self):
        self.assertFalse(self.order.order_inventories.exists())
        inventory1 = Inventory.objects.create(
            name='test_first_inventory',
            description="test_description"
        )
        inventory2 = Inventory.objects.create(
            name="test_second_inventory",
            description="description_test"
        )

        inventory_order_1 = InventoryOrder.objects.create(
            order=self.order,
            inventory=inventory1,
            amount=12
        )
        inventory_order_2 = InventoryOrder.objects.create(
            order=self.order,
            inventory=inventory2,
            amount=8
        )

        self.assertEqual(self.order.order_inventories.get(inventory=inventory1), inventory_order_1)
        self.assertEqual(self.order.order_inventories.get(inventory=inventory2), inventory_order_2)
        self.assertEqual(self.order.order_inventories.all().count(), 2)

        self.assertTrue(self.order.order_inventories.exists())

    def test_delete_order_view(self):
        responce = self.client.post(reverse("crmapp:order_delete", args=[self.second_order.pk]))
        self.assertEqual(responce.status_code, 302)
        self.assertEqual(Order.objects.filter(is_deleted=True).first(), self.second_order)
        self.assertTemplateUsed("order/order_list.html")

    def test_detail_order_view(self):
        responce = self.client.get(reverse("crmapp:order_detail", args=[self.second_order.pk]))
        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed("order/order_detail.html")
