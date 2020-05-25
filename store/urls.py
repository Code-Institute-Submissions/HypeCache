from django.urls import path,include
from .views import (
    ProductListView,
    )
from . import views

urlpatterns = [
    path('', ProductListView.as_view(),name='home' ),
]
