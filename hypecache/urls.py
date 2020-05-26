"""hypecache URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.conf.urls.static import static
from store.views import (
    ProductCreateView,
    ProductDetailView,
    ProductUpdateView,
    ProductDeleteView,
    ProductListView,
    FilterListView,
    )
from django.contrib.admin.views.decorators import staff_member_required
from users import views as user_views 
from store import views as store_views

urlpatterns = [
    path('admin/', admin.site.urls),
 

    # ? STORE
    path('',include('store.urls') ),
    path('product/new/', staff_member_required(ProductCreateView.as_view(), login_url='login'), name='product-create'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),

    path('search/<str:category>/', FilterListView.as_view() ,name='product-filter'),


    # ? USERS
    path('register/', user_views.register,name='register'),
    path('profile/', user_views.profile,name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/', user_views.logout_view, name='logout'), 

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'),
        name='password_reset'), 

    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'),
        name='password_reset_done'), 
    
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'),
        name='password_reset_confirm'), 

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),

        # ? Images with Pillow
        # !Not for use in production
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
