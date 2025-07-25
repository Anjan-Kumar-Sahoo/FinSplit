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
    path('create-user-form/', views.create_user_page),
    path('add-pool-member-form/', views.add_pool_member_page),
    path('all-pools/', views.show_all_pools, name='show_all_pools'),
    path('all-users/', views.show_all_users, name='show_all_users'),
    path('pool-summary-form/', views.pool_summary_page, name='pool-summary-form'),   # ✅ HTML Form Page
    path('pool-summary/<int:pool_id>/', views.get_pool_summary, name='pool-summary'), # ✅ API
    path('create-pool-form/', views.create_pool_page, name='create_pool_form'),
    path('create-pool/', views.create_pool, name='create_pool'),  # API endpoint

]
