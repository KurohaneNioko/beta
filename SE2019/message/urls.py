from django.urls import path
from .views import *

urlpatterns = (
    path("msg<int:uid>/", message, name='Msg'),
)
