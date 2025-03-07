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
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователь'
        ordering = ['-id']

    def __str__(self):
        return self.email
