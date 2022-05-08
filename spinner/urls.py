from django.urls import path
from spinner import views

urlpatterns = [
    path('api/spinner', views.spinner),
    path('api/spinner/<color>', views.color),
]