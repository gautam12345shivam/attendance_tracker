# Create your views here.
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework import generics
from .models import Attendance, Employee
from .serializers import AttendanceSerializer, EmployeeSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Employee
from datetime import datetime

class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        employee = Employee.objects.get(user=self.request.user)
        serializer.save(employee=employee)


class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]


class MyAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        employee = Employee.objects.get(user=self.request.user)
        return Attendance.objects.filter(employee=employee).order_by('-date')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        department = request.POST.get('department')
        designation = request.POST.get('designation')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})

        user = User.objects.create_user(username=username, password=password)
        Employee.objects.create(
            user=user, department=department, designation=designation)
        login(request, user)
        return redirect('home')

    return render(request, 'register.html')

# login_view

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

# logout_view


def logout_view(request):
    logout(request)
    return redirect('login')


class AttendanceTableView(LoginRequiredMixin, View):
    def get(self, request):
        employee = request.user.employee  
        records = Attendance.objects.filter(
            employee=employee).order_by('-date')

        for record in records:
            if record.check_in and record.check_out:
                check_in_time = datetime.combine(record.date, record.check_in)
                check_out_time = datetime.combine(
                    record.date, record.check_out)
                duration = check_out_time - check_in_time
                record.hours_worked = round(duration.total_seconds() / 3600, 2)
            else:
             record.hours_worked = None

        return render(request, 'my_attendance_table.html', {'records': records})


# Attendance_submitView

@csrf_exempt
def mark_attendance_view(request):
    message = None
    if request.method == 'POST':
        employee = Employee.objects.get(user=request.user)
        attendance_date = request.POST.get('date')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        status = request.POST.get('status')

        # Check if attendance already marked
        if Attendance.objects.filter(employee=employee, date=attendance_date).exists():
            message = "Attendance already marked for this date."
        else:
            Attendance.objects.create(
                employee=employee,
                date=attendance_date,
                check_in=check_in,
                check_out=check_out,
                status=status
            )
            message = "Attendance submitted successfully."

    return render(request, 'attendance_form.html', {'message': message})
