from django.urls import path
from .views import AttendanceListCreateView, EmployeeListView, MyAttendanceView, AttendanceTableView
from .views import login_view, logout_view, mark_attendance_view, register_view

urlpatterns = [
    path('attendance/', AttendanceListCreateView.as_view(), name='attendance-list-create'),
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('my-attendance/', MyAttendanceView.as_view(), name='my-attendance'),

    path('register/', register_view, name='register'),
    
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # path('my-attendance/', MyAttendanceTemplateView.as_view(), name='my-attendance'),
    path('mark-attendance/', mark_attendance_view, name='mark-attendance'),
    path('my-attendance-table/', AttendanceTableView.as_view(), name='my-attendance-table'),
]
