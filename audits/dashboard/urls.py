from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('auditsapi', views.auditsapi, name='auditsapi'),
    path('graphapi', views.graphapi, name='graphapi'),
    path('timelineapi', views.timelineapi, name='timelineapi'),
    path('dateapi', views.dateapi, name='dateapi'),
    path('showresults', views.showresults, name='showresults'),
    path('filtered_data_view/', views.filtered_data_view, name='filtered_data_view'),
    
    path('widgets/', views.widget_view, name='widgets'),
    # path('dropdown/', views.dropdown_view, name='dropdown'),

    # path('hourdate/', views.hourdate, name='hourdate'),
    path('hourdate/', views.hourdate, name='hourdate'),
    path('hourdate/<str:start_date>/<str:end_date>/', views.hourdate, name='hourdate_dates'),




    path('register', views.register, name='register'),
    path('user_login', views.user_login,  name='user_login'),
    # path(r'^user_login/$', views.user_login, {'redirect_authenticated_user': True},name='user_login'),
    # path('chart_view', views.chart_view, name='chart_view'),

    path('dropdown/', views.dashboard, name='dropdown'),
    path('get_type_counts/', views.get_type_counts, name='get_type_counts'),

    # path('display-data/', views.display_data, name='display_data'),
    # path('get-type-data/', views.get_type_data, name='get_type_data'),

    path('display_app/', views.display_app, name='display_app'),
    path('display_typedata/', views.display_typedata, name='display_typedata'),
    path('display_severitydata/', views.display_severitydata, name='display_severitydata'),

    # path('display_severitydata/?<str:start_date>&<str:end_date>/', views.display_severitydata, name='display_severitydata'),




]
