import logging
from uuid import uuid4

import bleach
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError, OperationalError, models, transaction
from django.utils.translation import gettext_lazy as _
from slugify import slugify
from .types import ProfileType

logger = logging.getLogger(__name__)


class HubUser(models.Model):
    """
    Model responsible for the user maintenance for the platform. This is a default from django but you can change to
    models.Model and create a One-to-One relationship.
    This way, the application logins are isolated in case of being integrated with external apps.
    If you do it, don't forget to remove the AUTH_USER_MODEL setting from the settings file.
    """

    uuid = models.UUIDField(null=False, blank=False, default=uuid4)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=False, blank=False, related_name="hub_user", on_delete=models.CASCADE
    )
    middle_name = models.CharField(blank=True, null=True, max_length=255)
    profile_type = models.CharField(
        max_length=255, choices=ProfileType.choices, default=ProfileType.USER, null=False, blank=False
    )
    slug = models.SlugField(max_length=255, help_text=_("Slug"), blank=False, null=False, unique=True)
    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    modified_at = models.DateTimeField(null=False, blank=False, auto_now=True)
    is_hidden = models.BooleanField(default=False, blank=False, null=False)
    is_disabled = models.BooleanField(default=False, blank=False, null=False)
    is_password_changed = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return self.display_name

    def save(self, *args, **kwargs):
        if not self.slug:
            _uuid = str(uuid4())[:12]
            self.slug = f"{slugify(self.user.first_name)}-{_uuid}"
        super().save(*args, **kwargs)
        return self

    @staticmethod
    def generate_username(first_name, last_name, email):
        """Generates a username based on certain parameters"""
        return f"{slugify(first_name)}-{slugify(last_name)}-{slugify(email)}-{str(uuid4())}"

    @staticmethod
    def create_hub_user(
        email, password, profile_type=ProfileType.USER, username=None, first_name=None, last_name=None, **kwargs
    ):
        """
        Wrapper where a user is created followed by the models
        :param username: str username
        :param email: str email
        :param password: str password
        :param profile_type: Type of user to be created. Defaults to User
        :param first_name: First name of a user
        :param last_name: Last name of a user
        :param incomplete_signup: If a signup of a HubUser is complete or not
        :return: HubUser
        """
        with transaction.atomic():
            try:
                username = username or HubUser.generate_username(first_name, last_name, email)
                user = get_user_model().objects.create_user(
                    username=bleach.clean(username),
                    email=bleach.clean(email),
                    password=password,
                    is_staff=False,
                    is_superuser=False,
                    first_name=bleach.clean(first_name),
                    last_name=bleach.clean(last_name),
                )
                hub_user = HubUser.objects.create(user=user, profile_type=profile_type, **kwargs)
            except IntegrityError as e:
                logger.exception(f"Error creating the HubUser: {e}")
                return
            return hub_user

    @classmethod
    def update_email(cls, instance, email):
        """Updates the email of an HubUser
        """
        with transaction.atomic():
            try:
                user = get_user_model().objects.select_for_update().get(pk=instance.pk)
                user.email = email
                user.save()
            except (get_user_model().DoesNotExist, OperationalError) as e:
                logger.exception(e)
                return
            return user

    @property
    def display_name(self):
        return "{} - {}".format(self.user.first_name, self.user.last_name)
