from django.urls import path
from . import views

urlpatterns = [
    path('protected/', views.protected_view, name='protected-view'),
    path('custom-headers/', views.custom_headers_view, name='custom-headers-view'),
    path('error-handling/', views.error_handling_view, name='error-handling-view'),
    path('rate-limited/', views.rate_limited_view, name='rate-limited-view'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('statistics/json/', views.get_statistics, name='get_statistics'),


]
