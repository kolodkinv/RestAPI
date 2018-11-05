from django.utils.translation import gettext_lazy as _


class ResourceNotFoundError(Exception):

    def __init__(self, resource, value):
        Exception.__init__(self)
        self.message = _('Resource: "{}" not found.'.format(resource))
        self.resource = resource
        self.value = value
