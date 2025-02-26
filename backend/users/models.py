from django.contrib.auth.models import AbstractUser
from django.db import models

from api import constants


class User(AbstractUser):
    """Расширенная модель пользователя."""

    email = models.EmailField(
        'Email',
        max_length=constants.EMAIL_NAME_FIELD_LENGTH,
        unique=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'
        ordering = ['-id']

    def __str__(self):
        return self.email
