from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from .models import Attendance
from .serializers import AttendanceSerializer

@api_view(['POST'])
def check_in(request):
    username = request.data.get('username')
    if not username:
        return Response({"message": "username required"}, status=400)

    today = datetime.now().date()
    time_now = datetime.now().time()

    attendance, created = Attendance.objects.get_or_create(
        username=username, date=today
    )

    if attendance.check_in:
        return Response({"message": "Already checked in today."}, status=200)

    attendance.check_in = time_now
    attendance.save()

    return Response({
        "message": "Check-in successful",
        "time": attendance.check_in.strftime("%H:%M:%S")
    }, status=201)


@api_view(['POST'])
def check_out(request):
    username = request.data.get('username')
    if not username:
        return Response({"message": "username required"}, status=400)

    today = datetime.now().date()
    time_now = datetime.now().time()

    try:
        attendance = Attendance.objects.get(username=username, date=today)
    except Attendance.DoesNotExist:
        return Response({"message": "No check-in record found for today"}, status=404)

    if attendance.check_out:
        return Response({"message": "Already checked out today."}, status=200)

    from datetime import datetime as dt
    check_in_dt = dt.combine(today, attendance.check_in)
    check_out_dt = dt.combine(today, time_now)
    duration_seconds = int((check_out_dt - check_in_dt).total_seconds())
    hours = duration_seconds // 3600
    minutes = (duration_seconds % 3600) // 60

    attendance.check_out = time_now
    attendance.duration = f"{hours}h {minutes}m"
    attendance.save()

    return Response({
        "message": "Check-out successful",
        "time": attendance.check_out.strftime("%H:%M:%S"),
        "duration": attendance.duration
    }, status=200)


@api_view(['GET'])
def get_attendance(request, username):
    records = Attendance.objects.filter(username=username).order_by('-date')
    serializer = AttendanceSerializer(records, many=True)
    return Response(serializer.data, status=200)
