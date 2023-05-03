from users.models import User
from carts.models import Cart
from addresses.models import Address
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create admin user"

    def add_arguments(self, parser):
        ...
     #Optional argument
        parser.add_argument(
            "--username",
            type=str,
            help="Define o nome do usuário"
        )
        parser.add_argument(
            "--password",
            type=str,
            help="Define a senha do usuário"
        )
        parser.add_argument(
            "--email",
            type=str,
            help="Define o email do usuário"
        )

    def handle(self, *args, **kwargs):
        username = kwargs["username"]
        email = kwargs["email"]
        password = kwargs["password"]

        new_address = Address.objects.create(
            street="modelUser",
            number="modelUser",
            po="modelUser",
            city="modelUser",
            country="modelUser",
            state="modelUser",
            complement="modelUser"
        )

        new_cart = Cart.objects.create(
            total_price=0.00,
            items=0
        )

        user_data = {}
        user_data["username"] = "admin"
        user_data["email"] = "admin@example.com"
        user_data["password"] = "admin1234"
        user_data["cart"] = new_cart
        user_data["address"] = new_address

        if username:
            user_data["username"] = username
            user_data["email"] = username + "@example.com"
        if email:
            user_data["email"] = email
        if password:
            user_data["password"] = password
        
        try:
            User.objects.get(username=user_data["username"])
        except User.DoesNotExist:
            ...
        else:
            raise CommandError(f'Username `{user_data["username"]}` already taken.')
        
        try:
            User.objects.get(email=user_data["email"])
        except User.DoesNotExist:
            ...
        else:
            raise CommandError(f'Email `{user_data["email"]}` already taken.')
        
        User.objects.create_superuser(**user_data)
        self.stdout.write(self.style.SUCCESS(f'Admin `{user_data["username"]}` successfully created!'))