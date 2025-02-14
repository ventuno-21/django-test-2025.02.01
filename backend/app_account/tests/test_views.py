from django.test import TestCase, Client
from django.urls import reverse
from app_account.models import User
from app_account.forms import UserRegistrationForm


class TestUserLoginView(TestCase):

    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username="ventuno",
            email="ventuno@ventuno.com",
            password="ventuno21",
        )

    def test_user_login_GET(self):
        response = self.client.get(reverse("app_account:user_login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_account/login.html")

    def test_user_login_valid_POST(self):
        response = self.client.post(
            reverse("app_account:user_login"),
            data={
                "username": "ventuno",
                "password": "ventuno21",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/")
        print("response.content=====", response.content)

    def test_user_login_invalid_POST(self):
        response = self.client.post(
            reverse("app_account:user_login"),
            data={
                "username": "not-valid-username",
                "password": "ventuno21",
            },
        )
        print("response.content=====", response.content)
        self.assertTemplateUsed(response, "app_account/login.html")
        # self.assertFormError(
        #     form=response.context["form"],
        #     field="username",
        #     errors=["username or password is wrong"],
        # )

        # self.assertIn("username or password is wrong", response.content)

    # def test_invalid_login(self):
    #     bad_resp = self.client.post(
    #     "/accounts/login/", {"username": "bad", "password":
    #     "bad"}
    #     )
    #     self.assertEqual(bad_resp.status_code, 200)
    #     self.assertIn(b"Please enter a correct username and
    #     password", bad_resp.content)


class TestUserRegisterView(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_register_GET(self):
        response = self.client.get(reverse("app_account:user_register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "app_account/register.html")
        self.assertEqual(response.status_code, 200)

        # self.failUnless(response.context["form"], UserRegistrationForm)

    def test_user_register_POST_valid(self):
        response = self.client.post(
            reverse("app_account:user_register"),
            data={
                "username": "ventuno",
                "email": "ventuno@ventuno.com",
                "password1": "ventuno21",
                "password2": "ventuno21",
            },
        )
        # status_code:302 is for redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("app_test1:homey"))
        # 1 user is added therefore in User model ONE user should be exist
        self.assertEqual(User.objects.count(), 1)

    def test_user_register_POST_invalid(self):
        response = self.client.post(
            reverse("app_account:user_register"),
            data={
                "username": "user2",
                "email": "invalid email",
                "password1": "ventuno21",
                "password2": "ventuno21",
            },
        )
        self.assertEqual(response.status_code, 200)
        # Seems like failIf doesnt work anymore
        # self.failIf(response.context["form"].is_valid())
        """
        The error inside errors is exacty 
        what django send us if the emil address be invalid
        """
        self.assertFormError(
            form=response.context["form"],
            field="email",
            errors=["Enter a valid email address."],
        )
