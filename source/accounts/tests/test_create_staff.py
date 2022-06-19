from django.contrib.auth import get_user_model
from django.db import IntegrityError, DataError
from django.test import TestCase, Client
from accounts.models import WorkDay
from django.urls import reverse

User = get_user_model()


class TestCreateUser(TestCase):

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
        cls.staff = User.objects.create(
            email="test_user@gmail.com",
            first_name="test_aman",
            last_name="test_bob",
            password="TestPassword",
            phone="0770700004",
            inn_passport="123345654",
            address="test address",
            online_wallet=["4443 3244 4324 5543"],
            experience="trainee",
            telegram_id="123321343",
        )

    def test_create_staff(self):
        self.assertEqual(self.staff.email, "test_user@gmail.com")
        self.assertEqual(self.staff.first_name, "test_aman")
        self.assertEqual(self.staff.last_name, "test_bob")
        self.assertEqual(self.staff.password, "TestPassword")
        self.assertEqual(self.staff.phone, "+996770700004")
        self.assertEqual(self.staff.inn_passport, "123345654")
        self.assertEqual(self.staff.address, "test address")
        self.assertEqual(self.staff.experience, "trainee")
        self.assertEqual(self.staff.telegram_id, "123321343")

        self.assertListEqual(self.staff.online_wallet, ["4443 3244 4324 5543"])
        self.assertFalse(self.staff.schedule.exists())
        self.assertFalse(self.staff.is_staff)

    def test_add_schedule(self):
        workday = WorkDay.objects.create(
            day="tuesday"
        )
        self.staff.schedule.add(workday)

        self.assertEqual(self.staff.schedule.first(), workday)
        self.assertTrue(self.staff.schedule.exists())

    def test_raise_when_some_unique_fields(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                email="test_user@gmail.com",
                first_name="test_second_user",
                last_name="test_second_bob",
                password="TestPassword",
                inn_passport="123345654",
                phone="0770700004",
            )

    def test_raise_address_length_gt_limit(self):
        with self.assertRaises(DataError):
            User.objects.create(
                email="test_third_user@gmail.com",
                first_name="test_third_user",
                last_name="test_third_bob",
                password="TestPassword",
                address="test" * 51
            )

    def test_profile_view_not_authenticated_user(self):
        self.client.logout()
        responce = self.client.get(reverse("accounts:profile", args=[self.staff.pk]))
        # 302 не авторизованные пользователи перенапрялются на страницу логина
        self.assertEqual(responce.status_code, 302)
        self.assertTemplateNotUsed(responce, "account/staff_profile.html")

    def test_profile_view_authenticated_user(self):
        responce = self.client.get(reverse("accounts:profile", args=[self.staff.pk]))
        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed(responce, "account/staff_profile.html")

    def test_staff_list_view_not_authenticated_user(self):
        self.client.logout()
        responce = self.client.get(reverse("accounts:staff-list"))
        # 302 не авторизованные пользователи перенапрялются на страницу логина
        self.assertEqual(responce.status_code, 302)
        self.assertTemplateNotUsed(responce, "account/staff_list.html")

    def test_staff_list_view_authenticated_user(self):
        responce = self.client.get(reverse("accounts:staff-list"))
        self.assertEqual(responce.status_code, 200)
        self.assertTemplateUsed(responce, "account/staff_list.html")

    def test_staff_delete_not_authenticated_user(self):
        self.client.logout()
        responce = self.client.get(reverse("accounts:staff-delete"))
        # 302 не авторизованные пользователи перенапрялются на страницу логина
        self.assertEqual(responce.status_code, 302)
        self.assertTemplateNotUsed(responce, "account/delete.html")

    def test_staff_delete_in_admin_user(self):
        test_delete_user = User.objects.create(
            email="delete@mail.ru",
            password="deleteS123",
            first_name="deletio",
            last_name="deletions"
        )
        responce = self.client.post(reverse("accounts:staff-delete", args=[test_delete_user.pk]))
        self.assertURLEqual(responce.url, reverse("accounts:staff-list"))
        self.assertEqual(responce.status_code, 302)


