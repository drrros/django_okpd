from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='okpd_check_home'),
    # path('result/', views.result, name='result-page'),

]
