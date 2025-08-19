from django.urls import path
from . import views

app_name = 'links'

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:code>/', views.follow, name='follow'),   # /abc123 -> redirect
    path('<str:code>/stats/', views.stats, name='stats')
]
