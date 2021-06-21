from django.urls import path
from . import views

from .views import loginT, registerT

urlpatterns = [
    path('login/', loginT, name='login'),
    path('signup/', registerT, name='register'),

]
