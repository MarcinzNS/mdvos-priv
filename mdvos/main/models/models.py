from django.db import models
import datetime, os
import hashlib
from django.contrib.auth.models import AbstractUser
from ..services.validators import UsernameValidator

def filepath(request, filename):
    extension = filename.split(".")[-1]
    old_filename_hash = str(hashlib.md5(filename.encode()).hexdigest())
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = f"{timeNow}-{old_filename_hash}.{extension}"
    return os.path.join('static/uploads/', filename)


class OS(models.Model):
    id_os = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    def __str__(self):
        return f"{self.name}"


class OS_version(models.Model):
    os_version_id = models.AutoField(primary_key=True)
    version = models.CharField(max_length=20, unique=True)
    date_start = models.DateField()
    date_end = models.DateField(null=True)
    description = models.CharField(max_length=500, null=True)
    accepted = models.BooleanField()
    os_id = models.ForeignKey(OS, on_delete=models.CASCADE)


class Devices(models.Model):
    id_device = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=30, unique=False)
    premier = models.DateField(null=True)
    device_type = models.CharField(max_length=30)
    model = models.CharField(max_length=50)
    #picture = models.BinaryField(null=True)
    image = models.ImageField(upload_to=filepath, null=True, blank=True)
    accepted = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.device_type}: {self.brand} {self.model}"

# class User(models.Model):
#     id_user = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=30)
#     lastname = models.CharField(max_length=30)
#     login = models.CharField(max_length=50, unique=True)
#     email = models.CharField(max_length=30, unique=True)
#     password = models.CharField(max_length=50)
#     theme = models.BooleanField(default=False)
#     admin_acc = models.BooleanField(default=False)
#     def __str__(self):
#         return f"{self.name} {self.lastname}"

class User(AbstractUser):
    
    # Sprawdza czy wprowadzono poprawną nazwę użytkownika
    username_validator = UsernameValidator()    

    def __str__(self):
        return f"{self.username} {self.first_name} {self.last_name}"
    
class Followed_devices(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    devices_id = models.ForeignKey(Devices, on_delete=models.CASCADE)

class Specification_type(models.Model):
    id_spec = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    def __str__(self):
        return f"{self.name}"

class Specification(models.Model):
    id_spec = models.AutoField(primary_key=True)
    spec_type_id = models.ForeignKey(Specification_type, on_delete=models.CASCADE)
    value = models.CharField(max_length=50, null=True)
    devices_id = models.ForeignKey(Devices, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.value}"

class OS_devices(models.Model):
    os_id = models.ForeignKey(OS_version, on_delete=models.CASCADE)
    devices_id = models.ForeignKey(Devices, on_delete=models.CASCADE)

class Error_report(models.Model):
    id_error = models.AutoField(primary_key=True)
    description = models.CharField(max_length=500)
    date_start = models.DateField()
    date_end = models.DateField(null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    devices_id = models.ForeignKey(Devices, on_delete=models.CASCADE, null=True)
    os_id = models.ForeignKey(OS, on_delete=models.CASCADE, null=True)

class Comment(models.Model):
    id_comment = models.AutoField(primary_key=True)
    text = models.CharField(max_length=250)
    main_comment_id = models.IntegerField(null=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    devices_id = models.ForeignKey(Devices, on_delete=models.CASCADE, null=True)
    os_id = models.ForeignKey(OS, on_delete=models.CASCADE, null=True)

class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    os_id = models.ForeignKey(OS, on_delete=models.CASCADE, null=True)
    devices_id = models.ForeignKey(Devices, on_delete=models.CASCADE, null=True)
    like = models.BooleanField()
    dislike = models.BooleanField()