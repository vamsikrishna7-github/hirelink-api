from django.urls import path
from .views import change_password, delete_account

urlpatterns = [
    path('change-password/', change_password, name='change_password'),
    path('delete-account/', delete_account, name='delete_account')
]