from django.urls import path

from folks.views import userRegistration


urlpatterns = [
    path('user/registre/', userRegistration)
]