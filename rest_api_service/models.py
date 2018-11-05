from django.db import models
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    SEX_CHOICES = ((MALE, 'Male'), (FEMALE, 'Female'))

    name = models.CharField(_('Name'), max_length=50)
    patronymic = models.CharField(_('Patronymic'), max_length=50)
    surname = models.CharField(_('Surname'), max_length=100)
    email = models.EmailField(_('Email'))
    age = models.IntegerField()
    sex = models.CharField(choices=SEX_CHOICES, max_length=1, default=MALE)
