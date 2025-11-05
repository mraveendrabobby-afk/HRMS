from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import LeaveRequest
from .serializers import LeaveRequestSerializer
from django.shortcuts import get_object_or_404

# Create leave (user must be authenticated)
from rest_framework.response import Response

class ApplyLeaveAPIView(generics.CreateAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("\n❌ Validation Errors:", serializer.errors)  # 👈 check Django console
            return Response(serializer.errors, status=400)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



# List leaves for the current user
class MyLeavesListAPIView(generics.ListAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LeaveRequest.objects.filter(user=self.request.user).order_by("-created_at")


# Admin: list all leaves
class AllLeavesListAPIView(generics.ListAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAdminUser]
    queryset = LeaveRequest.objects.all()


# Admin: update leave status (approve/reject)
class UpdateLeaveStatusAPIView(generics.UpdateAPIView):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAdminUser]
    queryset = LeaveRequest.objects.all()

    # Restrict updates to status only (you can expand if needed)
    def update(self, request, *args, **kwargs):
        leave = self.get_object()
        status_value = request.data.get("status")
        if status_value not in dict(LeaveRequest.STATUS_CHOICES):
            return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        leave.status = status_value
        leave.save()
        return Response(self.get_serializer(leave).data)
