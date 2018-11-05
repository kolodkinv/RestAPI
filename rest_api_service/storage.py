# -*- coding: utf-8 -*-
"""Хранилище данных"""
from abc import ABCMeta, abstractmethod
import redis
from rest_framework.fields import IntegerField

from rest_api_service import settings
from rest_api_service.exceptions import ResourceNotFoundError


class Storage(object):
    """
    Асбтрактное хранилище данных с набором CRUD операций
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def create(self, instance):
        raise NotImplementedError

    @abstractmethod
    def read(self, instance, pk=None, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def update(self, instance, pk):
        raise NotImplementedError

    @abstractmethod
    def delete(self, instance, pk=None):
        raise NotImplementedError


class RedisStorage(Storage):
    """
    Хранилище данных - Redis
    """

    # Фильтрация только целочисленных полей
    INT_FILTER = 'integer'
    # Фильтрация всех типов полей
    ALL_FILTER = 'all'

    FILTER_EQUAL = '='
    FILTER_NOT_EQUAL = '!='
    FILTER_LESS = '<'
    FILTER_MORE = '>'

    def __init__(self, allow_filter=INT_FILTER):
        # ADD SINGLTON
        self.redis = redis.StrictRedis(host=settings.REDIS_HOST,
                                       port=settings.REDIS_PORT,
                                       db=settings.REDIS_DATABASE)
        self.allow_filter = allow_filter

    def create(self, instance):
        """
        Создание объекта в хранилище
        :param instance: данные объекта
        :return:
        """
        type_instance = instance.__class__.__name__
        name_counter = 'id:{}'.format(type_instance)
        index = self.redis.incr(name_counter)
        key = '{}:{}'.format(type_instance, index)
        for field in instance.fields.keys():
            if field == 'id':
                continue

            self.redis.hset(key, field, instance[field].value)

            if self.allow_filter == RedisStorage.INT_FILTER:
                if type(instance.fields[field]) is IntegerField:
                    filter_key = '{}:{}'.format(field, type_instance)
                    self.redis.zadd(filter_key, instance[field].value, key)
            else:
                # Добавить фильтрацию по всем полям. В задаче не требуется
                pass

    def read(self, instance, pk=None, **kwargs):
        """
        Чтение объекта из хранилища
        :param instance: данные объекта
        :param pk: ИД объекта
        :param kwargs: дополнительные параметры, например - фильтрация
        :return:
        """
        result = []
        type_instance = instance.__class__.__name__

        if pk or instance['id'].value:
            id_instance = pk if pk else instance['id'].value
            key = '{}:{}'.format(type_instance, id_instance)
            result.append(self.get_hash_object(key))
        else:
            if 'filter' in kwargs and kwargs['filter']:
                keys = self.filter_instances(kwargs['filter'], type_instance)
            else:
                keys = self.redis.scan_iter('{}:*'.format(type_instance))

            [result.append(self.get_hash_object(key)) for key in keys]

        return result

    def update(self, instance, pk):
        """
        Редатирование объекта в хранилище
        :param instance: данные объекта
        :param pk: ИД объекта
        :return: данные отредактированного объекта
        """
        type_instance = instance.__class__.__name__
        key = '{}:{}'.format(type_instance, pk)
        value = self.redis.hgetall(key)
        if value:
            for field in instance.initial_data.keys():
                self.redis.hset(key, field, instance.initial_data[field])

                if self.allow_filter == RedisStorage.INT_FILTER:
                    filter_key = '{}:{}'.format(field, type_instance)
                    if self.redis.zcard(filter_key):
                        self.redis.zrem(filter_key, key)
                        self.redis.zadd(
                            filter_key, instance.initial_data[field], key)
        else:
            raise ResourceNotFoundError(type_instance, key)
        return self.redis.hgetall(key)

    def delete(self, instance, pk=None):
        """
        Удалить объект из хранилища
        :param instance: данные объекта
        :param pk: ИД объекта
        :return:
        """
        type_instance = instance.__class__.__name__

        if pk or instance['id'].value:
            id_instance = pk if pk else instance['id'].value
            key = '{}:{}'.format(type_instance, id_instance)
            if not self.redis.delete(key):
                raise ResourceNotFoundError(type_instance, key)

            for field in instance.fields.keys():
                if field == 'id':
                    continue

                if self.allow_filter == RedisStorage.INT_FILTER and \
                        type(instance.fields[field]) is IntegerField:
                    filter_key = '{}:{}'.format(field, type_instance)
                    self.redis.zrem(filter_key, key)

    def filter_instances(self, filter_args, type_instance):
        """
        Фильтрация объектов в хранилище
        :param filter_args: параметры фильтрации
        :param type_instance: тип фильтруемых объектов
        :return: список ИД удовлетворяющих фильтру
        """
        keys = set()
        for idx, arg in enumerate(filter_args):
            if self.FILTER_EQUAL in arg:
                keys_by_arg = self.filter_by_equal(arg, type_instance)
            else:
                # Добавить реализацию не равно, больше, меньше
                raise NotImplementedError

            keys = keys & set(keys_by_arg) if idx else set(keys_by_arg)
        return keys

    def filter_by_equal(self, argument, type_instance):
        """
        Фильтрация по равному значению
        :param argument: аргумент с нужным значением
        :param type_instance: тип фильтруемого объекта
        :return: список ИД, удовлетворяющих фильтру
        """
        filter_args = argument.split(self.FILTER_EQUAL)
        filter_value = int(filter_args[1])
        filter_key = '{}:{}'.format(filter_args[0], type_instance)
        return self.redis.zrangebyscore(filter_key, filter_value, filter_value)

    def get_hash_object(self, key):
        """
        Получить хэш-объект
        :param key: ключ объекта
        :return: словарь с полями объекта
        """
        value = self.redis.hgetall(key)
        args = key.split(':')
        if value:
            value.update({'id': args[-1]})
            return value
        else:
            raise ResourceNotFoundError(args[0], key)
