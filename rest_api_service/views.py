# -*- coding: utf-8 -*-
"""Views"""
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from rest_api_service.exceptions import ResourceNotFoundError
from rest_api_service.serializers import UserSerializer
from rest_api_service.storage import RedisStorage


class UserView(viewsets.ViewSet):
    """
    View пользователя
    """

    def __init__(self, **kwargs):
        super(UserView, self).__init__(**kwargs)
        self.storage = RedisStorage()

    def list(self, request):
        users = self.storage.read(
            UserSerializer(), pk=None, **request.query_params)
        return Response({'users': users})

    def create(self, request):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            self.storage.create(user)
            return Response(user.data, status=status.HTTP_201_CREATED)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            result = self.storage.read(UserSerializer(), pk)
        except ResourceNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(result, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        user = UserSerializer(data=request.data)
        if user.is_valid() and pk:
            try:
                result = self.storage.update(user, pk)
            except ResourceNotFoundError:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(result.update({'id': pk}))
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        user = UserSerializer(data=request.data, partial=True)
        if user.is_valid() and pk:
            try:
                result = self.storage.update(user, pk)
            except ResourceNotFoundError:
                return Response(status=status.HTTP_404_NOT_FOUND)
            return Response(result.update({'id': pk}))
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            self.storage.delete(UserSerializer(), pk)
        except ResourceNotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)



