from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from library.models import User, Item, Service
import datetime


class LibraryTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.user1 = User.objects.create(
            user_ID="USER1234",
            user_name="John Doe",
            user_phone="1111111111",
            user_address="123 Elm Street",
            user_dob="2010-01-01",
        )

        self.user2 = User.objects.create(
            user_ID="USER5678",
            user_name="Jane Smith",
            user_phone="2222222222",
            user_address="456 Oak Avenue",
            user_dob="2005-05-05",
        )

        # Create test items
        self.item1 = Item.objects.create(
            item_ID=1,
            item_name="Test Book",
            item_type=Item.BOOK,
            item_price=10.00,
            item_stock=5,
            item_request=False,
            best_seller=False,
        )

        self.item2 = Item.objects.create(
            item_ID=2,
            item_name="Test Video",
            item_type=Item.VIDEO,
            item_price=15.00,
            item_stock=0,
            item_request=True,
            best_seller=False,
        )

    def test_register_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "name": "Alice Johnson",
                "address": "789 Pine Lane",
                "mobile": "3333333333",
                "dob": "1990-02-02",
            },
        )
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertTrue(User.objects.filter(user_name="Alice Johnson").exists())

    def test_userlist_view(self):
        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("user_list", response.context)
        self.assertEqual(len(response.context["user_list"]), 2)

    def test_user_info_view(self):
        response = self.client.get(reverse("user_info", args=["USER1234"]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("user", response.context)
        self.assertEqual(response.context["user"].user_ID, "USER1234")

    def test_catalog_view(self):
        response = self.client.get(reverse("catalog", args=[Item.BOOK]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("item_data", response.context)
        self.assertEqual(len(response.context["item_data"]), 1)

    def test_checkout_view(self):
        response = self.client.post(
            reverse("checkout", args=[1]), {"user_id": "USER1234"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.context)
        self.assertEqual(response.context["message"], "Checkout Successful")
        self.assertEqual(Item.objects.get(item_ID=1).item_stock, 4)

    def test_services_view(self):
        issued_date = timezone.now().date()
        return_date = issued_date + datetime.timedelta(weeks=2)
        Service.objects.create(
            user_ID="USER1234",
            item_ID=1,
            issued_date=issued_date,
            return_date=return_date,
        )
        response = self.client.get(reverse("services", args=["USER1234"]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("services_data", response.context)
        self.assertEqual(len(response.context["services_data"]), 1)

    def test_item_info_view(self):
        response = self.client.get(reverse("item_info", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertIn("item", response.context)
        self.assertEqual(response.context["item"].item_ID, 1)
