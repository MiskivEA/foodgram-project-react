from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True,
        blank=False
    )

    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$')]
    )

    first_name = models.CharField(
        max_length=150,
        verbose_name='имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='фамилия',
        blank=True
    )
    REQUIRED_FIELDS = 'username',
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    """Подписки пользователей друг на друга"""
    user = models.ForeignKey(
        User,
        related_name='followers',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        related_name='followings',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='follow_unique'
            )
        ]

    def __str__(self):
        return f'{self.user} > подписан на > {self.author}'
