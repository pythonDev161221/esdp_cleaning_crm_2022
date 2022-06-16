from django.test import TestCase


from accounts.models import Staff


class TestCreateUser(TestCase):

    def test_success_create_login(self):
        staff = Staff.objects.create(
            email="test_user_1@gmail.com",
            password="123",
        )

        self.assertEqual(staff.email, "test_user_1@gmail.com")
        self.assertEqual(staff.password, "123")
