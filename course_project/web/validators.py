from django.core.exceptions import ValidationError


def file_max_size(value):
    max_size = 5
    filesize = value.file.size
    if filesize > max_size * 1024 * 1024:
        raise ValidationError(f'Image file size is larger of {max_size}MB.')


def phone_validator(value):
    phone_min_length = 7
    if len(value) <= phone_min_length:
        raise ValidationError(f'Phone number must be longer {phone_min_length} digits.')
    for ch in value:
        if not ch.isdigit():
            raise ValidationError('Phone number must contains only numbers.')
