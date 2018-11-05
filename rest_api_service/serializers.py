# -*- coding: utf-8 -*-
"""Сериализаторы"""
from rest_framework import serializers

from rest_api_service.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели пользователя
    """

    class Meta:
        """
        Метаданные сериализатора
        """
        model = User
        fields = ['id', 'name', 'patronymic', 'surname', 'email', 'age', 'sex']

    name = serializers.CharField()
    patronymic = serializers.CharField()
    surname = serializers.CharField()
    email = serializers.EmailField()
    age = serializers.IntegerField()
    sex = serializers.ChoiceField([(User.MALE, 'Male'),
                                   (User.FEMALE, 'Female')])


