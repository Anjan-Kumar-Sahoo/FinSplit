from django.urls import path
from . import views

urlpatterns = [
    path('add-expense/', views.add_expense),
    path('pool/<int:pool_id>/summary/', views.get_pool_summary),
    path('user/<str:upi_id>/summary/', views.get_user_summary),
    path('create-user/', views.create_user),
    path('add-pool-member/', views.add_pool_member),
    path('settle-debt/', views.settle_debt),

]
