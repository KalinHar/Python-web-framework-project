from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from course_project.web.validators import phone_validator, file_max_size


def get_username(self):
    return self.username


User.add_to_class("__str__", get_username)


class Client(models.Model):
    names = models.CharField(
        max_length=40,
    )

    old_debts = models.IntegerField(
        default=0,
    )

    phone = models.CharField(
        max_length=20,
        validators=(
            phone_validator,
        ),
    )

    old = models.IntegerField(
        validators=(
            MinValueValidator(0),
        ),
    )

    new = models.IntegerField(
        validators=(
            MinValueValidator(0),
        ),
    )

    username = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    paid = models.BooleanField(
        default=True,
    )

    reported = models.BooleanField(
        default=True,
    )

    @property
    def difference(self):
        return self.new - self.old

    def __str__(self):
        return self.names

    class Meta:
        ordering = ('pk',)


class Taxes(models.Model):
    price = models.FloatField(
        validators=(
            MinValueValidator(0),
        ),
    )

    tax = models.FloatField(
        validators=(
            MinValueValidator(0),
        ),
    )


class Archive(models.Model):
    from_date = models.DateTimeField(
        auto_now_add=True,
    )

    data = models.JSONField()

    taxes = models.JSONField()

    class Meta:
        ordering = ('-from_date',)


class Notice(models.Model):
    from_date = models.DateTimeField(
        auto_now=True,
    )

    title = models.CharField(
        max_length=30,
    )

    content = models.TextField(
        max_length=300,
    )

    image = models.ImageField(
        null=True,
        blank=True,
        upload_to='media/notice_images/',
        validators=(
            file_max_size,
        )
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-from_date',)


class OldDebts(models.Model):
    from_date = models.DateTimeField(
        auto_now_add=True,
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
    )

    debts = models.FloatField()

    indications = models.CharField(
        max_length=40
    )

    class Meta:
        ordering = ('-from_date',)


class Master(models.Model):
    old = models.IntegerField(
        validators=(
            MinValueValidator(0),
        ),
    )

    new = models.IntegerField(
        validators=(
            MinValueValidator(0),
        ),
    )

    reported = models.BooleanField(
        default=True,
    )

    @property
    def difference(self):
        return self.new - self.old