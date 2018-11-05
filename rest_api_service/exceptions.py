# -*- coding: utf-8 -*-
""" Исключения """
from django.utils.translation import gettext_lazy as _


class ResourceNotFoundError(Exception):
    """
    Исключение говорящее о том, что ресурс не найден
    """

    def __init__(self, resource, value):
        Exception.__init__(self)
        self.message = _('Resource: "{}" not found.'.format(resource))
        self.resource = resource
        self.value = value
