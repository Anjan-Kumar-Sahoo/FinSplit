from django.urls import path
from . import views

urlpatterns = [
    path('add-expense/', views.add_expense),
]
