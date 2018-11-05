from django.conf.urls import url, include
from rest_framework import routers

from rest_api_service import views

router = routers.DefaultRouter()
router.register(r'users', views.UserView, base_name='users')

urlpatterns = [
    url(r'^', include(router.urls)),
]