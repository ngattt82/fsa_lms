
# user/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from role.models import Role

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    training_programs = models.ManyToManyField('training_program.TrainingProgram', blank=True)

    def __str__(self):
        return self.username


# class CustomUser(AbstractUser):
#     # You don't need to redefine username, password, and email fields.
#     # These are already part of AbstractUser.
#     full_name = models.CharField(max_length=255, blank=True, null=True)
#     role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
#     training_programs = models.ManyToManyField(TrainingProgram, blank=True)

#     # Set unique related_name for groups and user_permissions
#     groups = models.ManyToManyField(
#         'auth.Group',
#         related_name='customuser_set',  # Change this to avoid conflict
#         blank=True,
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         related_name='customuser_set',  # Change this to avoid conflict
#         blank=True,
#     )

#     def __str__(self):
#         return self.username




# class User(models.Model):
#     username = models.CharField(max_length=255, unique=True)
#     password = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=255, blank=True, null=True)
#     role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
#     training_programs = models.ManyToManyField(TrainingProgram, blank=True)  # Correct reference

#     def __str__(self):
#         return self.username

