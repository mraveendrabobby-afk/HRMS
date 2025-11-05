from django.urls import path
from . import views

app_name = "holiday"

urlpatterns = [
    path("apply/", views.ApplyLeaveAPIView.as_view(), name="apply_leave"),
    path("my/", views.MyLeavesListAPIView.as_view(), name="my_leaves"),
    path("all/", views.AllLeavesListAPIView.as_view(), name="all_leaves"),  # admin only
    path("<int:pk>/status/", views.UpdateLeaveStatusAPIView.as_view(), name="update_status"),  # admin only
]
