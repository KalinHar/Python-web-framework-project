from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


def file_max_size(value):
    max_size = 5
    filesize = value.file.size
    if filesize > max_size * 1024 * 1024:
        raise ValidationError(f'File max size is {max_size}MB.')


def phone_validator(value):
    phone_min_length = 7
    if len(value) <= phone_min_length:
        raise ValidationError(f'Phone number must be longer {phone_min_length} digits.')
    for ch in value:
        if not ch.isdigit():
            raise ValidationError('Phone number must contains only numbers.')


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
        default=False,
    )

    reported = models.BooleanField(
        default=False,
    )

    @property
    def difference(self):
        return self.new - self.old

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
        default=False,
    )

    @property
    def difference(self):
        return self.new - self.old