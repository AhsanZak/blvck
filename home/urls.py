from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('user_login/', views.user_login, name='user_login'),
    path('user-signup/', views.user_signup, name='user_signup'),
    path('view-single/<int:id>', views.view_single, name="single"),
    path('user_home/', views.user_home, name="user_home"),
    path('user-profile/', views.user_profile, name="user_profile"),
    path('user-editprofile/', views.edit_userProfile, name="edit_userProfile"),
    path('user_logout', views.user_logout, name="user_logout"),

    path('add-cart/<int:id>', views.add_cart, name="add_cart"),
    path('cart/', views.cart, name="cart"),

    path('checkout/', views.checkout, name="checkout"),

    path('user-payment/', views.user_payment, name="user_payment"),
    path('user-order/', views.user_order, name="user_order"),
    path('user-removeOrderItem/<int:id>', views.user_removeOrderItem, name="user_removeOrderItem"),


    path('razorpay', views.razorpay, name="razorpay"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)