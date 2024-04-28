from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    if filesize > 3145728:
        raise ValidationError(
            "The maximum image file size that can be uploaded is 3MB")
    else:
        return value
