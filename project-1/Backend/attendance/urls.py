from django.urls import path
from . import views

urlpatterns = [
    path('attendance/checkin/', views.check_in, name='checkin'),
    path('attendance/checkout/', views.check_out, name='checkout'),
    path('attendance/<str:username>/', views.get_attendance, name='get_attendance'),
]
