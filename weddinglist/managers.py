from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field.
    """
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        """Create and save a regular User with the given email and password.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, *, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class AddressUtility:

    @staticmethod
    def defaut_address():
        return {
            "primary": 'false',
            "billing": 'false',
            "address_line1": "",
            "address_line2": "",
            "city": "",
            "state": "",
            "postcode": "",
            "country": "UK",
            "map": {}
        }

    # Google address respons example
    address_components_default = [
        {
            "long_name": "16",
            "short_name": "16",
            "types": ["street_number"]
        },
        {
            "long_name": "San Frantzisko Kalea",
            "short_name": "San Frantzisko Kalea",
            "types": ["route"]
        },
        {
            "long_name": "Bilbo",
            "short_name": "Bilbo",
            "types": ["locality", "political"]
        },
        {
            "long_name": "ME20 7PP",
            "short_name": "ME20 7PP",
            "types": ["postal_code"]
        },
        {
            "long_name": "Aylesford",
            "short_name": "Aylesford",
            "types": ["postal_town"]
        },
        {
            "long_name": "Kent",
            "short_name": "Kent",
            "types": ["administrative_area_level_2", "political"]
        },
        {
            "long_name": "England",
            "short_name": "England",
            "types": ["administrative_area_level_1", "political"]
        },
        {
            "long_name": "United Kingdom",
            "short_name": "GB",
            "types": ["country", "political"]
        }
    ]
