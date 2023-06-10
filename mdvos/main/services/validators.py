from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.translation import ngettext
from django.utils.deconstruct import deconstructible
from PIL import Image

class MinimumLengthValidator:

    #Sprawdza czy hasło ma odpowiednią długość.

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    f"Hasło musi zawierać co najmniej {self.min_length} znaków.",
                    f"Hasło musi zawierać co najmniej {self.min_length} znaków.",
                    self.min_length,
                ),
                code="password_too_short",
                params={"min_length": self.min_length},
            )

    def get_help_text(self):
        return ngettext(
            f"Hasło musi zawierać co najmniej {self.min_length} znaków.",
            f"Hasło musi zawierać co najmniej {self.min_length} znaków.",
            self.min_length,
        )
    

@deconstructible
class UsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+\Z"
    message = f"Nazwa użytkownika może zawierać tylko litery, cyfry oraz znaki @ . + - _"
    flags = 0


def validate_image_file_size(image):
    if image.size > 1024 * 1024:
        raise ValidationError("Maksymalny rozmiar pliku to 1 MB.")
    
    
def validate_image_size(image):
    max_size = 650

    with Image.open(image) as img:
        if img.width > max_size or img.height > max_size:
            raise ValidationError(f'Maksymalny rozmiar obrazu to {max_size}x{max_size}')
    
    
def validate_image_format(image):
    with Image.open(image) as img:
        if img.format != "PNG":
            raise ValidationError("Podany obraz musi być w formacie PNG")
    