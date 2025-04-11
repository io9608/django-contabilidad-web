"""
URL configuration for pizzeria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from users import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('', views.dashboard_view),  # Redirect root to dashboard
    path('investments/', views.investments_view, name='investments'),
    path('settings/', views.settings_view, name='settings'),
    path('delete-partner/<int:partner_id>/', views.delete_partner, name='delete_partner'),
    path('products/', views.products_view, name='products'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
]

