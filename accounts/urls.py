from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('adminpanel/', views.admin_panel, name='admin_panel'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),


    path('manage-user/', views.manage_user, name='manage_user'),
    path('manage-product/', views.manage_product, name='manage_product'),
    path('manage-category/', views.manage_category, name="manage_category"),
    path('manage-order/', views.manage_order, name="manage_order"),
    path('cancel-order/<str:tid>', views.cancel_order, name="cancel_order"),
    path('order-report', views.order_report, name="order_report"),


    path('add-category', views.add_category, name="add_category"),
    path('delete-category/<int:id>', views.delete_category, name="delete_category"),
    path('delete-user/<int:user_id>', views.delete_user, name='delete_user'),
    path('delete-product/<int:product_id>', views.delete_product, name='delete_product'),
    path('update-user/<int:user_id>', views.update_user, name='update_user'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('update-product/<int:product_id>', views.update_product, name='update_product'),
    path('edit-product/<int:product_id>', views.edit_product, name='edit_product'),
    path('create_user/', views.create_user, name='create_user'),
    path('create_product/', views.create_product, name='create_product'),

]
