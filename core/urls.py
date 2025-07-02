from django.urls import path
from . import views

urlpatterns = [
    path('add-expense/', views.add_expense),
    path('pool/<int:pool_id>/summary/', views.get_pool_summary),
    path('user/<str:upi_id>/summary/', views.get_user_summary),
    path('create-user/', views.create_user),
    path('add-pool-member/', views.add_pool_member),
    path('settle-debt/', views.settle_debt),
    path('add-expense-form/', views.add_expense_page, name='add-expense-page'),
    path('pool-summary-form/', views.pool_summary_page, name='pool-summary-form'),
    path('pool-summary/<int:pool_id>/', views.get_pool_summary, name='pool-summary'),
    path('user-summary-form/', views.user_summary_page, name='user-summary-page'),
    path('user-summary/<str:upi_id>/', views.get_user_summary, name='user-summary'),
    path('settle-dues-form/', views.settle_debt_page, name='settle-debt-form'),
    path('settle/', views.settle_debt, name='settle-debt'),
    path('', views.home, name='home'),

]
