from django.contrib.auth.forms import UserCreationForm
from .models.models import User, Devices, Comment
from django import forms
from .services.validators import *


class CustomUserCreationForm(UserCreationForm):
    first_name_max_len = 30
    last_name_max_len = 30
    username_max_len = 30
    email_max_len = 50
    username_validator = UsernameValidator()
    
    first_name = forms.CharField(
        label='Imię',
        required=False,
        max_length=first_name_max_len,
        error_messages={
            'max_length': f"Imię nie może przekraczać {first_name_max_len} znaków",
        }
    )
    last_name = forms.CharField(
        label='Nazwisko',
        required=False,
        max_length=last_name_max_len,
        error_messages={
            'max_length': f"Nazwisko nie może przekraczać {last_name_max_len} znaków",
        }
    )
    
    username = forms.CharField(
        label='Nazwa użytkownika*',
        max_length=30,
        validators=[username_validator],
        error_messages={
            'required': "Należy wpisać nazwę użytkownika",
            'max_length': f"Nazwa użytkownika nie może przekraczać {username_max_len} znaków",
            "unique": f"Podana nazwa użytkownika jest już zajęta",
        }
    )

    email = forms.EmailField(
        label='Email*',
        max_length=email_max_len,
        error_messages={
            'required': "Należy wpisać adres email",
            'max_length': f"Email nie może przekraczać {email_max_len} znaków",
            "unique": f"Konto o podanym adresie email już istnieje.",
        }
    )
    
    password1 = forms.CharField(
        label=("Hasło*"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        error_messages={
            'required': "Należy wpisać hasło",
        }
    )
    
    password2 = forms.CharField(
        label=("Powtórz hasło*"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        error_messages={
            'required': "Należy powtórzyć hasło",
        }
    )
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    # nadpisanie error_messages
    error_messages = {
        "password_mismatch": "Hasła muszą być takie same",
    }


class AddDeviceForm(forms.ModelForm):

    brand = forms.CharField(
        label="Marka*",
        max_length=30,
        error_messages={
            'required': "Należy podać markę",
        },
    )

    model = forms.CharField(
        label="Model*",
        max_length=50,
        error_messages={
            'required': "Należy podać model",
        },
    )

    device_type = forms.ChoiceField(
        label="Kategoria",
        choices=[
            ("PHONE", "Telefon"),
            ("TABLET", "Tablet"),
            ("LAPTOP", "Laptop"),
        ],
    )
    release_date = forms.DateField(required=False)
    image = forms.ImageField(
        required=False,
        validators=[validate_image_format, validate_image_file_size, validate_image_size],    
        error_messages= {
            "invalid_image": "Przesłany plik nie jest obrazem lub jest uszkodzony.",
        }, 
    )

    class Meta:
        model = Devices
        fields = ['brand', 'model', 'device_type', 'release_date', 'image']

    def save(self, commit=True):
        # zapisanie wartości release_date w premier
        instance = super().save(commit=False)

        if self.cleaned_data['release_date'] != '':
            instance.premier = self.cleaned_data['release_date']

        if commit:
            instance.save()
        return instance
    

class ChangeDevicePhotoForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        validators=[validate_image_format, validate_image_file_size, validate_image_size],    
        error_messages= {
            "invalid_image": "Przesłany plik nie jest obrazem lub jest uszkodzony.",
        }, 
    )

    class Meta:
        model = Devices
        fields = ['image']

class AddDeviceSpecsForm(forms.Form):

    cpu = forms.CharField(
        label='CPU',
        max_length=50,
        required=False,
    )

    ram = forms.CharField(
        label='RAM',
        max_length=50,
        required=False,
    )

    screen_size = forms.CharField(
        label='Rozmiar ekranu',
        max_length=50,
        required=False,
    )

    battery = forms.CharField(
        label='Bateria',
        max_length=50,
        required=False,
    )

    disk_size = forms.CharField(
        label='Rozmiar dysku',
        max_length=50,
        required=False,
    )


class EditUserForm(forms.ModelForm):
    email = forms.EmailField(
        label='Email',
        required=False,
    )

    first_name = forms.CharField(
        label='Imię',
        required=False
    )
    last_name = forms.CharField(
        label='Nazwisko',
        required=False,
    )
    username = forms.CharField(
        label='Nazwa użytkownika',
        required=False,
    )
    old_password = forms.CharField(
        label='Stare hasło',
        required=True,
    )
    password1 = forms.CharField(
        label='Nowe hasło',
        required=True,
    )

    password2= forms.CharField(
        label='Powtórz hasło',
        required=True,
    )

    def save(self, commit=True):
        instance = super().save(commit=commit)
    
    class Meta:
        model=User
        fields = ['first_name', 'last_name', 'email'] 



class CommentForm(forms.ModelForm):

    comment_text = forms.CharField(
        max_length=250,
        required=True,
        error_messages={
            'required': 'Wpisz treść komentarza'
        } 
    )

    class Meta:
        model = Comment  # Dodaj właściwą klasę modelu
        fields = ['comment_text']  # Dodaj pola, które chcesz uwzględnić w formularzu

    def save(self, device_id, request, os_id=None, main_comment_id=0, commit=True):
        instance = super().save(commit=False)
        instance.text = self.cleaned_data['comment_text']
        instance.user_id = request.user
        instance.os_id=os_id
        instance.main_comment_id=main_comment_id
        instance.devices_id = Devices.objects.get(id_device=device_id)

        if commit:
            instance.save()
        return instance

class UnderCommentForm(forms.ModelForm):

    comment_text = forms.CharField(
        max_length=250,
        required=True,
        error_messages={
            'required': 'Wpisz treść podkomentarza'
        } 
    )


    class Meta:
        model = Comment  # Dodaj właściwą klasę modelu
        fields = ['comment_text']  # Dodaj pola, które chcesz uwzględnić w formularzu

    def save(self, device_id, request, main_id, os_id=None, commit=True):
        instance = super().save(commit=False)
        instance.text = self.cleaned_data['comment_text']
        instance.user_id = request.user
        instance.os_id=os_id
        instance.main_comment_id=main_id
        instance.devices_id = Devices.objects.get(id_device=device_id)

        if commit:
            instance.save()
        return instance


